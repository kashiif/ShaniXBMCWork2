import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer,uuid
from time import time
import base64
def tryplay(url,listitem):    
    import  CustomPlayer,time

    player = CustomPlayer.MyXBMCPlayer()
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    while player.is_active:
        xbmc.sleep(200)
        if player.urlplayed:
            print 'yes played'
            return True
        xbmc.sleep(1000)
    print 'not played',url
    return False
def play(listitem, item):
    played=False
    try:
        url=item[0]["http_stream"].split('|')[0]+"|User-Agent=UKTVNOW_PLAYER_1.2&Referer=www.uktvnow.net"
        played=tryplay(url,listitem)
        
    except: pass
    #print "playing stream name: " + str(name) 
    #xbmc.Player(  ).play( urlToPlay, listitem)    
    url=item[0]["rtmp_stream"].replace(' ','')
    if not played:
        tryplay(url,listitem)
        
        