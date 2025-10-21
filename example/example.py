from podcast_util import PodcastUtil

pd = PodcastUtil('podcasts.opml')
pd.dump_json('dumpjson.json')
