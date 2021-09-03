import xbmc
import time
import xbmcaddon
import xbmcgui
import xbmcplugin
from common import GLOBAL_SETUP  #Needed first to setup import locations

pos = 0
file = ''
count = 0 
pacount = 0

xbmc.log("Autostop addon service started." , xbmc.LOGINFO)

def settings(setting, value = None):
    # Get or add addon setting
    if value:
        xbmcaddon.Addon().setSetting(setting, value)
    else:
        return xbmcaddon.Addon().getSetting(setting)
  
class XBMCPlayer(xbmc.Player):
    
    def __init__(self, *args):
        self.paflag = 0
        pass
 
    def onPlayBackStarted(self):
        file = xbmc.Player().getPlayingFile()
        self.paflag = 0
 
    def onPlayBackPaused(self):
        xbmc.log("Autostop playback paused" , xbmc.LOGDEBUG)
        self.paflag = 1
 
    def onPlayBackResumed(self):
        file = self.getPlayingFile()
        xbmc.log("Autostop playback resumed" , xbmc.LOGDEBUG)
        self.paflag = 0
 
    def onPlayBackEnded(self):
        xbmc.log("Autostop playback ended" , xbmc.LOGDEBUG)
        pos = 0
        self.paflag = 0
 
    def onPlayBackStopped(self):
        self.paflag = 0

             
player = XBMCPlayer()
 
monitor = xbmc.Monitor()      
 
while True:

    pacount += 1 
    if pacount % 30 == 0:                          # Check for paused video every 30 seconds
        pastoptime = int(settings('pastop'))
        xbmc.log('Autostop count and stop time ' + str(pacount) + ' ' + str(pastoptime) +    \
        ' ' + str(player.paflag), xbmc.LOGDEBUG)
        if pastoptime > 0 and pacount >= pastoptime * 60 and player.paflag == 1:
            ptag = xbmc.Player().getVideoInfoTag()
            ptitle = ptag.getTitle()
            pos = xbmc.Player().getTime()
            xbmc.Player().stop()
            pacount = 0
            mgenlog ='Autostop stopped paused playback: ' + ptitle +     \
            ' at: ' + time.strftime("%H:%M:%S", time.gmtime(pos))
            xbmc.log(mgenlog, xbmc.LOGINFO)
            if settings('screensaver') == 'true':  #  Active screensaver if option selected
                xbmc.executebuiltin('ActivateScreensaver')
        elif player.paflag == 0:
            pacount = 0


    if monitor.waitForAbort(1): # Sleep/wait for abort for 1 second.
        xbmc.log("Autostop addon service stopped." , xbmc.LOGINFO)
            
        break # Abort was requested while waiting. Exit the while loop.

