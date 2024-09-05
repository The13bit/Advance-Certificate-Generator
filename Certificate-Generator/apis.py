
"""
APIs for interacting with Google Forms and Spreadsheets

This module provides functions for creating a spreadsheet and linking a form
to it, getting JSON data from a spreadsheet, removing a form and its associated
spreadsheet, and getting the boxes from a slide in a Google Slides document.

The functions are designed to be used with the `asyncio` library, and are
intended to be used with the `Thread_lock` module to ensure that only one
request is sent to the Google API at a time.

"""

from Auth import api, auth, current_dir
from Thread_lock import Locker


def createSpreadsheetAndLinkForm(formId):
    """
    Creates a spreadsheet and links a form to it.

    Args:
        formId (str): The ID of the form to link to the spreadsheet.

    Returns:
        dict: The result of the link operation.
    """
    with Locker():
        request = {
            "function": "createSpreadsheetAndLinkForm",
            "parameters": [formId],
            "devMode": "False"
        }
        gapi = auth()
        entry = api(gapi)
        return entry.Link_form_to_spreadsheet(request)


# def LoadAndSaveCertTemplate(spreadId):
#     """
#     Loads a certificate template from a spreadsheet and saves it as a JSON file.

#     Args:
#         spreadId (str): The ID of the spreadsheet containing the template.

#     Returns:
#         str: The JSON representation of the template.
#     """
#     request = {
#         "function": "getBoxesFromSlide",
#         "parameters": [spreadId],
#         "devMode": "True"
#     }
#     gapi = auth()
#     entry = api(gapi)
#     return entry.cert_access(request)


# def HandleImageData(data):
#     """
#     Handles image data from a form response.

#     Args:
#         data (str): The image data from the form response.

#     Returns:
#         str: The image data as a JSON object.
#     """
#     request = {
#         "function": "handleImageData",
#         "parameters": [data],
#         "devMode": "True"
#     }
#     gapi = auth()
#     entry = api(gapi)
#     return entry.Image_access(request)


def Get_Json(spreadId, inx):
    """
    Gets JSON data from a spreadsheet.

    Args:
        spreadId (str): The ID of the spreadsheet to get data from.
        inx (int): The index of the row to start getting data from.

    Returns:
        dict: The JSON data from the spreadsheet.
    """
    with Locker():
        request = {
            "function": "spreadsheetToJson",
            "parameters": [spreadId, inx],
            "devMode": "False"
        }
        gapi = auth()
        entry = api(gapi)
        return entry.JSonSpread(request, spreadId)


def Remove_entry(spreadId, formId):
    """
    Removes a form and its associated spreadsheet.

    Args:
        spreadId (str): The ID of the spreadsheet to remove.
        formId (str): The ID of the form to remove.

    Returns:
        bool: True if the form and spreadsheet were successfully removed.
    """
    request = {
        "function": "delete_form_spread",
        "parameters": [spreadId, formId],
        "devMode": "False"
    }
    gapi = auth()
    entry = api(gapi)
    return entry.delete_form_sheet(request, formId)




