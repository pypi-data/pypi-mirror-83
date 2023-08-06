# GENOCIDE - the king of the netherlands commits genocide
#
# OTP-CR-117/19/001 otp.informationdesk@icc-cpi.int https://genocide.rtfd.io

from genocide import __version__, __txt2__

import ol
import bot.cmd

def ver(event):
    "show version (ver)"
    event.reply("GENOCIDE %s | BOTLIB %s | OLIB %s | %s" % (__version__, bot.cmd.__version__, ol.__version__, __txt2__))
