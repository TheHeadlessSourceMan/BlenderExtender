# This file provides a way to do commonly needed events

try:
    # note: use namespace so Blender.sys doesn't override sys
    import Blender
    from Blender import *
    inBlender=True
except ImportError:
    inBlender=False

import sys

def doQuit():
    """
    Exactly what happens in here varies from app to app
    """
    if inBlender:
        Blender.Quit()
    else:
        # the catch-all
        sys.exit()

def doEmail(server,user,passwd,fromaddr,toaddr,subject,message):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    smtp = smtplib.SMTP()
    smtp.connect(server)
    if user!=None and user!="" and passwd!=None and passwd!="":
        smtp.login(user,passwd)
    smtp.sendmail(fromaddr, toaddr, msg.as_string())
    smtp.close()


def doFTP(server,fileName,user=None,passwd=None,contents=None):
    from ftplib import FTP
    ftp = FTP(server)
    if user==None or user=="":
        user="anonymous"
    if passwd==None or passwd=="":
        user="anonymous@nowhere.com"
    ftp.login(user,passwd)
    if contents!=None and contents!="":
        f=open(filename+".ftp.tmp","w+")
	f.write(contents)
        f.close()
        f=open(filename+".ftp.tmp","r")
    else:
        f=open(filename,"r")
    ftp.storbinary("STOR "+fileName,f)
    ftp.quit()
    f.close()
    if contents!=None and contents!="":
        os.ulink(filename+".ftp.tmp")


def doHTTP(url,method="GET",user=None,passwd=None):
    """
    Will use cUrl if available, otherwise will use builtin httplib.

    Currently does not support method,user,or passwd
    """
    try:
        # curl is better if we've got it
        import pycurl

        retults=""
        def onLoaded(data):
            retsults=results+data

        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 300)
        curl.setopt(pycurl.NOSIGNAL, 1)
        curl.setopt(c.WRITEFUNCTION,onLoaded)
        curl.perform()
        curl.close()
    except ImportError:
        import httplib

        conn=httplib.HTTPConnection(url)
        results=conn.getresponse()

    return results


def doCommonEvent(eventInfo,params={}):
    """
    This provides a common way to send common events.  You can send one eventInfo, or
    an array of them to be executed.

    eventInfo also contains parameters separated by ":".  Some needed ones are
        close://
        twitter://user:passwd:message
        email://server:user:passwd:from@me.com:to@you.com:subject:message
        ftp://server/file:user:passwd:fileContents
        http://url&x=blah
        exec://command.exe -a=1:2:3 -b=1
        python://x=foo()

    Any items may contain any $(params.key) to have that value inserted.
    Params can either be a dict of params or an object from which you want all values available.
    """
    if type(params).__name__!='dict':
        # If it's an object, try and convert its values into a dict
        params=dict((k,v) for k,v in params.__dict__.iteritems() if not callable(v) and not k.startswith('__'))
    if type(eventInfo).__name__!='list':
        for k,v in params.items():
            eventInfo=eventInfo.replace("$("+k+")",str(v))
        eventInfo=eventInfo.split(":")
        if len(eventInfo)>1:
            while len(eventInfo[1])>0 and (eventInfo[1][0]=="/" or eventInfo[1][0]==" "):
                eventInfo[1]=eventInfo[1][1:] # strip off "//"
        if eventInfo[0]=="close":
            doQuit()
        elif settings.onComplete=="shutdown":
            windll.PowrProf.SetSuspendState(1,1,0)
            # or os.system("Shutdown.exe -s -t 00")
        elif settings.onComplete=="suspend": # aka "sleep"
            windll.PowrProf.SetSuspendState(0,1,0)
        elif settings.onComplete=="hibernate":
            windll.PowrProf.SetSuspendState(0,0,0)
        elif settings.onComplete=="email":
            doEmail(eventInfo[1],eventInfo[2],eventInfo[3],eventInfo[4],eventInfo[5],eventInfo[6],eventInfo[7])
        elif settings.onComplete=="twitter":
            os.system('curl -u '+eventInfo[1]+':'+eventInfo[2]+' -d status="'+eventInfo[3]+'" http://twitter.com/statuses/update.xml')
            # or doHTTP("http://twitter.com/statuses/update.xml?status="+eventInfo[3],eventInfo[1],eventInfo[2])
        elif settings.onComplete=="ftp":
            fileAt=eventInfo[1].split("/")
            eventInfo[1]=fileAt[0]
            fileAt="/".join(fileAt[1:])
            doFTP(eventInfo[1],fileAt,eventInfo[2],eventInfo[3],eventInfo[4])
        elif settings.onComplete=="http":
            doHTTP(":".join(eventInfo[1:]))
        elif settings.onComplete=="exec":
            os.system(":".join(eventInfo[1:]))
        elif settings.onComplete=="python":
            eval(":".join(eventInfo[1:]),globals(),locals())
    else:
        for event in eventInfo:
            doCommonEvent(event,params)
