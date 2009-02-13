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

from ft_cmd import *

class CommandFtpop(ICommand):
    __commandObject = None
    __processor = None
    
    def __init__(self, cmd, processor):
        self.__processor = processor
        ICommand.__init__(self, cmd[5:].strip()) 
        
    def getHelp(self):
        helpMessage = "-- ftpop --\n"
        helpMessage += "usage:"
        helpMessage += "ftpop period {period in seconds}\n"
        helpMessage += "ftpop password {new password} {new password again}\n"
        helpMessage += "ftpop reload\n"
        return helpMessage
        
    def execute(self):
        if self._cmd.lower().find("period") == 0:
            tokens = self._cmd.split(" ")
            if len(tokens) < 2:
                return "ftpop period requires an argument, the period in seconds."
            
            # Change the period here ...
            try:
                self.__processor.setPollingPeriod(int(tokens[1]))
                self._response = "Polling period changed successfully"
            except:
                self._response = "Failed to change the polling period"
            
            return
        
        if self._cmd.lower().find("password") == 0:
            tokens = self._cmd.split(" ")
            if len(tokens) < 3:
                return "ftpop passwords requires two arguments, the new password and a confirmation of the password."
            
            # Change the passwords here
            try:
                if tokens[1] != tokens[2]:
                    self._response = "The two passwords received are not the same"
                    return
                
                if self.__processor.changePassword(tokens[1], tokens[2]):
                    self.__processor.saveUsers()
                    self._response = "Change password succeeded"
                    return
            except:
                None
                
            self._response = "Failed to change password"
            
        if self._cmd.lower().find("reload") == 0:
            
            # Reload the config here
            try:                
                self.__processor.loadUsers()
                self._response = "Users loaded successfully"
            except:
                self._response = "Failed to load users"
                None
            
            return
        
        self._response = "Unknown command %s" % (self._cmd)
        
        