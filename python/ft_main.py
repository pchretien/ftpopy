## ftpoPy ##
#
# This program allows a user to take control of a remote computer using email.
# The following code is the server part of the application. The client part is
# not part of this project. Any email client can be used.  
# Copyright (C) 2008,2009  Philippe Chretien
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License Version 2
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# You will find the latest version of this code at the following address:
# http://github.com/pchretien
#
# You can contact me at the following email address:
# philippe.chretien@gmail.com

import os
import sys
import poplib
import smtplib
import email
import time

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ft_cmd import ICommand
from ft_cmd_factory import CommandFactory

if len(sys.argv) < 5:
    print "usage: ft_main.py pop_server pop_username pop_password smtp_server [polling_period]"
    
# POP3 server to receive messages from ...
popServer = sys.argv[1]
popUsername = sys.argv[2]
popPassword = sys.argv[3]

# SMTP server to send emails
smtpServer = sys.argv[4]

period = 15 # seconds
if len(sys.argv) > 5:
    period = int(sys.argv[5])

def returnResponse(msg, reply):
    global smtpServer
    
    # Replace with the SMTP call or other ways of returning the response
    #reply = MIMEText(response)
    reply['Subject'] = "RE:" + msg["Subject"]
    reply['From'] = msg["To"]
    reply['To'] = msg["From"]
        
    server = smtplib.SMTP(smtpServer)
    server.set_debuglevel(1)
    
    # To and From reversed for the reply
    server.sendmail(msg["To"], msg["From"], reply.as_string())
    server.quit()

def processMsg(inMsg):
    try:
        payload = inMsg.get_payload()
        if isinstance(payload,list):
            payload = payload[0].get_payload()
            
        reply = MIMEMultipart()
        allAttachments = []
        allResponses = "FTPOPY reply to the following commands:\n\n%s" % (payload)
        
        # This piece of code should split commands
        currentCommand = ""
        commandLines = []
        for line in payload.split('\n'):
            if line.find("/") == 0:
                currentCommand = currentCommand.replace("\n", "")
                currentCommand = currentCommand.replace("\r", "")
                currentCommand = currentCommand.strip()                
                commandLines.append(currentCommand)
                currentCommand = ""
            else:
                currentCommand = currentCommand + line
        
        for line in commandLines:            
            if len(line) == 0:
                continue
            
            # The the command objects
            command = CommandFactory().getCommand(line)
            command.execute()
            response = command.response()
            
            if isinstance(response, str) or isinstance(response, basestring):      
                allResponses = allResponses + "\n\n->" + line + "\n" + response
            else:
                allAttachments.append(response)
            
    except:
        print "processMsg() failed!"
        raise 
        return False
    
    reply.attach(MIMEText(allResponses))
    for attachment in allAttachments:
        reply.attach(attachment)
        
    returnResponse(inMsg, reply)
    return True
                   
while True:
    print "reading e-mails ..."
    
    M = poplib.POP3(popServer)
    M.user(popUsername)
    M.pass_(popPassword)
    numMessages = len(M.list()[1])
    for i in range(numMessages):
        emailContent = ""
        for s in M.retr(i+1)[1]:
            emailContent += s
            emailContent += "\n"
        
        msg = email.message_from_string(emailContent)
        if processMsg(msg):
            M.dele(i+1)
       
    print "Done."
    M.quit()    
    time.sleep(period)
    
