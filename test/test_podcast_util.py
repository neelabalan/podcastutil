from podcast.podcast_util import PodcastUtil
from feedparser import FeedParserDict

import pytest
import datetime
from unittest import mock

@pytest.fixture
def pu():
    '''Returns a Wallet instance with a zero balance'''
    return PodcastUtil('./extras/podcasts.opml')

@pytest.fixture
def feed():
    ''' returns feed instance '''
    return FeedParserDict(
        feed = FeedParserDict(
            link = 'https://sample.com',
            subtitle = 'This is the best podcast show in the entire universe',
            title = 'PodcastTitle'
        ),
        entries = [
            FeedParserDict(
                title = 'Episode1',
                subtitle = 'episode of week 1',
                published = str(datetime.datetime(2021, 1, 1)),
                links = [
                    {
                        'href': 'https://somesite.com/episode1.mp3',
                        'type': 'audio/mpeg'
                    },
                    {
                        'href': 'https://somesite.com/episode1',
                        'type': 'text'
                    }
                ]
            ),
            FeedParserDict(
                title = 'Episode2',
                subtitle = 'episode of week 2',
                published = str(datetime.datetime(2021, 1, 7)),
                links = [
                    {
                        'href': 'https://somesite.com/episode2',
                        'type': 'text',
                    },
                    {
                        'href': 'https://somesite.com/episode2.mp3',
                        'type': 'audio/mpeg'
                    }
                ]
            )
        ],
        etag = '5f77c6d7-45f1e',
        href = 'https://sample.podcast.tv/test.xml',
        updated = str(datetime.datetime(2021, 1, 1)),
        status = 200
    )

def test_extract_url_from_opml( pu ):
    # running pytest from parent dir
    # ../extras/podcasts.opml works only when runnig pytest from test dir
    assert pu.extract_url_from_opml() == ['https://feeds.twit.tv/tri.xml', 'https://feeds.megaphone.fm/sciencevs']

def test_get_channel_title( pu, feed ):
    assert pu._get_channel_title( feed ) == 'PodcastTitle'

# order of params matter here
@mock.patch('podcast.podcast_util.feedparser.parse')
def test_get_feeds(mock_parse, pu, feed):
    mock_parse.return_value = feed
    assert pu.get_feeds() == [feed, feed] 


def test_construct_episodes_message(pu, feed):
    expected = [
        {
            'title': 'Episode1',
            'subtitle': 'episode of week 1',
            'published': str(datetime.datetime(2021, 1, 1)),
            'audiolink': 'https://somesite.com/episode1.mp3',
            'link': 'https://somesite.com/episode1',
        },
        {
            'title': 'Episode2',
            'subtitle': 'episode of week 2',
            'published': str(datetime.datetime(2021, 1, 7)),
            'audiolink': 'https://somesite.com/episode2.mp3',
            'link': 'https://somesite.com/episode2',
        }
    ]
    assert pu._construct_episodes_message(feed) == expected

@mock.patch('podcast.podcast_util.PodcastUtil.get_feeds')
def test_get_dict(mock_get_feeds, pu, feed):
    mock_get_feeds.return_value = feed
    expected_dict = {
        'PodcastTitle': {
            'etag': '5f77c6d7-45f1e',
            'last_updated': str(datetime.datetime(2021, 1, 1)),
            'rsslink': 'https://sample.podcast.tv/test.xml',
            'link': 'https://sample.com',
            'subtitle': 'This is the best podcast show in the entire universe',
            'episodes': [
                {
                    'title': 'Episode1',
                    'subtitle': 'episode of week 1',
                    'published': str(datetime.datetime(2021, 1, 1)),
                    'audiolink': 'https://somesite.com/episode1.mp3',
                    'link': 'https://somesite.com/episode1',
                },
                {
                    'title': 'Episode2',
                    'subtitle': 'episode of week 2',
                    'published': str(datetime.datetime(2021, 1, 7)),
                    'audiolink': 'https://somesite.com/episode2.mp3',
                    'link': 'https://somesite.com/episode2',
                }
            ]
        }
    }