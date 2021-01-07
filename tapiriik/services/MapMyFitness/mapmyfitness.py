from tapiriik.services.service_base import ServiceAuthenticationType, ServiceBase
from tapiriik.services.service_record import ServiceRecord
from tapiriik.services.api import APIException, UserException, UserExceptionType
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
        response = requests.get("https://api.mapmyfitness.com/v7.1/user/self", headers=self._apiHeaders(serviceRecord))
        logger.debug("_getUserId response=%s" % response)
        responseData = response.json()
        return responseData["id"]

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
        # there doesn't seem to be a way to revoke the token
        pass

    def _getActivityTypeHierarchy(self, headers):
        logger.debug("_getActivityTypeHierarchy")
        if hasattr(self, "_activityTypes"):
            return self._activityTypes
        response = requests.get("https://api.mapmyfitness.com/v7.1/activity_type", headers=headers)
        data = response.json()
        self._activityTypes = {}
        for actType in data["_embedded"]["activity_types"]:
            self._activityTypes[actType["_links"]["root"][0]["id"]] = actType
        return self._activityTypes

    def _resolveActivityType(self, actType, headers):
        logger.debug("_resolveActivityType")
        self._getActivityTypeHierarchy(headers)
        if actType in self._activityMappings:
            return self._activityMappings[actType]
        activity = self._activityTypes[actType]
        parentLink = activity["_links"].get("parent")
        if parentLink is not None:
            parentId = parentLink[0]["id"]
            parent = self._activityMappings[parentId]
            return self._resolveActivityType(parent, headers)
        return ActivityType.Other

    def DownloadActivityList(self, serviceRecord, exhaustive=False):
        logger.debug("DownloadActivityList")
        allItems = []
        headers=self._apiHeaders(serviceRecord)
        nextRequest = '/v7.1/workout/?user=' + str(serviceRecord.ExternalID)
        while True:
            response = requests.get("https://api.mapmyfitness.com" + nextRequest, headers=headers)
            if response.status_code != 200:
                if response.status_code == 401 or response.status_code == 403:
                    raise APIException("No authorization to retrieve activity list", block=True, user_exception=UserException(UserExceptionType.Authorization, intervention_required=True))
                raise APIException("Unable to retrieve activity list " + str(response), serviceRecord)
            data = response.json()
            allItems += data["_embedded"]["workouts"]
            nextLink = data["_links"].get("next")
            if not exhaustive or not nextLink:
                break
            nextRequest = nextLink[0]["href"]

        activities = []
        for act in allItems:
            activity = UploadedActivity()
            activity.StartTime = datetime.strptime(act["start_datetime"], "%Y-%m-%dT%H:%M:%S%z")
            aggregates = act["aggregates"]
            activity.EndTime = activity.StartTime + timedelta(0, round(float(aggregates["elapsed_time_total"])))
            activity.Distance = aggregates["distance_total"]
            activityTypeId = act["_links"]["activity_type"][0]["id"]
            activity.Type = self._resolveActivityType(activityTypeId, headers)
            activity.ServiceData = {"ActivityID": act["reference_key"]}
            activity.UploadedTo = [{"Connection": serviceRecord, "ActivityID": act["reference_key"]}]
            activity.CalculateUID()
            activities.append(activity)
        return activities

    def DownloadActivity(self, serviceRecord, activity):
        # TODO probably get rid of UploadedTo and do the same as runkeeper
        logger.debug("DownloadActivity")
        activityID = [x["ActivityID"] for x in activity.UploadedTo if x["Connection"] == serviceRecord][0]
        response = requests.get("https://api.mapmyfitness.com/v7.1/routes/get_routes", headers=self._apiHeaders(serviceRecord))

    def UploadActivity(self, serviceRecord, activity):
        # TODO
        pass

    def DeleteCachedData(self, serviceRecord):
        pass

    def DeleteActivity(self, serviceRecord, uploadId):
        pass
