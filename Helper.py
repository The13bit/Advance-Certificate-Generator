import json
from pathlib import Path
import logging as log
import pickle
from urllib import response
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import os
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from requests import Request
from google.auth.exceptions import RefreshError
load_dotenv()
class auth:
  def __init__(self) :
    self.client_secret=Path('creds.json')
    self.token=Path("token.json")
    self.scopes=["https://www.googleapis.com/auth/forms.body","https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/script.projects",	"https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/forms",	"https://www.googleapis.com/auth/presentations","https://www.googleapis.com/auth/gmail.send"]
    self.credntials=None

  def get_service(self):
    self.__authenticate()
    return build("script","v1",credentials=self.credntials)
  def create_mail_service(self):
    self.__authenticate()
    return build("gmail","v1",credentials=self.credntials)
  def __authenticate(self):
        log.debug(f"Searching for token in {self.token}")
        if self.token.exists():
            
            self.credntials = Credentials.from_authorized_user_file(self.token)
            try:
               
              if self.__Expired():
                self.credntials.refresh(Request)
            except RefreshError:
              log.debug("Refresh Token Epired ")
              self.__log_in()
              self.__SaveTk()
               
        else:
            self.__log_in()
            self.__SaveTk()
  def __log_in(self):
    flow=client.flow_from_clientsecrets(self.client_secret,self.scopes)
    self.credntials=tools.run_flow(flow,file.Storage(self.token))

  def __SaveTk(self):
        with open(self.token, 'w') as token:
            if self.credntials:
              token.write(self.credntials.to_json())
  def __Expired(self):
    return self.credntials and not self.credntials.expired and \
            self.credntials.refresh_token
  
class api:
  def __init__(self,gapi):
    self.SCOPES=["https://www.googleapis.com/auth/forms.body","https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/script.projects",	"https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/forms",	"https://www.googleapis.com/auth/presentations","https://www.googleapis.com/auth/gmail.send"]
    self.script_id= os.environ.get("SCRIPT_ID")
    self.gapi=gapi
  def Image_access(self,request):
     with self.gapi.get_service() as service:
        response=service.scripts().run(scriptId=self.script_id,body=request).execute()
        if response.get('error'):
          message = response['error']['details'][0]['errorMessage']
          raise RuntimeError(message)
        else:
           print(response["respinse"]['result'])
           entry_file=Path('Entries.json')
           with open(entry_file) as file:
              content=json.load(file)
              content["Signatures"].append(response['response']['result'])
              file.seek(0)
              file.truncate()
              json.dump(content,file,indent=3)
              return True
  def cert_access(self,request):
    with self.gapi.get_service() as service:
      response = service.scripts().run(scriptId=self.script_id, body=request).execute()
      if response.get('error'):
        message = response['error']['details'][0]['errorMessage']
        raise RuntimeError(message)
      else:
        print(response['response']['result'])
        entry_file=Path("Entries.json")
        with entry_file.open("r+") as file:
          content=json.load(file)
          
          content["certificates"].append(response['response']['result'])
          file.seek(0)
          file.truncate()
          json.dump(content,file)
        return True   
  
  def create_mailer(self):
     return self.gapi.create_mail_service()
  def JSonSpread(self,request):
     with self.gapi.get_service() as service:
        response = service.scripts().run(scriptId=self.script_id, body=request).execute()
        if response.get('error'):
          message = response['error']['details'][0]['errorMessage']
          raise RuntimeError(message)
        
        return response["response"]["result"]
  def access(self,request):
    with self.gapi.get_service() as service:

      response = service.scripts().run(scriptId=self.script_id, body=request).execute()
      if response.get('error'):
        message = response['error']['details'][0]['errorMessage']
        raise RuntimeError(message)
      else:
        print(response['response']['result'])
        store=response['response']['result']
        if isinstance(store,dict):
          self.__entry_maker(store)
        return store
  def __entry_maker(self,res):
    entry_file=Path("Entries.json")
    if not entry_file.exists():
       
        data={"count":0,"Entry":[]}
        with entry_file.open("w") as file:
          json.dump(data,file)
       

    with entry_file.open("r+") as file:
      content=json.load(file)
      content["count"]+=1
      
      content["Entry"].append(res)
      file.seek(0)
      json.dump(content,file)

      
