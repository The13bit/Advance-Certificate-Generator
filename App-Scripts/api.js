/**
 * Return the set of folder names contained in the user's root folder as an
 * object (with folder IDs as keys).
 * @return {Object} A set of folder names keyed by folder ID.
 */



function delete_form_spread(spreadId,formId){
    DriveApp.getFileById(spreadId).setTrashed(true)
    DriveApp.getFileById(formId).setTrashed(true)
  }
  
  
  
  
  function createSpreadsheetAndLinkForm(formId) {
    var form = FormApp.openById(formId);
    var name = form.getTitle() + "(RESPONSE)"
    Logger.log( form.getTitle())
    var files = DriveApp.getFilesByName(name)
    if (files.hasNext()) {
      return "Link already exists"
    }
  
    var spreadsheet = SpreadsheetApp.create(name);
    var spreadsheetId = spreadsheet.getId();
  
    form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheetId);
  
    var sheet = spreadsheet.getSheets()[0];
  
  
    var columns = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0]
    var redundant = ["Timestamp"]
    var ans = columns.filter((item) =>
      !redundant.includes(item)
    )
   
  
    return {
      'Form_Name': form.getTitle(),
      'spreadsheetId': spreadsheetId,
      'formId': form.getId(),
      colums: ans,
      index:0
      
  
    };
  }
  function spreadsheetToJson(spreadId,inx) {
    //var spreadId="1mLuvk5HQt15Wj0698O8Dx3BciVZmgY6Ewh76jKI6XYQ"
    
    var spreadsheet = SpreadsheetApp.openById(spreadId);
    var sheet = spreadsheet.getSheets()[0]; // Get the first sheet
    var range = sheet.getDataRange(); // Get the range of cells containing data
    var values = range.getValues(); // Get the values of the cells in the range
  
    var data = [];
    var headers = values[0]; // Assume the first row is headers
  
    for (var row = 1+inx; row < values.length; row++) {
      var rowData = {};
      for (var col = 1; col < headers.length; col++) {
        rowData[headers[col]] = values[row][col];
      }
      data.push(rowData);
    }
  
    var json = JSON.stringify(data);
    Logger.log(json)
    return {
      data:json,
      index:row-1
    }
  }
  
  