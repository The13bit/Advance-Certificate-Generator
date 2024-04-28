import json
from math import e
from pathlib import Path
import re
from urllib import request
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import os
from google.oauth2.credentials import Credentials
from requests import Request

from Helper import api, auth



def is_valid_json(js):
   try:
      json.loads(js)
      
   except json.JSONDecodeError as e:
      return False
   return True


    
       
    
          

def main():
  """Runs the sample."""
  # pylint: disable=maybe-no-member
  
  
  DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
  
  # Create an execution request object.
  formId="1PlYTwM_Pu70jhR-FRxxOV3IilJrhvlEkOkASXOAS1Rc"
  request = {"function": "createSpreadsheetAndLinkForm","parameters":[formId, False, "Test" ],"devMode":"True"}
  gapi=auth()
  entry=api(gapi)
  return entry.access(request)
  
  
def createSpreadsheetAndLinkForm(formId):
   request = {"function": "createSpreadsheetAndLinkForm","parameters":[formId, False, "Test" ],"devMode":"True"}
   gapi=auth()
   entry=api(gapi)
   return entry.access(request)

def LoadAndSaveCertTemplate(spreadId):
   request = {"function": "getBoxesFromSlide","parameters":[spreadId],"devMode":"True"}
   gapi=auth()
   entry=api(gapi)
   return entry.cert_access(request)

def HandleImageData(data):
   request={"function": "handleImageData","parameters":[data],"devMode":"True"}
   gapi=auth()
   entry=api(gapi)
   return entry.Image_access(request)
def Get_Json(spreadId):
   request={"function": "spreadsheetToJson","parameters":[spreadId],"devMode":"True"}
   gapi=auth()
   entry=api(gapi)
   return entry.JSonSpread(request)


if __name__ == "__main__":
  print(main())
