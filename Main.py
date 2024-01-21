import WebsData
import sys
import traceback
import datafunctions

sys.excepthook = datafunctions.saveErrors

try:
    WebsData.vlmweb()
except Exception as e:
    datafunctions.saveErrors(type(e), e, e.__traceback__)


try:
    WebsData.obchodnyvestnik()
except Exception as e:
    datafunctions.saveErrors(type(e), e, e.__traceback__)

    
