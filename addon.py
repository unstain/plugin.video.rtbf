import sys
import m3u8
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'songs')

# Radio
purefm_url = 'http://purefm.ice.rtbf.be/purefm-64.aac'
lapremiere_url = 'http://lapremiere.ice.rtbf.be/lapremiere-64.aac'
viva_url = 'http://vivacitebruxelles.ice.rtbf.be/vivabxl-64.aac'

purefm_li     = xbmcgui.ListItem(label = 'PureFM', thumbnailImage = './assets/purefm.png')
lapremiere_li = xbmcgui.ListItem(label = 'La Premiere', thumbnailImage = './assets/lapremiere.png')
viva_li       = xbmcgui.ListItem(label = 'Vivacite', thumbnailImage = './assets/viva.png')


if not xbmcplugin.addDirectoryItem(handle = addon_handle, url = purefm_url, listitem = purefm_li):
	print 'Failed to add PureFM !'

if not xbmcplugin.addDirectoryItem(handle = addon_handle, url = lapremiere_url, listitem = lapremiere_li):
	print 'Failed to add La Premiere !'

if not xbmcplugin.addDirectoryItem(handle = addon_handle, url = viva_url, listitem = viva_li):
	print 'Failed to add Vivacite !'

emissions = [ 'https://www.rtbf.be/auvio/emissions/detail_le-12-minutes?id=9',
	  'https://www.rtbf.be/auvio/emissions/detail_le-15-minutes?id=2863',
	  'https://www.rtbf.be/auvio/emissions/detail_journal-televise-13h?id=4',
	  'https://www.rtbf.be/auvio/emissions/detail_journal-televise-19h30?id=5' ]

# Scrape each URL for video information

listing = []
for vurl in emissions:
	page = BeautifulSoup(requests.get(vurl).text, 'html.parser')
	# For each URL...
	print 'Parsing page ' + vurl

	title = page.find('meta', attrs={'property':'og:title'})['content']
	image = page.find('meta', attrs={'property':'og:image'})['content']
	descr = page.find('meta', attrs={'property':'og:description'})['content']
	video = page.find('meta', attrs={'itemprop':'contentURL'})['content']

	list_item = xbmcgui.ListItem(label = title, thumbnailImage = image)
	listing.append((video, list_item, False))

xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))

xbmcplugin.endOfDirectory(addon_handle)
