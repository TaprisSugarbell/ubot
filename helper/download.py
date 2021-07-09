import logging
import urllib.request
from helper.extractors import *

logging.basicConfig(filename="sayu.log", level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def download_file(urli, out="./", custom=""):
    dwn = ""
    host = urllib.request.Request(urli).host
    host2 = ".".join(host.split(".")[1:])
    if host == "www.mediafire.com" or host == "mediafire.com":
        dwn = mediafire(urli, out, custom)
    else:
        dwn = generic(urli, out, custom)
    return dwn
