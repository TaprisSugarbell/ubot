
import logging
import requests
from bs4 import BeautifulSoup
from helper.utils import ytdl

logging.basicConfig(filename="sayu.log", level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@ytdl
def mediafire(url, out, custom=""):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    dwnld = soup.find(id='downloadButton')
    w = dwnld.get('href')
    return {"url": w,
            "out": out,
            "custom": custom,
            "ext": ""}


@ytdl
def generic(url, out, custom=""):
    return {"url": url,
            "out": out,
            "custom": custom,
            "ext": ""}
