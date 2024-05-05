


from Auth import api, auth
from Thread_lock import Locker


def createSpreadsheetAndLinkForm(formId):
   with Locker():
      request = {"function": "createSpreadsheetAndLinkForm","parameters":[formId],"devMode":"False"}
      gapi=auth()
      entry=api(gapi)
      return entry.Link_form_to_spreadsheet(request)

# def LoadAndSaveCertTemplate(spreadId):
#    request = {"function": "getBoxesFromSlide","parameters":[spreadId],"devMode":"True"}
#    gapi=auth()
#    entry=api(gapi)
#    return entry.cert_access(request)

# def HandleImageData(data):
#    request={"function": "handleImageData","parameters":[data],"devMode":"True"}
#    gapi=auth()
#    entry=api(gapi)
#    return entry.Image_access(request)
def Get_Json(spreadId,inx):
   with Locker():
      request={"function": "spreadsheetToJson","parameters":[spreadId,inx],"devMode":"False"}
      gapi=auth()
      entry=api(gapi)   
      return entry.JSonSpread(request,spreadId)

def Remove_entry(spreadId,formId):
   request={"function": "delete_form_spread","parameters":[spreadId,formId],"devMode":"False"}
   gapi=auth()
   entry=api(gapi)  
   return entry.delete_form_sheet(request,formId)




