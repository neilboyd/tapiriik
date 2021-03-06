import os
from datetime import timedelta
from Crypto.PublicKey import RSA

# Look in settings.py for more settings to override
# including mongodb, rabbitmq, and redis connection settings

DEBUG = os.getenv("DEBUG", False) in (True, 'True')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# This is the url that is used for redirects after logging in to each service
# It only needs to be accessible to the client browser
WEB_ROOT = os.getenv("WEB_ROOT", "http://localhost:8000")

# email settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False) in (True, 'True')
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# Default is a new key every time, which is okay for testing locally, but won't be able to decrypt next time
key = RSA.generate(2048)
CREDENTIAL_STORAGE_PRIVATE_KEY = os.getenv("CREDENTIAL_STORAGE_PRIVATE_KEY", key.exportKey("PEM"))
CREDENTIAL_STORAGE_PUBLIC_KEY = os.getenv("CREDENTIAL_STORAGE_PUBLIC_KEY", key.publickey().exportKey("PEM"))

# PayPal
PP_WEBSCR = os.getenv("PP_WEBSCR", "https://www.sandbox.paypal.com/cgi-bin/webscr")
PP_RECEIVER_ID = os.getenv("PP_RECEIVER_ID", "NR6NTNSRT7NDJ")

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

MAPMYFITNESS_CLIENT_KEY = os.getenv("MAPMYFITNESS_CLIENT_KEY")
MAPMYFITNESS_CLIENT_SECRET = os.getenv("MAPMYFITNESS_CLIENT_SECRET")
