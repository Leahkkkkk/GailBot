""" 
Implementation of Component of each page

Console
    @ a console window that display all logged message

MainStack
    @ basic structure for displaying multiple pages and linking every
      pages 
      
      public function:
      gotoConfirm() 
      gotoTranscribeInProgress()
      gotoTranscribeSuccess()
      gotoFileUploadPage()
      confirmCancel()
    
MenuBar
    @ a menubar, currently only has console open and console close action

StatusBar
    @ a statusbar that is able to display status msg
    
    public function:
    showStatusMsg(msg:str, time:int = None)
"""