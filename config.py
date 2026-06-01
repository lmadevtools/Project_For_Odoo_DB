import os

#DB POSTGRES - also possible to put it in an ini file
DB_HOST     = "localhost"
DB_PORT     = 5432
DB_NAME     = "postgres"
DB_USER     = "postgres"
DB_PASSWORD = "postgres"

ORDER_PREFIX = "CMD" 
ORDER_NUMBERS = 4 

DIR_DATA_FILES     = 'Data/'
DIR_LOGS_FILES     = 'Logs/'

#create dirs if necessary
if not os.path.isdir(DIR_DATA_FILES):
    os.mkdir(DIR_DATA_FILES)

if not os.path.isdir(DIR_LOGS_FILES):
    os.mkdir(DIR_LOGS_FILES)