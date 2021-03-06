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

class CommandHelp(ICommand):
    __commandObject = None
    
    def __init__(self, commandObject):
        ICommand.__init__(self, "?")
        self.__commandObject = commandObject 
        
    def getHelp(self):
        helpMessage = "-- ? --\n"
        helpMessage += "usage: ? {command}\n"
        return helpMessage
        
    def execute(self):
        print "display help for: " + self.__commandObject._cmd
        self._response =  self.__commandObject.getHelp()
        
        