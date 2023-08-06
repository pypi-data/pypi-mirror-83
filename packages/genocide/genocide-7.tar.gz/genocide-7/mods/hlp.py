# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"manual"

def help():
    print("GENOCIDE(8)                    System Administration                 GENOCIDE(8)")
    print("")
    print("NAME")
    print("        genocide - the king of the netherlands commits genocide")
    print("")
    print("SYNOPSIS")
    print("""        GENOCIDE is a pure python3 IRC chat bot that can run as a background
        daemon for 24/7 a day presence in a IRC channel. It installs itself
        as a service so you can get it restarted on reboot. You can use it
        to display RSS feeds, act as a UDP to IRC gateway, program your own
        commands for it, have it log objects on disk and search them and scan
        emails for correspondence analysis. GENOCIDE uses a JSON in file
        database with a versioned readonly storage. It reconstructs objects
        based on type information in the path and uses a "dump OOP and use 
        OP" programming library where the methods are factored out into
        functions that use the object as the first argument. GENOCIDE is
        placed in the Public Domain and has no COPYRIGHT or LICENSE.

        GENOCIDE also provides information on the genocide the king of the
        netherlands is doing. See https://pypi.org/project/genocide/ 

        GENOCIDE needs root, it lowers it's permission to the genocide user.
        /var/lib/genocide is used as the working directory, any logging is 
        in /var/log/syslog.
        """)
    print("")
    print("USAGE")
    print("        genocide cmd [mods=mod1,mod2] [-b] [-d] [-h] [-s] [-v]")
    print("")
    print("OPTIONS")
    print("        -s 		start a shell")
    print("        -d		start a background daemon")
    print("        -b		display a banner")
    print("        -v		be verbose")
    print("        -h		print this message")
    print("")
    print("        mods= let's you starts modules on boot, possbile modules to")
    print("        load are: irc,rss,udp")
    print("")
    print("EXAMPLES")
    print("        # show list of commands")
    print("        $ sudo genocide cmd")
    print("        cfg,cmd,cor,dne,dpl,fed,fnd,ftc,log,mbx,rem,req,rss,sts,tdo,")
    print("        trt,tsk,upt,ver,wsd")
    print("")
    print("        # configure the irc client")
    print("        $ sudo genocide cfg server=irc.freenode.net channel=\\#dunkbots")
    print("         nick=genocide2")
    print("        channel=#dunkbots nick=genocide2 port=6667 server=irc.freenode.net")
    print("")
    print("        # start the irc client with rss fetcher and udp<->irc gateway running")
    print("        $ sudo genocide mods=irc,rss,udp -d")
    print("")
