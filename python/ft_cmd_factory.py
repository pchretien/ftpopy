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

from ft_cmd_get import CommandGet
from ft_cmd_put import CommandPut
from ft_cmd_shell import CommandShell
from ft_cmd_help import CommandHelp
from ft_cmd_ftpop import CommandFtpop 

class CommandFactory:
    __processor = None
    
    def __init__(self, processor):
        self.__processor = processor
    
    def getCommand(self, cmd, msg):
        global uniqueProcessor
            
        if cmd.lower().strip().find("get") == 0:
            return CommandGet(cmd)
        elif cmd.lower().strip().find("put") == 0:
            return CommandPut(cmd, msg)
        elif cmd.lower().strip().find("ftpop") == 0:
            return CommandFtpop(cmd, self.__processor)
        elif cmd.lower().strip().find("?") == 0:
            return CommandHelp( self.getCommand(cmd[1:].strip(), msg))
        else:
            return CommandShell(cmd)
            