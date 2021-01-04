from tapiriik.services.service_base import ServiceAuthenticationType, ServiceBase
from tapiriik.services.service_record import ServiceRecord
from tapiriik.services.api import APIException, APIAuthorizationException
from tapiriik.services.interchange import UploadedActivity, ActivityType, WaypointType, Waypoint, Location
from tapiriik.settings import WEB_ROOT, MAPMYFITNESS_CLIENT_KEY, MAPMYFITNESS_CLIENT_SECRET

from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlencode
import requests
from django.core.urlresolvers import reverse
from requests_oauthlib import OAuth1

import logging

logger = logging.getLogger(__name__)

class MapMyFitnessService(ServiceBase):
    ID = "mapmyfitness"
    DisplayName = "MapMyFitness"
    AuthenticationType = ServiceAuthenticationType.OAuth
    UserAuthorizationURL = None
    AuthenticationNoFrame = True
    OutstandingOAuthRequestTokens = {}

    _activityMappings = {16: ActivityType.Running,
                         11: ActivityType.Cycling,
                         41: ActivityType.MountainBiking,
                         9: ActivityType.Walking,
                         24: ActivityType.Hiking,
                         398: ActivityType.DownhillSkiing,
                         397: ActivityType.CrossCountrySkiing,  # actually "backcountry" :S
                         107: ActivityType.Snowboarding,
                         86: ActivityType.Skating,  # ice skating
                         15: ActivityType.Swimming,
                         57: ActivityType.Rowing,  # canoe/rowing
                         211: ActivityType.Elliptical,
                         21: ActivityType.Other}
    SupportedActivities = list(_activityMappings.values())

    def WebInit(self):
        logger.debug("WebInit")
        redirect_uri = WEB_ROOT + reverse("oauth_return", kwargs={"service": "mapmyfitness"})
        params = {'client_id': MAPMYFITNESS_CLIENT_KEY,
                  'response_type': 'code',
                  'redirect_uri': redirect_uri}
        self.UserAuthorizationURL = \
            "https://api.mapmyfitness.com/v7.1/oauth2/authorize/?" + urlencode(params)

    def GenerateUserAuthorizationURL(self, session, level=None):
        logger.debug("GenerateUserAuthorizationURL")
        oauth = OAuth1(MAPMYFITNESS_CLIENT_KEY, client_secret=MAPMYFITNESS_CLIENT_SECRET)
        response = requests.post("https://api.mapmyfitness.com/v7.1/oauth2/request_token", auth=oauth)
        credentials = parse_qs(response.text)
        token = credentials["oauth_token"][0]
        self.OutstandingOAuthRequestTokens[token] = credentials["oauth_token_secret"][0]
        reqObj = {"oauth_token": token, "oauth_callback": WEB_ROOT + reverse("oauth_return", kwargs={"service": "mapmyfitness"})}
        return "https://api.mapmyfitness.com/v7.1/oauth2/authorize?" + urlencode(reqObj)

    def _apiHeaders(self, serviceRecord):
        logger.debug("_apiHeaders")
        return {"Authorization": "Bearer " + serviceRecord.Authorization["Token"],
                "Accept-Charset": "UTF-8"}

    def _getUserId(self, serviceRecord):
        logger.debug("_getUserId")
        response = requests.get("https://api.mapmyfitness.com/v7.1/users/get_user", headers=self._apiHeaders(serviceRecord))
        responseData = response.json()
        return responseData["result"]["output"]["user"]["user_id"]

    def RetrieveAuthorizationToken(self, req, level):
        logger.debug("RetrieveAuthorizationToken")
        from tapiriik.services import Service

        code = req.GET.get("code")
        params = {"grant_type": "authorization_code",
                  "code": code,
                  "client_id": MAPMYFITNESS_CLIENT_KEY,
                  "client_secret": MAPMYFITNESS_CLIENT_SECRET,
                  "redirect_uri": WEB_ROOT + reverse("oauth_return", kwargs={"service": "mapmyfitness"})}

        response = requests.post("https://api.mapmyfitness.com/v7.1/oauth2/access_token",
                                 data=urlencode(params),
                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                          "api-key": MAPMYFITNESS_CLIENT_KEY})

        if response.status_code != 200:
            raise APIException("Invalid code")
        token = response.json()["access_token"]

        uid = self._getUserId(ServiceRecord({"Authorization": {"Token": token}}))

        return (uid, {"Token": token})

    def RevokeAuthorization(self, serviceRecord):
        logger.debug("RevokeAuthorization")
        oauth = self._getOauthClient(serviceRecord)
        resp = requests.post("https://api.mapmyfitness.com/v7.1/oauth2/revoke", auth=oauth)
        if resp.status_code != 200:
            raise APIException("Unable to deauthorize MMF auth token, status " + str(resp.status_code) + " resp " + resp.text, serviceRecord)

    def _getActivityTypeHierarchy(self):
        logger.debug("_getActivityTypeHierarchy")
        if hasattr(self, "_activityTypes"):
            return self._activityTypes
        response = requests.get("https://api.mapmyfitness.com/v7.1/workouts/get_activity_types")
        data = response.json()
        self._activityTypes = {}
        for actType in data["result"]["output"]["activity_types"]:
            self._activityTypes[int(actType["activity_type_id"])] = actType
        return self._activityTypes

    def _resolveActivityType(self, actType):
        logger.debug("_resolveActivityType")
        self._getActivityTypeHierarchy()
        while actType not in self._activityMappings or self._activityTypes[actType]["parent_activity_type_id"] is not None:
            actType = int(self._activityTypes[actType]["parent_activity_type_id"])
        if actType in self._activityMappings:
            return self._activityMappings[actType]
        else:
            return ActivityType.Other

    def DownloadActivityList(self, serviceRecord, exhaustive=False):
        logger.debug("DownloadActivityList")
        oauth = self._getOauthClient(serviceRecord)

        allItems = []

        offset = 0

        while True:
            response = requests.get("https://api.mapmyfitness.com/v7.1/workouts/get_workouts?limit=25&start_record=" + str(offset), auth=oauth)
            if response.status_code != 200:
                if response.status_code == 401 or response.status_code == 403:
                    raise APIAuthorizationException("No authorization to retrieve activity list", serviceRecord)
                raise APIException("Unable to retrieve activity list " + str(response), serviceRecord)
            data = response.json()
            print(data)
            allItems += data["result"]["output"]["workouts"]
            if not exhaustive or int(data["result"]["output"]["count"]) < 25:
                break

        activities = []
        for act in allItems:
            activity = UploadedActivity()
            activity.StartTime = datetime.strptime(act["workout_date"] + " " + act["workout_start_time"], "%Y-%m-%d %H:%M:%S")
            activity.EndTime = activity.StartTime + timedelta(0, round(float(act["time_taken"])))
            activity.Distance = act["distance"]

            activity.Type = self._resolveActivityType(int(act["activity_type_id"]))
            activity.CalculateUID()

            activity.UploadedTo = [{"Connection": serviceRecord, "ActivityID": act["workout_id"]}]
            activities.append(activity)
        return activities

    def DownloadActivity(self, serviceRecord, activity):
        logger.debug("DownloadActivity")
        activityID = [x["ActivityID"] for x in activity.UploadedTo if x["Connection"] == serviceRecord][0]
        print (activityID)# route id 175411456 key 2025466620
        oauth = self._getOauthClient(serviceRecord)
        response = requests.get("https://api.mapmyfitness.com/v7.1/routes/get_routes", auth=oauth)
        print (response.text)
