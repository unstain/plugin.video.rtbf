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
args = urlparse.parse_qs(sys.argv[2][1:])
listing = []

xbmcplugin.setContent(addon_handle, 'songs')

# Channels
channels = [ 'https://www.rtbf.be/auvio/chaine_la-une?id=1',
		'https://www.rtbf.be/auvio/chaine_la-deux?id=2',
		'https://www.rtbf.be/auvio/chaine_la-trois?id=3',
		'https://www.rtbf.be/auvio/chaine_la-premiere?id=17',
		'https://www.rtbf.be/auvio/chaine_vivacite?id=10',
		'https://www.rtbf.be/auvio/chaine_musiq-3?id=8', 
		'https://www.rtbf.be/auvio/chaine_classic-21?id=7',
		'https://www.rtbf.be/auvio/chaine_pure-fm?id=9' ]

mode = args.get('mode', None)

# If nothing is passed to the addon, parse channels
if mode is None:
	for chanurl in channels:
		page = BeautifulSoup(requests.get(chanurl).text, 'html.parser')
		print 'Parsing channel metadata at ' + chanurl
		icon = page.find('img', attrs={'class':'img-responsive center-block'})['src']
		name = page.find('meta', attrs={'property':'og:title'})['content']
		li = xbmcgui.ListItem(name, iconImage = icon)
		url = baseurl + '?' + urllib.urlencode({'mode':'folder', 'chanurl':chanurl})
		xbmcplugin.addDirectoryItem(handle = addon_handle, url = url, listitem = li, isFolder = True)

# If something is passed to the addon, channel has been specified.
elif mode[0] == 'folder':
	page = BeautifulSoup(requests.get(args['chanurl'][0]).text, 'html.parser')
	print 'Parsing channel at ' + args['chanurl'][0]
	# If channel is one of known, add live streaming.
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
		list_item.setInfo('video', {'tagline':descr})
		listing.append((media, list_item, False))

	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))

xbmcplugin.endOfDirectory(addon_handle)
# Radio
# purefm_url = 'http://purefm.ice.rtbf.be/purefm-64.aac'
# lapremiere_url = 'http://lapremiere.ice.rtbf.be/lapremiere-64.aac'
# viva_url = 'http://vivacitebruxelles.ice.rtbf.be/vivabxl-64.aac'
