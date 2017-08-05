import urllib2, urllib, cgi, re, sys
import HTMLParser
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urlresolver
import traceback

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.dramasonline'
selfAddon = xbmcaddon.Addon(id=addon_id)

DRAMAS_ONLINE_MAIN_URL = 'http://www.dramasonline.com/'
liveURL = 'http://www.zemtv.com/live-pakistani-news-channels/'

tabURL = 'http://www.eboundservices.com:8888/users/rex/m_live.php?app=%s&stream=%s'

MODE_LIST_SHOWS = 2
MODE_LIST_EPISODES = 3
MODE_LIST_SHOWS_HUM_TV = 12
MODE_LIST_EPISODES_HUM_TV = 13


def addLink(name, url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def Colored(text='', colorid='', isBold=False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid

    if isBold == True:
        text = '[B]' + text + '[/B]'

    return '[COLOR ' + color + ']' + text + '[/COLOR]'


def addDir(name, url, mode, iconimage, showContext=False, showLiveContext=False, isItFolder=True):
    #	print name
    #	name=name.decode('utf-8','replace')
    h = HTMLParser.HTMLParser()
    name = h.unescape(name.decode("utf8")).encode("ascii", "ignore")

    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True

    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})

    if showContext == True:
        cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
        cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
        cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
        liz.addContextMenuItems(
            [('Play Youtube video', cmd3), ('Play DailyMotion video', cmd1), ('Play Tune.pk video', cmd2)])

    if showLiveContext == True:
        cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
        cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
        liz.addContextMenuItems([('Play RTMP Steam (flash)', cmd1), ('Play Http Stream (ios)', cmd2)])

    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isItFolder)
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def show_channels():
    baseLink = 'http://dramaonline.com/%s-latest-dramas-episodes-online/'
    # 2 is series=3 are links
    addDir('All Recent Episodes', 'http://dramaonline.com/', 3, 'http://i.imgur.com/qSzxay9.png')  # links
    addDir('HumTv Shows', 'http://www.hum.tv/dramas/', MODE_LIST_SHOWS_HUM_TV,
           'http://i.imgur.com/SPbcdsI.png')
    addDir('GeoTv Shows', baseLink % 'geo-tv', MODE_LIST_SHOWS, 'http://i.imgur.com/YELzFHv.png')
    addDir('PTV Home Shows', baseLink % 'ptv-home', MODE_LIST_SHOWS, 'http://i.imgur.com/vJPo6xO.png')
    addDir('AryDigital Shows', baseLink % 'ary-digital-tv', MODE_LIST_SHOWS, 'http://i.imgur.com/Qpvx9N4.png')
    addDir('Hum Sitaray Shows', baseLink % 'hum-sitaray', MODE_LIST_SHOWS, 'http://i.imgur.com/GtoMqkd.png')
    addDir('Express Shows', baseLink % 'express-entertainment', MODE_LIST_SHOWS, 'http://i.imgur.com/RBlvLwp.png')
    addDir('APlus Shows', baseLink % 'aplus-entertainment', MODE_LIST_SHOWS, 'http://i.imgur.com/wynK0iI.png')
    addDir('Urdu1 Shows', baseLink % 'urdu-1', MODE_LIST_SHOWS, 'http://i.imgur.com/9i396WG.jpg')
    addDir('Ary Zindagi Shows', baseLink % 'ary-zindagi', MODE_LIST_SHOWS, 'http://i.imgur.com/a1PH1wk.png')
    addDir('TVOne Shows', 'http://dramaonline.com/pakistani-dramas-tvone-latest-dramas-episodes-online//', 2,
           'http://dramaonline.com/wp-content/themes/mts_newspaper/images/tvone.jpeg')
    addDir('SeeTV Shows', baseLink % '/pakistani-dramas-see-tv', MODE_LIST_SHOWS, 'http://i.imgur.com/BkJ1440.png')
    addDir('Teleplays', 'http://www.dramaonline.com/?cat=255', 3,
           'http://i.imgur.com/FhL5Yas.png')  # these are is links
    addDir('All Time Hits', 'http://dramaonline.com/watch-evergreen-famous-pakistani-dramas-of-all-time/', 2,
           'http://i.imgur.com/aFWO9Y7.png')  # top
    addDir('Popular Dramas', 'http://dramaonline.com//', 5, 'http://i.imgur.com/aFWO9Y7.png')  # top
    addDir('Search Drama', 'http://dramaonline.com/', 10, 'http://i.imgur.com/aFWO9Y7.png')  # top
    # addDir('Live Channels' ,'http://www.dramaonline.com/category/live-channels/' ,6,'') ##
    addDir('Settings', 'http://www.dramaonline.com/category/live-channels/', 8, '', isItFolder=False)  ##


def ShowSettings(Fromurl):
    selfAddon.openSettings()


def TakeInput(name, headname):
    print 'in take input'
    try:
        import xbmc
        kb = xbmc.Keyboard('default', 'heading', True)
        kb.setDefault(name)
        kb.setHeading(headname)
        kb.setHiddenInput(False)
        print 'loading text'
        kb.doModal()
        return kb.getText()
    except:
        traceback.print_exc(file=sys.stdout)


def SearchDramas(Fromurl):
    search = TakeInput(selfAddon.getSetting("searchkeyword"), 'Enter Drama name')
    if search == "": return
    print search
    selfAddon.setSetting("searchkeyword", search)
    url = 'http://dramaonline.com/?s=' + urllib.quote_plus(search)
    return list_entries_dramas_online(url)
    ## skip and call add entries
    link = get_html(url)
    import json
    jsdata = json.loads(link)

    for res in jsdata["results"]:

        item_name = res["title"]
        item_url = res["url"]

        if not '/category/' in item_url:
            addDir(item_name, item_url, 4, '')  # name, url, mode, icon
        else:
            addDir(item_name, item_url, 3, '')  # name, url, mode, icon


def list_series_dramas_online(source_url):
    link = get_html(source_url)

    pattern = re.compile(
        '<td><a (title=".*?"\s)*href="(?P<url>[^"]*)"[^>]*><img (class="[^"]*")*\s*(src="(?P<imgsrc1>[^"]*)"\salt="(?P<seriesname1>[^"]*)"|alt="(?P<seriesname2>[^"]*)"\ssrc="(?P<imgsrc2>[^"]*)")')

    _list_series_for_channel(source_url, pattern, MODE_LIST_EPISODES)

    match = re.findall('"nextLink":"(http.*?)"', link)
    # print link,'match',match
    if len(match) == 1:
        addDir('Next Page', match[0].replace('\\/', '/'), MODE_LIST_SHOWS, '')


def list_series_hum_tv(source_url):
    link = get_html(source_url)

    pattern = re.compile(
        '<div class="trending_single">\s*<a href="(?P<url>[^"]+)">\s*<figure>\s*<img src="(?P<imgsrc1>[^"]+)" .*>\s*<figcaption>\s*<p>(?P<seriesname1>.+)<\/p>'
    )

    _list_series_for_channel(source_url, pattern, MODE_LIST_EPISODES_HUM_TV)

    match = re.findall('"nextLink":"(http.*?)"', link)
    # print link,'match',match
    if len(match) == 1:
        addDir('Next Page', match[0].replace('\\/', '/'), MODE_LIST_SHOWS, '')


def _list_series_for_channel(source_url, pattern_for_series, mode_for_next_screen):
    html_source = get_html(source_url)

    for cname in pattern_for_series.finditer(html_source):
        named_groups_dict = cname.groupdict()

        alt_text = named_groups_dict['seriesname1'] or named_groups_dict['seriesname2']
        img_src = named_groups_dict['imgsrc1'] or named_groups_dict['imgsrc2']

        item_name = name_from_re = alt_text
        name_from_url = named_groups_dict['url'].rstrip('/').split('/')

        # get last part of url
        name_from_url = name_from_url[-1].replace('-', ' ')

        # print '%s - %s - %s' % (item_name, name_from_url, name_from_re)

        if (name_from_url.lower() != name_from_re.lower()):
            item_name = name_from_url

        item_name = item_name.replace('Watch ', '').replace('watch ', '').title()

        # print item_name, cname[groupUrl], cname[groupImage]
        addDir(item_name, named_groups_dict['url'], mode_for_next_screen, img_src)  # name, url, mode, icon


    match = re.findall('"nextLink":"(http.*?)"', html_source)
    # print link,'match',match
    if len(match) == 1:
        addDir('Next Page', match[0].replace('\\/', '/'), MODE_LIST_SHOWS, '')


def TopRatedDramas(Fromurl):
    link = get_html(Fromurl)

    regstring = '<li class="popular.*?>\s*?<a href="(.*?)" title="(.*?)"'
    match = re.findall(regstring, link, re.M | re.DOTALL)
    #	print Fromurl

    #	print match
    h = HTMLParser.HTMLParser()
    #	print 'match',match
    for cname in match:
        addDir(cname[1], cname[0], 3, '')  # url,name,jpg#name,url,mode,icon


def list_entries_dramas_online(source_url):
    print 'getting entries %s' % source_url

    pagenum = ''
    if 'admin-ajax.php' in source_url:
        source_url, pagenum = source_url.split('$page$=')
        post = {'action': 'mts_home_tabs_content', 'tab': '#latest-tab-content', 'page': pagenum}
        post = urllib.urlencode(post)
        html_content = get_html(source_url, post=post)
    else:
        html_content = get_html(source_url)

    pattern = re.compile(
        '<img width.*? src="(?P<imagesrc>.+?[^"])".*?\/>\s*<\/a><\/div><div class="postlisttitlewrap"><h5 class="postlisttitle"><a href="(?P<url>.+?[^"])".*?>(?P<episodetitle>.+?)<\/a>'
    )

    _list_entries(source_url, pattern)

    nextpageurl = ''
    if 'admin-ajax.php' in source_url:
        nextpageurl = 'http://dramaonline.com/wp-admin/admin-ajax.php$page$=' + str(int(pagenum) + 1)
    else:
        if 'class="paginate">' in html_content:
            match = re.findall("<a href='(.*?)' class=", html_content.split('class="paginate">')[1].split('div')[0])
            print 'next', match
            if len(match) > 0:
                nextpageurl = match[-1]
    if len(nextpageurl) > 0:
        addDir('Next Page', nextpageurl, 3, '')
        # print 'match', match


def list_entries_hum_tv(source_url):
    print 'getting entries %s' % source_url

    pattern = re.compile(
        '<div class="trending_single">\s*<a href="(?P<url>[^"]+)".*[^>]>\s*<figure>\s*<img src="(?P<imagesrc>[^"]+)" alt="(?P<episodetitle>[^"]+)"'
    )

    _list_entries(source_url, pattern)


def _list_entries(source_url, pattern_for_episode):
    html_source = get_html(source_url)

    for match in pattern_for_episode.finditer(html_source):
        named_groups_dict = match.groupdict()

        addDir(named_groups_dict['episodetitle'],  # title
               named_groups_dict['url'],  # url
               4,  # mode
               named_groups_dict['imagesrc'],  # image
               isItFolder=False)

def AddChannels(liveURL):
    link = get_html(liveURL)

    #	print link

    match = re.findall(
        '<div class="videopart">\s*<div class="paneleft">\s*<a.*?href="(.*?)".*?title="(.*?)".*?<img.*?src="(.*?)"',
        link, re.M)

    for cname in match:
        addDir(Colored(cname[1], 'ZM'), cname[0], 7, cname[2], False, True, isItFolder=False)  # name,url,mode,icon


def AddChannelsFromEbound():
    liveURL = 'http://eboundservices.com/istream_demo.php'

    link = get_html(liveURL)

    #	print link

    match = re.findall('<a href=".*?stream=(.*?)".*?src="(.*?)"', link, re.M)

    # print match
    expressExists = False
    expressCName = 'express'
    arynewsAdded = False

    for cname in match:
        addDir(Colored(cname[0].capitalize(), 'EB'), cname[0], 9, cname[1], False, True,
               isItFolder=False)  # name,url,mode,icon
        if cname[0] == expressCName:
            expressExists = True
        if cname[0] == 'arynews':
            arynewsAdded = True

    if not expressExists:
        addDir(Colored('Express Tv', 'EB'), 'express', 9, '', False, True, isItFolder=False)  # name,url,mode,icon
    if not arynewsAdded:
        addDir(Colored('Ary News', 'EB'), 'arynews', 9, '', False, True, isItFolder=False)  # name,url,mode,icon
        addDir(Colored('Ary Digital', 'EB'), 'aryentertainment', 9, '', False, True,
               isItFolder=False)  # name,url,mode,icon

    return


def Colored(text='', colorid='', isBold=False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid

    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'


def getPlaywireUrl(html, short):
    playURL = None
    newFormat = False

    try:
        match = re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', html)

        if len(match):
            playURL = match[0]

        else:
            # try new links
            str = '<script data-config="(http)?...?config.playwire.com.(\d+)\/videos.v2.(\d+)\/'
            match = re.findall(str, html)

            if len(match):
                newFormat = True
                playURL = match[len(match) - 1]

        print playURL
        if short:
            return playURL

        if playURL is None:
            return None

        if newFormat:
            (pp, PubId, videoID) = playURL

            cdnUrl = "http://config.playwire.com/%s/videos/v2/%s/manifest.f4m" % (PubId, videoID)
            link = get_html(cdnUrl)

            str = '<baseURL>\s*(.+)\s*</baseURL>\s*<media url="(.+)" bitrate'
            match = re.findall(str, link)[0]

            playURL = "%s/%s" % (match[0], match[1])

        else:
            (playWireVar, PubId, videoID) = playURL
            cdnUrl = "http://cdn.playwire.com/v2/%s/config/%s.json" % (PubId, videoID)
            link = get_html(cdnUrl)
            playURL = "http://cdn.playwire.com/%s/%s" % (PubId, re.findall('src":".*?mp4:(.*?)"', link)[0])

        print 'Final playURL: %s' % playURL
        return playURL

    except:
        traceback.print_exc(file=sys.stdout)
        return None


def getDailyMotionUrl(html, short):
    try:
        match = re.findall('src="(.*?(dailymotion).*?)"', html)
        playURL = match[0][0]
        print playURL
        if short:
            return playURL
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        return stream_url
    except:
        print 'Error fetching DailyMotion stream url'
        traceback.print_exc(file=sys.stdout)
        return None


def getYouTubeURL(html, short):
    try:
        print 'Trying to find Youtube Link >>'
        match = re.findall('youtu.*?(?<=(?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', html, re.IGNORECASE)
        if len(match) > 0:
            youtubeids = []
            for m in match:
                if m[2] not in youtubeids:
                    youtubeids.append(m[2])
            print youtubeids
            # print 'YoutubeURL>>>',match[2]
            playURL = ','.join(youtubeids)
            print playURL
            return 'youtube:' + playURL

    except:
        print 'Error fetching YouTube Stream URL>>'
        traceback.print_exc(file=sys.stdout)
        return None


def getTuneTvUrl(html, short):
    try:
        # Find the first match
        playURL = re.search('(tune.pk.*\/embed_player.php\?\s*?vid=(\d+).*?)"', html)
        print 'getTuneTvUrl: %s' % playURL
        if short:
            return playURL

        if playURL is None:
            return None

        print 'match: ' + playURL.group(1)

        playURL = 'http://embed.tune.pk/play/%s?autoplay=no&ssl=no' % playURL.group(2)
        print playURL

        link = get_html(playURL)
        pattern = 'file":"(.*?)"'
        match = re.findall(pattern, link)
        print 'match', match
        stream_url = match[0]
        print stream_url
        stream_url = stream_url.replace('\\/', '/')
        #		stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        return stream_url
    except:
        traceback.print_exc(file=sys.stdout)
        return None


def get_html(url, ref=None, post=None):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req, post)
    link = response.read()
    response.close()
    return link


def SelectUrl(html, url):
    try:
        available_source = []
        print 'selecting Url'
        mainUrl = getDailyMotionUrl(html, True)
        print 'selected Url: %s' % mainUrl

        if (mainUrl):
            available_source.append('Dailymotion Video')

        mainUrl = getTuneTvUrl(html, True)
        if (mainUrl):
            available_source.append('Tune Video')

        mainUrl = getPlaywireUrl(html, True)
        if (mainUrl):
            available_source.append('Playwire Video')
        mainUrl = getVidrailUrl(html, True)
        if mainUrl and len(mainUrl) > 0:
            available_source.append('Vidrail Video')

        mainUrl = getYouTubeURL(html, True)
        if mainUrl and len(mainUrl) > 0:
            available_source.append('Youtube Video')

        defaultlinks = ['Dailymotion Video', 'Tune Video', 'Playwire Video', 'Vidrail Video', 'Youtube Video']
        defaultLinkType = selfAddon.getSetting("DefaultVideoType")
        if defaultLinkType is None or defaultLinkType == '':
            defaultLinkType = '0'
        print defaultLinkType
        defaultLinkType = defaultlinks[int(defaultLinkType)]
        print defaultLinkType

        print 'available_source: %s' % available_source
        if len(available_source) > 0:
            return _play_from_available_sources(defaultLinkType, available_source, html)
        else:
            line1 = "No sources found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, 2000, __icon__))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        return None


def getVidrailUrl(html, short):
    playURL = None
    newFormat = False

    try:
        match = re.findall('src="(.*?(vidrail\.com).*?)"', html)

        if len(match) > 0:
            playURL = match[0]

        if short:
            return playURL

        if playURL is None:
            return None
        playURL = match[0][0]
        pat = '<source src="(.*?)"'
        link = get_html(playURL)
        playURL = re.findall(pat, link)
        if len(playURL) == 0:
            return None
        return playURL[0]

    except:
        traceback.print_exc(file=sys.stdout)
        return None


def _play_from_available_sources(defaultLinkType, available_source, html):
    index = 0
    if len(available_source) > 1:
        print 'defaultLinkType: %s' % defaultLinkType

        # if not defaultLinkType in available_source:
        # 	dialog = xbmcgui.Dialog()
        # 	index = dialog.select('Choose your source', available_source)
        # else:
        # 	index=available_source.index(defaultLinkType)

        # since the settings default is not being used, we will show the dialog for the source selection.
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose your source', available_source)

    if index > -1:
        linkType = available_source[index]
        line1 = "Finding links from " + linkType
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, 2000, __icon__))
        print 'linkType: %s' % linkType

        ret = None

        if 'Dailymotion Video' == linkType:
            ret = getDailyMotionUrl(html, False)
        elif 'Tune Video' == linkType:
            ret = getTuneTvUrl(html, False)
        elif 'Playwire Video' == linkType:
            ret = getPlaywireUrl(html, False)
        elif 'Vidrail Video' == linkType:
            ret = getVidrailUrl(html, False)
        elif 'Youtube Video' == linkType:
            ret = getYouTubeURL(html, False)
        if not ret and len(available_source) > 1:
            # try next available source
            available_source.remove(defaultLinkType)

            return _play_from_available_sources(available_source[0], available_source, html)

        return ret


def PlayShowLink(url):
    #	url = tabURL.replace('%s',channelName);
    line1 = "Finding links"
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, 1000, __icon__))

    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    #	print url
    urlToPlay = SelectUrl(link, url)

    print 'urlToPlay: %s' % urlToPlay

    if urlToPlay:
        if not urlToPlay.startswith('youtube:'):
            playlist = xbmc.PlayList(1)
            playlist.clear()
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
            listitem.setInfo("Video", {"Title": name})
            if '.mp4' in urlToPlay:
                listitem.setProperty('mimetype', 'video/mp4')
                listitem.setContentLookup(False)
            else:
                listitem.setProperty('mimetype', 'video/x-msvideo')
            listitem.setProperty('IsPlayable', 'true')
            playlist.add(urlToPlay, listitem)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playlist)
        else:
            playlist = None
            video_ids = urlToPlay.split('youtube:')[1].split(',')
            print 'video ids: %s' % video_ids

            playlist = xbmc.PlayList(1)
            playlist.clear()

            for youtubevid in video_ids:
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo("Video", {"Title": name})
                listitem.setProperty('mimetype', 'video/x-msvideo')
                listitem.setProperty('IsPlayable', 'true')
                uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubevid
                playlist.add(uurl, listitem)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playlist)

            # xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
    return


def PlayLiveLink(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update(10, "", "Finding links..", "")

    if mode == 7:
        req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.findall('"http.*(ebound).*?\?site=(.*?)"', link, re.IGNORECASE)[0]
        cName = match[1]
        progress.update(20, "", "Finding links..", "")

    else:
        cName = url
    # match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]



    newURL = 'http://www.eboundservices.com/iframe/newads/iframe.php?stream=' + cName + '&width=undefined&height=undefined&clip=' + cName
    print newURL

    req = urllib2.Request(newURL)
    req.add_header('User-Agent',
                   'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    progress.update(50, "", "Finding links..", "")


    #	match =re.findall('<iframe.+src=\'(.*)\' frame',link,  re.IGNORECASE)
    #	print match
    #	req = urllib2.Request(match[0])
    #	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    #	response = urllib2.urlopen(req)
    #	link=response.read()
    #	response.close()
    time = 2000  # in miliseconds
    defaultStreamType = 0  # 0 RTMP,1 HTTP
    defaultStreamType = selfAddon.getSetting("DefaultStreamType")
    print 'defaultStreamType', defaultStreamType
    if 1 == 2 and (linkType == "HTTP" or (
            linkType == "" and defaultStreamType == "1")):  # disable http streaming for time being
        #	print link
        line1 = "Playing Http Stream"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, time, __icon__))

        match = re.findall('MM_openBrWindow\(\'(.*)\',\'ebound\'', link, re.IGNORECASE)

        #	print url
        #	print match

        strval = match[0]

        # listitem = xbmcgui.ListItem(name)
        # listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
        # playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        # playlist.clear()
        # playlist.add (strval)

        # xbmc.Player().play(playlist)
        listitem = xbmcgui.ListItem(label=str(cName), iconImage="DefaultVideo.png",
                                    thumbnailImage=xbmc.getInfoImage("ListItem.Thumb"), path=strval)
        print "playing stream name: " + str(cName)
        listitem.setInfo(type="video", infoLabels={"Title": cName, "Path": strval})
        listitem.setInfo(type="video", infoLabels={"Title": cName, "Plot": cName, "TVShowTitle": cName})
        xbmc.Player().play(str(strval), listitem)
    else:
        line1 = "Playing RTMP Stream"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, line1, time, __icon__))
        progress.update(60, "", "Finding links..", "")

        post = {'username': 'hash'}
        post = urllib.urlencode(post)
        req = urllib2.Request('http://eboundservices.com/flashplayerhash/index.php')
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
        response = urllib2.urlopen(req, post)
        link = response.read()
        response.close()

        print link
        # match =re.findall("=(.*)", link)

        # print url
        # print match

        strval = link  # match[0]

        # listitem = xbmcgui.ListItem(name)
        # listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
        # playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        # playlist.clear()
        # playlist.add (strval)

        playfile = 'rtmp://cdn.ebound.tv/tv?wmsAuthSign=/%s app=tv?wmsAuthSign=?%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=&channel=%s&country=GB pageUrl=http://www.eboundservices.com/iframe/newads/iframe.php?stream=%s tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=?%s live=true timeout=15' % (
        cName, strval, cName, cName, strval)
        # playfile='rtmp://cdn.ebound.tv/tv?wmsAuthSign=/humtv app=tv?wmsAuthSign=?%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=&channel=humtv&country=GB pageUrl=http://www.eboundservices.com/iframe/newads/iframe.php?stream=humtv tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=?%s live=true'	% (strval,strval)
        progress.update(100, "", "Almost done..", "")
        print playfile
        # xbmc.Player().play(playlist)
        listitem = xbmcgui.ListItem(label=str(name), iconImage="DefaultVideo.png",
                                    thumbnailImage=xbmc.getInfoImage("ListItem.Thumb"))
        print "playing stream name: " + str(name)
        # listitem.setInfo( type="video", infoLabels={ "Title": name, "Path" : playfile } )
        # listitem.setInfo( type="video", infoLabels={ "Title": name, "Plot" : name, "TVShowTitle": name } )
        xbmc.Player().play(playfile, listitem)
        # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    return


# print "i am here"
params = get_params()
url = None
name = None
mode = None
linkType = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

args = cgi.parse_qs(sys.argv[2][1:])
linkType = ''
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print 'mode: %s' % mode

try:
    if mode == None or url == None or len(url) < 1:
        print "InAddTypes"
        show_channels()

    elif mode == MODE_LIST_SHOWS:
        print "List shows for channel '%s' from %s" % (name, url)
        list_series_dramas_online(url)

    elif mode == MODE_LIST_SHOWS_HUM_TV:
        print "List shows for channel '%s' from %s" % (name, url)
        list_series_hum_tv(url)

    elif mode == MODE_LIST_EPISODES:
        print "Ent url is " + url
        list_entries_dramas_online(url)

    elif mode == MODE_LIST_EPISODES_HUM_TV:
        print "Ent url is " + url
        list_entries_hum_tv(url)

    elif mode == 4:
        print "Play url is " + url
        PlayShowLink(url)

    elif mode == 5:
        print "TopRatedDramas url is " + url
        TopRatedDramas(url)
    elif mode == 6:
        print "Play url is " + url
        addDir(Colored('dramaonline Channels', 'ZM', True), 'ZEMTV', 10, '', False, True,
               isItFolder=False)  # name,url,mode,icon
        AddChannels(url)
        addDir(Colored('EboundServices Channels', 'EB', True), 'ZEMTV', 10, '', False, True,
               isItFolder=False)  # name,url,mode,icon
        AddChannelsFromEbound()
    elif mode == 7 or mode == 9:
        print "Play url is " + url, mode
        PlayLiveLink(url)
    elif mode == 8:
        print "Play url is " + url, mode
        ShowSettings(url)
    elif mode == 10:
        print "Play url is " + url, mode
        SearchDramas(url)

except Exception, ex:
    print ex
    print 'somethingwrong'

if not (mode == 7 or mode == 4 or mode == 9):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
