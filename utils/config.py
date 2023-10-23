from dotenv import load_dotenv, find_dotenv
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(find_dotenv(root_path + '/.env'))


# ------------------------------
# |     APP Config  |
# ------------------------------
BASE_SERVER_HOST = os.getenv('BASE_SERVER_HOST')
ACCOUNT_VALIDATOR_URL = os.getenv('ACCOUNT_VALIDATOR_URL')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECEIVER1 = os.getenv('EMAIL_RECEIVER1')
EMAIL_RECEIVER2 = os.getenv('EMAIL_RECEIVER2')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')


# ------------------------------
# |         SQL Server Config  |
# ------------------------------
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_PORT = os.getenv('SQL_PORT')

# ------------------------------
# | SPLUNK Config  |
# ------------------------------
SPLUNK_URL = os.getenv('SPLUNK_URL')
SPLUNK_KEY = os.getenv('SPLUNK_KEY')
SPLUNK_HOST = os.getenv('SPLUNK_HOST')
SPLUNK_SOURCE = os.getenv('SPLUNK_SOURCE')

# ------------------------------
# |       Logger Config        |
# ------------------------------
# Logger type   -> persist | show
# Logger Format -> string  | json
LOGGER_TYPE = os.getenv('LOGGER_TYPE')
LOGGER_LEVEL = os.getenv('LOGGER_LEVEL')
LOGGER_FORMAT = os.getenv('LOGGER_FORMAT')

# ------------------------------
# |       MONGO Config        |
# ------------------------------
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_AUTH_MECHANISM = os.getenv('MONGO_AUTH_MECHANISM')
MONGO_REPSET = os.getenv('MONGO_REPSET')

MYSQL_GENERAL_HOST = os.getenv('MYSQL_GENERAL_HOST')
MYSQL_GENERAL_DATABASE = os.getenv('MYSQL_GENERAL_DATABASE')
MYSQL_GENERAL_USERNAME = os.getenv('MYSQL_GENERAL_USERNAME')
MYSQL_GENERAL_PASSWORD = os.getenv('MYSQL_GENERAL_PASSWORD')
