# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"rich site syndicate"

import datetime
import html.parser
import ol
import os
import random
import re
import time
import urllib

from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

#:
debug = False

#;
timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
    "%d, %b %Y %H:%M:%S +0000"
]


def init(krn):
    "start a rss poller and return it"
    f = Fetcher()
    f.start()
    return f

class Cfg(ol.Cfg):

    "rss configuration"

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(ol.Default):

    "a feed item"

class Rss(ol.Object):

    "a rss feed url"

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(ol.Object):

    "all urls seen"

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(ol.Object):

    "rss feed poller"

    #:
    cfg = ol.Cfg()
    #:
    seen = Seen()

    def __init__(self):
        super().__init__()
        self._thrs = []

    def display(self, o):
        "display a rss feed item"
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = ol.get(o, key, None)
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            if data:
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = unescape(data)
                result += data.rstrip()
                result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        "update a rss feed"
        counter = 0
        objs = []
        if not rssobj.rss:
            return 0
        for o in reversed(list(get_feed(rssobj.rss))):
            if not o:
                continue
            f = Feed()
            ol.update(f, rssobj)
            ol.update(f, o)
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                ol.save(f)
        if objs:
            ol.save(Fetcher.seen)
        for o in objs:
            txt = self.display(o)
            for bot in ol.bus.bus:
                bot.announce(txt)
        return counter

    def run(self):
        "update all feeds"
        thrs = []
        for o in ol.dbs.all("mods.rss.Rss"):
            thrs.append(ol.tsk.launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        "start the rss poller"
        ol.dbs.last(Fetcher.cfg)
        ol.dbs.last(Fetcher.seen)
        if repeat:
            repeater = ol.tms.Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        "stop the rss poller"
        ol.save(self.seen)

#:
fetcher = Fetcher()

def get_feed(url):
    "return a feed by it's url"
    if debug:
        return [ol.Object(), ol.Object()]
    try:
        result = get_url(url)
    except (HTTPError, URLError):
        return [ol.Object(), ol.Object()]
    if gotparser:
        result = feedparser.parse(result.data)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        print("feedparser is missing")
        return [ol.Object(), ol.Object()]

def file_time(timestamp):
    s = str(datetime.datetime.fromtimestamp(timestamp))
    return s.replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def get_tinyurl(url):
    "return a corresponding timyurl"
    postarray = [
        ('submit', 'submit'),
        ('url', url),
        ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php', data=bytes(postdata, "UTF-8"))
    req.add_header('User-agent', useragent())
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()
    return []

def get_url(url):
    "return a http page"
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent())
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def strip_html(text):
    "strip html codes from a page"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def to_time(daystr):
    "convert a timestring to unix timestamp"
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
            break
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    return res

def unescape(text):
    "unescape html codes"
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)

def useragent():
    "return useragent"
    return 'Mozilla/5.0 (X11; Linux x86_64) GENOCIDE +http://github.com/bthate/genocide)'

def rem(event):
    "remove a rss feed"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for o in ol.dbs.find("mods.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        ol.save(o)
    event.reply("ok")

def dpl(event):
    "set keys to display"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for o in ol.dbs.find("mods.rss.Rss", {"rss": event.args[0]}):
        ol.edit(o, setter)
        ol.save(o)
    event.reply("ok")

def fed(event):
    "search through saved feed items"
    if not event.args:
        return
    match = event.args[0]
    nr = 0
    res = list(find("mods.rss.Feed", {"link": match}))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr,
                                                  o.title,
                                                  o.summary,
                                                  o.link))
        nr += 1
    if nr:
        return
    res = list(ol.dbs.find("mods.rss.Feed", {"title": match}))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1
    res = list(ol.dbs.find("mods.rss.Feed", {"summary": match}))
    for o in res:
        if match:
            event.reply("%s %s - %s - %s" % (nr, o.title, o.summary, o.link))
        nr += 1

def ftc(event):
    "manual run a fetch batch"
    res = []
    thrs = []
    fetchr = Fetcher()
    fetchr.start(False)
    thrs = fetchr.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rss(event):
    "add a feed"
    if not event.args:
        return
    url = event.args[0]
    res = list(ol.dbs.find("mods.rss.Rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    ol.save(o)
    event.reply("ok")
