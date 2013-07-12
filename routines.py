import sys
import os
import re
import xbmc, xbmcgui, xbmcaddon
from t0mm0.common.addon import Addon
from donnie import htmlcleaner
ADDON_NAME = 'The Royal We'
ADDON_ID = 'plugin.video.theroyalwe'
ADDON = xbmcaddon.Addon(id=ADDON_ID)
ROOT_PATH = ADDON.getAddonInfo('path')
VERSION = ADDON.getAddonInfo('version')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/' + ADDON_ID), '')

class TextBox:
	# constants
	WINDOW = 10147
	CONTROL_LABEL = 1
	CONTROL_TEXTBOX = 5

	def __init__( self, *args, **kwargs):
		# activate the text viewer window
		xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
		# get window
		self.window = xbmcgui.Window( self.WINDOW )
		# give window time to initialize
		xbmc.sleep( 500 )


	def setControls( self ):
		#get header, text
		heading, text = self.message
		# set heading
		self.window.getControl( self.CONTROL_LABEL ).setLabel( "%s - %s v%s" % ( heading, ADDON_NAME, VERSION) )
		# set text
		self.window.getControl( self.CONTROL_TEXTBOX ).setText( text )

   	def show(self, heading, text):
		# set controls

		self.message = heading, text
		self.setControls()

def readfile(path, soup=False):
	try:
		file = open(path, 'r')
		content=file.read()
		file.close()
		if soup:
			soup = BeautifulSoup(content)
			return soup
		else:
			return content
	except:
		return ''

def writefile(path, content):
	try:
		file = open(path, 'w')
		file.write(content)
		file.close()
		return True
	except:
		return False

def showWelcome():
	path = os.path.join(xbmc.translatePath(ROOT_PATH + '/resources'), 'welcome.html')
	text = readfile(path)
	TextBox().show('Welcome new user!', text)

def CleanFileName(s, remove_year=True, use_encoding = False, use_blanks = True):
		has_year = re.search('( \(\d{4}\))$', s)
		if remove_year and has_year:
			s = s[0:len(s)-7]
		s = htmlcleaner.clean(s,strip=True)
		s = s.strip()
		if use_encoding:
			s = s.replace('"', '%22')
			s = s.replace('*', '%2A')
			s = s.replace('/', '%2F')
			s = s.replace(':', ',')
			s = s.replace('<', '%3C')
			s = s.replace('>', '%3E')
			s = s.replace('?', '%3F')
			s = s.replace('\\', '%5C')
			s = s.replace('|', '%7C')
			s = s.replace('&frac12;', '%BD')
			s = s.replace('&#xBD;', '%BD') #half character
			s = s.replace('&#xB3;', '%B3')
			s = s.replace('&#xB0;', '%B0') #degree character		
		if use_blanks:
			s = s.replace('"', ' ')
			s = s.replace('*', ' ')
			s = s.replace('/', ' ')
			s = s.replace(':', ' ')
			s = s.replace('<', ' ')
			s = s.replace('>', ' ')
			s = s.replace('?', ' ')
			s = s.replace('\\', ' ')
			s = s.replace('|', ' ')
			s = s.replace('&frac12;', ' ')
			s = s.replace('&#xBD;', ' ') #half character
			s = s.replace('&#xB3;', ' ')
			s = s.replace('&#xB0;', ' ') #degree character
		return s	
