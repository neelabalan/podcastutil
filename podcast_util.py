import logging
import json
import feedparser
from xml.etree import ElementTree

logging.basicConfig( format='%(levelname)s:%(message)s',filename='podcastlogs.log', level=logging.DEBUG )

class PodcastUtil( object ):
    def __init__( self, filename = 'podcasts.opml' ):
        self.filename = filename

    def extract_url_from_opml( self ):
        ''' extract url from opml file '''
        urls = list() 
        with open( self.filename, 'rt' ) as file:
            tree = ElementTree.parse( file )
        for node in tree.findall( './/outline' ):
            url = node.attrib.get( 'xmlUrl' )
            if url:
                urls.append( url )
        logging.info( 'urls extracted from {} - {}'.format( self.filename, urls ))
        return urls

    def get_feeds( self ):
        ''' returns a list of feeds from all urls '''
        urls = self.extract_url_from_opml()
        feeds = list()
        for url in urls:
            feed = feedparser.parse( url )
            if feed.status == 200:
                feeds.append( feedparser.parse( url ))
                logging.info( 'url parsed - {}'.format( url ) )
            else:
                logging.info( 'status - {} while parsing url {}'.format( feed.status, url ))
        return feeds
        # return [ feedparser.parse( url ) for url in urls ] 


    def get_dict( self ):
        ''' construct a dictionary with all podcast with episodes in list '''
        podcasts_dict = dict()
        feeds = self.get_feeds()
        for feed in feeds:
            title = self._get_channel_title( feed )
            logging.info( 'constructing dict for {}'.format( title ))
            podcasts_dict[ title ] = dict(
                last_updated = feed.updated if hasattr( feed, 'updated' ) \
                                            else feed.get( 'feed' ).get( 'updated' ),
                etag         = feed.etag if hasattr( feed, 'etag' ) else None,
                rsslink      = feed.href,
                link         = feed.feed.link,
                subtitle     = feed.feed.get( 'subtitle' ), 
                episodes     = self._construct_episodes_message( feed )
            ) 

        return podcasts_dict

    def _get_channel_title( self, feed ):
        ''' returns the title of the channel '''
        return feed.get( 'channel' ).get( 'title' )

    def _construct_episodes_message( self, feed ):
        ''' returns a list of dictionary with episode url, time, title etc'''
        episodes = list()
        entries = feed.entries
        for entry in entries:
            firstlink  = entry.get( 'links' )[ 0 ]
            secondlink = entry.get( 'links' )[ 1 ] if len( entry.get( 'links' )) > 1 else dict() 
            textlink, audiolink = ( firstlink.get( 'href' ), secondlink.get( 'href' )) if \
                'text' in firstlink.get( 'type' ) else ( secondlink.get( 'href' ), firstlink.get( 'href' ))
            episodes.append(
                dict(
                    title     = entry.title.replace( '\u00A0', ' ' ),
                    subtitle  = entry.get( 'subtitle' ),
                    published = entry.get( 'published' ),
                    audiolink = audiolink,
                    link      = textlink,
                )
            )
        return episodes
    
    def dump_json( self, filename ):
        ''' dump all json to filename'''
        with open( filename, 'w' ) as jsonfile:
            json.dump( self.get_dict(), jsonfile )

