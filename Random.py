#  This code will write a random number to a Google Sheet.
#  Written by Ken Flerlage, December, 2021.

import datetime
import json
import random
import gspread
import boto3
from oauth2client.service_account import ServiceAccountCredentials
from botocore.exceptions import ClientError

#------------------------------------------------------------------------------------------------------------------------------
# Write a message to the log (or screen). When running in AWS, print will write to Cloudwatch.
#------------------------------------------------------------------------------------------------------------------------------
def log (msg):
    logTimeStamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(str(logTimeStamp) + ": " + msg)

#------------------------------------------------------------------------------------------------------------------------------
# Log a message and exit the program.
#------------------------------------------------------------------------------------------------------------------------------
def end_function(msg=''):
    if msg != '':
        log(msg)
    
    exit()

#------------------------------------------------------------------------------------------------------------------------------
# Main lambda handler
#------------------------------------------------------------------------------------------------------------------------------
def lambda_handler(event, context):
    # Get the Google Sheets credentials from S3
    s3 = boto3.client('s3')
    bucket = "flerlage-lambda"
    key = "creds.json"
    object = s3.get_object(Bucket=bucket, Key=key)
    content = object['Body']
    creds = json.loads(content.read())

    # Open Google Sheet
    scope =['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # Read your Google API key from a local json file.
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    gc = gspread.authorize(credentials) 

    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/15dsBQF3Y-9ZYDq4yKuPr9FcZpNFQTnCrNvowGTcJiSQ')
    worksheet = sheet.get_worksheet(0)

    randNumber = random.random()

    worksheet.update_cell(1, 1, str(randNumber))

    log("Wrote a new random number, " + str(randNumber))

#------------------------------------------------------------------------------------------------------------------------------
# Labmda will always call the lambda handler function, so this will not get run unless you are running locally.
# This code will connect to AWS locally. This requires a credentials file in C:\Users\<Username>\.aws\
# For further details, see: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
#------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    log("Code is running locally..............................................................")
    context = []
    event = {"state": "DISABLED"}
    boto3.setup_default_session(region_name="us-east-2", profile_name="default")
    lambda_handler(event, context)