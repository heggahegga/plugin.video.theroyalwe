import sys
import os
import re
import shutil
import xbmc, xbmcgui, xbmcaddon
from t0mm0.common.addon import Addon
from donnie import htmlcleaner
import HTMLParser
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
ADDON_NAME = 'The Royal We'
ADDON_ID = 'plugin.video.theroyalwe'
ADDON = xbmcaddon.Addon(id=ADDON_ID)
ROOT_PATH = ADDON.getAddonInfo('path')
VERSION = ADDON.getAddonInfo('version')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/' + ADDON_ID), '')

	
