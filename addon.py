import sys
import m3u8
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
import urlparse
import urllib
from bs4 import BeautifulSoup

baseurl = sys.argv[0]
addon_handle = int(sys.argv[1])
my_addon = xbmcaddon.Addon('plugin.video.rtbf')
args = urlparse.parse_qs(sys.argv[2][1:])
listing = []

xbmcplugin.setContent(addon_handle, 'songs')

# Channels
channels = [ { 'mainurl':'https://www.rtbf.be/auvio/chaine_la-une?id=1', 'liveurl':'' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_la-deux?id=2', 'liveurl':'https://rtbf.l3.freecaster.net/live/rtbf/geo/open/a48e7df3dbbd5d027427bca5e89201deda443f03/ladeux-audio_1=128000-video=200000.m3u8' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_la-trois?id=3', 'liveurl':'' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_la-premiere?id=17', 'liveurl':'http://lapremiere.ice.rtbf.be/lapremiere-64.aac' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_vivacite?id=10', 'liveurl':'http://vivacitebruxelles.ice.rtbf.be/vivabxl-64.aac' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_musiq-3?id=8', 'liveurl':'http://musiq3.ice.rtbf.be/musiq3-128.aac' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_classic-21?id=7', 'liveurl':'http://classic21.ice.rtbf.be/classic21-64.aac' },
		{ 'mainurl': 'https://www.rtbf.be/auvio/chaine_pure-fm?id=9' , 'liveurl':'http://purefm.ice.rtbf.be/purefm-64.aac' } ]

mode = args.get('mode', None)

# If nothing is passed to the addon, parse channels
if mode is None:
	for chanurl in channels:
		page = BeautifulSoup(requests.get(chanurl['mainurl']).text, 'html.parser')
		print 'Parsing channel metadata at ' + chanurl['mainurl']
		icon = page.find('img', attrs={'class':'img-responsive center-block'})['src']
		name = page.find('meta', attrs={'property':'og:title'})['content']
		descr = page.find('meta', attrs={'property':'og:description'})['content']
		li = xbmcgui.ListItem(name, iconImage = icon)
		li.setArt({'fanart':my_addon.getAddonInfo('fanart')})
		li.setInfo('video',{'plot':descr})
		url = baseurl + '?' + urllib.urlencode({'mode':'folder', 'chanurl':chanurl['mainurl'], 'liveurl':chanurl['liveurl']})
		xbmcplugin.addDirectoryItem(handle = addon_handle, url = url, listitem = li, isFolder = True)

# If something is passed to the addon, channel has been specified.
elif mode[0] == 'folder':
	print 'Parsing channel at ' + args['chanurl'][0]
	page = BeautifulSoup(requests.get(args['chanurl'][0]).text, 'html.parser')

	# If channel is one of known, add live streaming.
	if args['liveurl'][0] != '':
		liveinfo = page.find('article', attrs={'class':'js-channel-live'}).find('figure')
		image = liveinfo.find('div', attrs={'class':'www-img-16by9'}).find('img')['data-srcset'].split(',')[-1].split()[0]
		title = liveinfo.find('figcaption').string
		list_item = xbmcgui.ListItem(label = 'EN DIRECT: ' + title, thumbnailImage = image)
		list_item.setArt({'fanart':my_addon.getAddonInfo('fanart')})
		listing.append((args['liveurl'][0], list_item, False))

	vidlist = page.find('section', attrs={'data-analytics-event-category':'Channel Catchup'}).find_all('a', attrs={'class':'www-faux-link'})
	for vid in vidlist:
		print 'Adding media at ' + vid['href']
		vidpage = BeautifulSoup(requests.get(vid['href']).text, 'html.parser')
		title = vidpage.find('meta', attrs={'property':'og:title'})['content']
		image = vidpage.find('meta', attrs={'property':'og:image'})['content']
		descr = vidpage.find('meta', attrs={'property':'og:description'})['content']
		if vidpage.find('meta', attrs={'itemprop':'contentURL'}) == None:
			media = vidpage.find('meta', attrs={'property':'og:audio'})['content']
		else:
			media = vidpage.find('meta', attrs={'itemprop':'contentURL'})['content']

		list_item = xbmcgui.ListItem(label = title, thumbnailImage = image)
		list_item.setArt({'fanart':my_addon.getAddonInfo('fanart')})
		list_item.setInfo('video', {'plot':descr})
		listing.append((media, list_item, False))

	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))

xbmcplugin.endOfDirectory(addon_handle)
# Radio
# purefm_url = 'http://purefm.ice.rtbf.be/purefm-64.aac'
# lapremiere_url = 'http://lapremiere.ice.rtbf.be/lapremiere-64.aac'
# viva_url = 'http://vivacitebruxelles.ice.rtbf.be/vivabxl-64.aac'
