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
import poplib
import smtplib
import email
import time
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ft_mail import *
from ft_cmd import ICommand
from ft_cmd_factory import CommandFactory

class MailProcessor:
    __mailUtil = None
    __pollingPeriod = 15
    __users = []
    __currentUser = ""
    __factory = None
    
    def __init__(self, argv):
        # Display usage is not started with the proper arguments
        if len(argv) < 5:
            print "usage: ft_main.py pop_server pop_username pop_password smtp_server [polling_period]"
            quit()
            
        # The polling period in seconds
        if len(argv) > 5:
            self.__pollingPeriod = int(argv[5])
                           
        # Create an instance of the email utility.
        self.__mailUtil = MailUtil(argv[1], argv[2], argv[3], argv[4])
        
        self.loadUsers()
        
        self.__factory = CommandFactory(self)
        
    def loadUsers(self):
        print "Reading onfigurations ..."
        self.__users = list()
        file = open("./ft_users.config")
        lines = file.read().splitlines()
        for line in lines:
            tokens = line.split('=')
            if len(tokens[0]) > 0:
                self.__users.append([tokens[0], tokens[1]])
        file.close()
                
    def saveUsers(self):
        print "Writing onfigurations ..."
        file = open("./ft_users.config", "w")
        for u, p in self.__users:
            file.write("%s=%s\n" % (u,p))
        file.close()                
                
    def setPollingPeriod(self, period):
        print "Changing polling period to %d" % (int(period))
        self.__pollingPeriod = int(period)
        
    def changePassword(self, newPassword, newPasswordAgain):
        print "Changing password for user %s" % (self.__currentUser)
        
        for u, p in self.__users:
            u2 = "<"+u.strip().lower()+">"
            if self.__currentUser.strip().lower().find(u2) > -1:
                self.__users.remove([u,p])
                self.__users.append([u,newPassword])
                return True
            
        return False
        
    def checkPassword(self, password):
        for u, p in self.__users:
            u = "<"+u.strip().lower()+">"
            if self.__currentUser.strip().lower().find(u) > -1 and password.strip() == p.strip():
                return True
        
        return False
    
    def run(self):
        print "Ready."        
        while True:
            msg = self.__mailUtil.getTopMessage()
            if msg is None:
                time.sleep(self.__pollingPeriod)
                continue
            
            response = self.processMessage(msg)
            if response != None:
                self.__mailUtil.sendMessage(response)
                
#            self.__mailUtil.delTopMessage()
            quit()
            
            print "Ready."

    def processMessage(self, inMsg):
        try:
            startTime = time.time()
            
            print "processing message from: " + inMsg['From']
            
            payload = inMsg.get_payload()
            while isinstance(payload,list):
                payload = payload[0].get_payload()
                
            reply = MIMEMultipart()
            allAttachments = []
            allResponses = "FTPOPY reply to the following commands:\n\n%s" % (payload)
            
            # Check password
            self.__currentUser = inMsg['From']
            if self.checkPassword(inMsg['Subject']):  
                # This piece of code splits commands
                currentCommand = ""
                commandLines = []
                for line in payload.split('\n'):
                    if line.find("/") == 0:
                        currentCommand = currentCommand.replace("\n", "")
                        currentCommand = currentCommand.replace("\r", "")
                        currentCommand = currentCommand.replace("=20", "")
                        currentCommand = currentCommand.replace("=", "")
                        currentCommand = currentCommand.strip()                
                        commandLines.append(currentCommand)
                        currentCommand = ""
                    else:
                        currentCommand = currentCommand + line
                
                for line in commandLines:            
                    if len(line) == 0:
                        continue
                    
                    # The the command objects
                    command = self.__factory.getCommand(line, inMsg)
                    command.execute()
                    response = command.response()
                    
                    if isinstance(response, str) or isinstance(response, basestring):      
                        allResponses = allResponses + "\n\n->" + line + "\n" + response
                    else:
                        allAttachments.append(response)
            else:
                allResponses += "\n\nAccess denied.\n"
                allResponses += "Invalid email or password\n"    
        except:
            print "processMsg() failed!"
            raise 
            return None
        
        allResponses += "\n\n"
        allResponses += "Available commands are: \n? (help), \nGET (download a file), \nPUT (upload a file), \nFTPOP (ftpoPY server management) \n... and all commands supported by the remote shell.\n"
        allResponses += 'All commands must be separated by an empty line starting with /\n'
        allResponses += "\n"
        allResponses += "Visit the project website at http://www.basbrun.com/?ftpopy\n"
        
        #reply['Subject'] = "RE:" + inMsg["Subject"]
        reply['Subject'] = "RE: Executed on " + time.asctime()+ " in %8.2f seconds" % (time.time()-startTime) 
        reply['From'] = inMsg["To"]
        reply['To'] = inMsg["From"]
            
        reply.attach(MIMEText(allResponses))
        for attachment in allAttachments:
            reply.attach(attachment)
            
        return reply
        
        