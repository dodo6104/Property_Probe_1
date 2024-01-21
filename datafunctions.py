import gspread
import time
import sys
import traceback
jsonData = {
    #your info
}
sa = gspread.service_account_from_dict(jsonData)
sh = sa.open("DataforMaros")

def savedate(date, city, title, link, nameofSite):
    wks = sh.worksheet("Sended Data")
    try:
        wks.insert_row([date, city, title, link, nameofSite], 2)
        wks.delete_row(201)
    except gspread.exceptions.APIError:
        time.sleep(15)
        savedate(date, city, title, link, nameofSite)

def loadLast(nameofsheet):
    wks = sh.worksheet(nameofsheet)
    return [wks.acell('A2').value, wks.acell('B2').value, wks.acell('C2').value, wks.acell('D2').value]

def returnDataForMail(x): return sh.worksheet("Information").acell(x).value

def saveErrors(exc_type, exc_value, exc_traceback): 
    print( "bla: ",''.join(traceback.format_tb(exc_traceback)))
    sh.worksheet("Information").insert_row([''.join(traceback.format_tb(exc_traceback))] ,5)
    