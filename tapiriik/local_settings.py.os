import os
from datetime import timedelta

# Look in settings.py for more settings to override
# including mongodb, rabbitmq, and redis connection settings

DEBUG = os.getenv("DEBUG", False) in (True, 'True')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# This is the url that is used for redirects after logging in to each service
# It only needs to be accessible to the client browser
WEB_ROOT = os.getenv("WEB_ROOT", "http://localhost:8000")

# In order the generate the keys to use for the environment variables:
# from Crypto.PublicKey import RSA
# key = RSA.generate(2048)
# key.exportKey("PEM")
# key.publickey().exportKey("PEM")
# NB: append .__repr__() to the above commands to get the secrets for the pipeline
CREDENTIAL_STORAGE_PRIVATE_KEY = os.getenv("CREDENTIAL_STORAGE_PRIVATE_KEY", None)
CREDENTIAL_STORAGE_PUBLIC_KEY = os.getenv("CREDENTIAL_STORAGE_PUBLIC_KEY", b"NotTheRealKeyFYI")

# This is where sync logs show up
# It is the only directory that needs to be writable by the webapp user
USER_SYNC_LOGS = "./"

# How many total sync workers are expected to be running
TOTAL_SYNC_WORKERS = 1

# Services to hide from regular signup
SOFT_LAUNCH_SERVICES = os.getenv("SOFT_LAUNCH_SERVICES", "").split(",")

# These settings are used to communicate with each respective service
# Register your installation with each service to get these values

# http://beginnertriathlete.com/discussion/contact.asp?department=api
BT_APIKEY = os.getenv("BT_APIKEY")

DROPBOX_FULL_APP_KEY = os.getenv("DROPBOX_FULL_APP_KEY")
DROPBOX_FULL_APP_SECRET = os.getenv("DROPBOX_FULL_APP_SECRET")

DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

ENDOMONDO_CLIENT_KEY = os.getenv("ENDOMONDO_CLIENT_KEY")
ENDOMONDO_CLIENT_SECRET = os.getenv("ENDOMONDO_CLIENT_SECRET")

MOTIVATO_PREMIUM_USERS_LIST_URL = os.getenv("MOTIVATO_PREMIUM_USERS_LIST_URL", "http://...")

NIKEPLUS_CLIENT_NAME = os.getenv("NIKEPLUS_CLIENT_NAME")
NIKEPLUS_CLIENT_ID = os.getenv("NIKEPLUS_CLIENT_ID")
NIKEPLUS_CLIENT_SECRET = os.getenv("NIKEPLUS_CLIENT_SECRET")

PULSSTORY_CLIENT_ID = os.getenv("PULSSTORY_CLIENT_ID")
PULSSTORY_CLIENT_SECRET = os.getenv("PULSSTORY_CLIENT_SECRET")

RUNKEEPER_CLIENT_ID = os.getenv("RUNKEEPER_CLIENT_ID")
RUNKEEPER_CLIENT_SECRET = os.getenv("RUNKEEPER_CLIENT_SECRET")

RWGPS_APIKEY = os.getenv("RWGPS_APIKEY")

SETIO_CLIENT_ID = os.getenv("SETIO_CLIENT_ID")
SETIO_CLIENT_SECRET = os.getenv("SETIO_CLIENT_SECRET")

SINGLETRACKER_CLIENT_ID = os.getenv("SINGLETRACKER_CLIENT_ID")
SINGLETRACKER_CLIENT_SECRET = os.getenv("SINGLETRACKER_CLIENT_SECRET")

SMASHRUN_CLIENT_ID = os.getenv("SMASHRUN_CLIENT_ID")
SMASHRUN_CLIENT_SECRET = os.getenv("SMASHRUN_CLIENT_SECRET")

SPORTTRACKS_CLIENT_ID = os.getenv("SPORTTRACKS_CLIENT_ID")
SPORTTRACKS_CLIENT_SECRET = os.getenv("SPORTTRACKS_CLIENT_SECRET")

STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")

# TODO read this from environment: https://github.com/neilboyd/tapiriik/issues/18
STRAVA_RATE_LIMITS = [ (  timedelta(minutes=15) , 100 ) , (  timedelta(days=1) , 1000 ) ]

TRAINASONE_SERVER_URL = "https://beta.trainasone.com"
TRAINASONE_CLIENT_SECRET = os.getenv("TRAINASONE_CLIENT_SECRET")
TRAINASONE_CLIENT_ID = os.getenv("TRAINASONE_CLIENT_ID")

TRAININGPEAKS_CLIENT_ID = os.getenv("TRAININGPEAKS_CLIENT_ID")
TRAININGPEAKS_CLIENT_SECRET = os.getenv("TRAININGPEAKS_CLIENT_SECRET")
TRAININGPEAKS_CLIENT_SCOPE = "cats:cuddle dogs:throw-frisbee"
TRAININGPEAKS_API_BASE_URL = "https://api.trainingpeaks.com"
TRAININGPEAKS_OAUTH_BASE_URL = "https://oauth.trainingpeaks.com"
