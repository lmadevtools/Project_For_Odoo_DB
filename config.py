import os

#DB POSTGRES - also possible to put it in an ini file
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "postgres"
DB_USER     = "postgres"
DB_PASSWORD = "postgres"

#SMTP MAIL CONFIG  -- NOT USED
SMTP_SERVER = 'smtp.server.com'
SMTP_PORT = 25  # 25 is The default SMTP port for unauthenticated sending
MAIL_USER = 'email@server.com'
MAIL_PASSWORD = "mail_password"
#############

ORDER_PREFIX = "CMD" 
ORDER_NUMBERS = 4 

DIR_DATA_FILES     = 'Data/'
DIR_LOGS_FILES     = 'Logs/'

#create dirs if necessary
if not os.path.isdir(DIR_DATA_FILES):
    os.mkdir(DIR_DATA_FILES)

if not os.path.isdir(DIR_LOGS_FILES):
    os.mkdir(DIR_LOGS_FILES)