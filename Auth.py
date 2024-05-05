import json
from pathlib import Path
import logging as log
import select

from googleapiclient.discovery import build

from oauth2client import client, file, tools
import os
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from requests import Request
from google.auth.exceptions import RefreshError
load_dotenv()
class auth:
  def __init__(self) :
    self.client_secret=os.environ.get("GOOGLE_CREDENTIAL_PATH")
    self.token=Path("./Credentials/token.json")
    self.scopes=["https://www.googleapis.com/auth/forms.body","https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/script.projects",	"https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/forms",	"https://www.googleapis.com/auth/presentations","https://www.googleapis.com/auth/gmail.send"]
    self.credntials=None

  def get_service(self):
    self.__authenticate()
    return build("script","v1",credentials=self.credntials)
  def create_mail_service(self):
    self.__authenticate()
    return build("gmail","v1",credentials=self.credntials)
  def create_form_servcice(self):
    self.__authenticate()
    return build("forms","v1",credentials=self.credntials)
  def __authenticate(self):
        log.debug(f"Searching for token in {self.token}")
        if self.token.exists():
            
            self.credntials = Credentials.from_authorized_user_file(self.token)
            try:
               
              if self.__Expired():
                self.credntials.refresh(Request())
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
  """
  A class that represents an API.

  Attributes:
    script_id (str): The script ID.
    gapi (object): An instance of the GAPI class.

  Methods:
    __init__(self, gapi): Initializes the api object.
    create_mailer(self): Creates a mailer service.
    JSonSpread(self, request): Executes a script and returns the JSON response.
    Link_form_to_spreadsheet(self, request): Links a form to a spreadsheet.
    __entry_maker(self, res): Makes an entry in the Entries.json file.
  """

  def __init__(self, gapi):
    """
    Initializes the api object.

    Args:
      gapi (object): An instance of the GAPI class.

    """
    print(os.environ.get("SCRIPT_ID"))
    self.script_id = os.environ.get("SCRIPT_ID")
    self.gapi = gapi
  
  def fetch_form(self,formId):
    with self.gapi.create_form_servcice() as service:
      print(service.forms().responses().list(formId=formId).execute())


  def create_mailer(self):
    """
    Creates a mailer service.

    Returns:
      object: The mailer service object.
    """
    return self.gapi.create_mail_service()
  
  def delete_form_sheet(self,request,formId):
    with self.gapi.get_service() as service:
      response=service.scripts().run(scriptId=self.script_id,body=request).execute()
      if response.get('error'):
        message = response['error']['details'][0]['errorMessage']
        raise RuntimeError(message)
      with open('Entries.json','r+') as file:
        data=json.load(file)
        data["Entry"]=[entry for entry in data["Entry"] if entry.get("formId")!=formId]
        file.seek(0)
        json.dump(data,file,indent=4)
        file.truncate()

      return True



  def JSonSpread(self, request,sheetId):
    """
    Executes a script and returns the JSON response.

    Args:
      request (object): The request object.

    Returns:
      object: The JSON response.
    """
    with self.gapi.get_service() as service:
      response = service.scripts().run(scriptId=self.script_id, body=request).execute()
      if response.get('error'):
        message = response['error']['details'][0]['errorMessage']
        raise RuntimeError(message)
      with open("Entries.json","r+") as file:
        content=json.load(file)
        for entry in content["Entry"]:
          if entry["spreadsheetId"]==sheetId:
            entry["index"]=response["response"]["result"]["index"]
        file.seek(0)
        json.dump(content,file,indent=4)
        file.truncate()


      
      return response["response"]["result"]["data"]

  def Link_form_to_spreadsheet(self, request):
    """
    Links a form to a spreadsheet.

    Args:
      request (object): The request object.

    Returns:
      object: The result of the link operation.
    """
    with self.gapi.get_service() as service:
      response = service.scripts().run(scriptId=self.script_id, body=request).execute()
      if response.get('error'):
        message = response['error']['details'][0]['errorMessage']
        raise RuntimeError(message)
      else:
        print(response['response']['result'])
        store = response['response']['result']
        if isinstance(store, dict):
          self.__entry_maker(store)
        return store

  def __entry_maker(self, res):
    """
    Makes an entry in the Entries.json file.

    Args:
      res (object): The entry object.
    """
    entry_file = Path("Entries.json")
    if not entry_file.exists():
      data = {"Entry": []}
      with entry_file.open("w") as file:
        json.dump(data, file,indent=4)

    with entry_file.open("r+") as file:
      content = json.load(file)
      content["Entry"].append(res)
      file.seek(0)
      json.dump(content, file,indent=4)
      

      

