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
import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ft_cmd import ICommand

class CommandGet(ICommand):    
    def __init__(self, cmd):
        ICommand.__init__(self, cmd)
        
    def getHelp(self):
        helpMessage = "-- get --\n"
        helpMessage += "usage: get {full path of the file on the remote computer}\n"
        return helpMessage
        
    def execute(self):
        path = self._cmd[3:].strip()
        
        print "attach file: " + path        
        if not os.path.isfile(path):
            #reply.attach(MIMEText("File not found:\n"+path))
            self._response = self._cmd + "\nFile not found:\n" + path
            return
        
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(path)
            # Note: we should handle calculating the charset
            outMsg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(path, 'rb')
            outMsg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            outMsg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(path, 'rb')
            outMsg = MIMEBase(maintype, subtype)
            outMsg.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(outMsg)
        # Set the filename parameter
        filename = path[path.replace("\\", "/").rfind("/")+1:]
        outMsg.add_header('Content-Disposition', 'attachment', filename=filename)
        
        self._response = outMsg
        
    
        
        