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



def showWelcome():
	path = os.path.join(xbmc.translatePath(ROOT_PATH + '/resources'), 'welcome.html')
	text = readfile(path)
	TextBox().show('Welcome new user!', text)

def removeYear(s, regex='( \(\d{4}\))$'):
	has_year = re.search(regex, s)
	if has_year:
		s = s[0:len(s)-7]
	s = htmlcleaner.clean(s,strip=True)
	s = s.strip()
	return s
	
def DoSearch(msg):
	kb = xbmc.Keyboard('', msg, False)
    	kb.doModal()
	if (kb.isConfirmed()):
        	search = kb.getText()
        	if search != '':
			return search
		else:
			return False


def CreateDirectory(dir_path):
	dir_path = dir_path.strip()
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

def RemoveDirectory(dir):
	dialog = xbmcgui.Dialog()
	if dialog.yesno("Remove directory", "Do you want to remove directory?", dir):
		if os.path.exists(dir):
			pDialog = xbmcgui.DialogProgress()
			pDialog.create(' Removing directory...')
			pDialog.update(0, dir)	
			shutil.rmtree(dir)
			pDialog.close()
			Notification("Directory removed", dir)
		else:
			Notification("Directory not found", "Can't delete what does not exist.")	
	



def CleanFileName(s, remove_year=True, use_encoding = False, use_blanks = True):
		if remove_year:
			s=removeYear(s)
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

def sys_exit():
	exit = xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	return exit

def Notify(title, message, image=''):
	if image == '':
		image = xbmcpath(rootpath, 'icon.png')
	xbmc.executebuiltin("XBMC.Notification("+title+","+message+", 1000, "+image+")")

def xbmcpath(path,filename):
     translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
     return translatedpath

def showQuote(msg=''):
	filepath = xbmcpath(rootpath+'/resources/', 'quotes.txt')
	f = open(filepath)
	lines = f.readlines(100)
	n= random.randint(0, len(lines)-1)
	quote = lines[n]
	dialog = xbmcgui.Dialog()
	dialog.ok(msg, quote)


def htmldecode(body):
	h = HTMLParser.HTMLParser()
	body = h.unescape(body)
	try:
	    encoding = req.headers['content-type'].split('charset=')[-1]
	except:
	    enc_regex = re.search('<meta.+?charset=(.+?)" />')
	    encoding = enc_regex.group(1)
	body = unicode(body, encoding).encode('utf-8')
	return body



def ClearDatabaseLock():
	dialog = xbmcgui.Dialog()
	if dialog.yesno("Clear Database Lock?", "If a job has failed, you may manually delete the database lock.", "Do you want to proceed?"):
		DB.connect()
		DB.execute("UPDATE rw_status SET updating=0, job=''")
		DB.commit()	
