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

class MailUtil:
    __popServername = ""
    __popUsername = ""
    __popPassword = ""
    __smtpServername = ""
    
    __popServer = None
    __smtpServer = None
    
    def __init__(self, popserver, popuser, poppassword, smtpserver):
        self.__popServername = popserver
        self.__popUsername = popuser
        self.__popPassword = poppassword
        self.__smtpServername = smtpserver
        
    def getTopMessage(self):
        msg = None
                
        # Connect to the pop server
        self.__popServer = poplib.POP3(self.__popServername)
        self.__popServer.user(self.__popUsername)
        self.__popServer.pass_(self.__popPassword)
        
        #Get the number of messages in the mailbox
        numMessages = len(self.__popServer.list()[1])
        if numMessages == 0:
            return msg
        
        emailContent = ""
        for s in self.__popServer.retr(1)[1]:
            emailContent += s
            emailContent += "\n"
            
        msg = email.message_from_string(emailContent)
        self.__popServer.quit()
        
        return msg
    
    def delTopMessage(self):
        # Connect to the pop server
        self.__popServer = poplib.POP3(self.__popServername)
        self.__popServer.user(self.__popUsername)
        self.__popServer.pass_(self.__popPassword)
        
        #Get the number of messages in the mailbox
        numMessages = len(self.__popServer.list()[1])
        if numMessages > 0:
            self.__popServer.dele(1)
            
        self.__popServer.quit()
            
    def sendMessage(self, msg):
        
        print "return response to: " + msg['To']
        self.__smtpServer = smtplib.SMTP(self.__smtpServername)
#        self.__smtpServer.set_debuglevel(1)        

        self.__smtpServer.sendmail(msg['From'], msg['To'], msg.as_string())
        self.__smtpServer.quit()

        
        