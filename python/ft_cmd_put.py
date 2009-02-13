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

import base64
from ft_cmd import ICommand

class CommandPut(ICommand):
    __message = None

    def __init__(self, cmd, msg):
        ICommand.__init__(self, cmd)
        self.__message = msg
        
    def execute(self):
        print self._cmd
        tokens = self._cmd.split(" ", 2) #asuming filename with no spaces
        for part in self.__message.walk():
            filename = part.get_param("name")
            if filename is not None:
                if filename != tokens[1]:
                    continue
                
                print "file " + filename + " found"
                path = tokens[2].strip()
                if len(path) == 0:
                    path = "."
                if path[-1] != "/" and path[-1] != "\\":
                    path += "/"
                    
                payload = part.get_payload()
                if part.get_content_type().find("text/") == 0:
                    file = open(path+filename, "w")
                    file.write(payload)
                    file.close()
                else:
                    data = base64.decodestring(payload)
                    file = open(path+filename, "wb")
                    file.write(data)
                    file.close()
                    
                self._response = "File " + filename + " uploaded successfully"
                return
            
        self._response = "File " + filename + " upload failed"
                
        
    def getHelp(self):
        helpMessage = "-- put --\n"
        helpMessage += "Not yet implemented\n"
        return helpMessage
        