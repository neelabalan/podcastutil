# Podcast Util :headphones:
[![Build Status - Github](https://github.com/neelabalan/podcastutil/workflows/pytesting/badge.svn)](https://github.com/neelabalan/podcastutil/actions?query=workflow%3Apytesting)
> A minimal Podcast feed parsing utility in python



## Usage



```python
from podcast_util import PodcastUtil

pd = PodcastUtil( 'podcasts.opml' )
pd.dump_json( 'dump.json' )
```

```bash
user@blue ~ time python3 example.py 

real    0m5.999s
user    0m0.676s
sys     0m0.053s
```


> you can refer to [`dump.json`](https://github.com/neelabalan/podcastutil/blob/master/extras/dump.json) to get the structure of how it is constructed

There are other functions like `get_feeds` and `extract_url_from_opml` you can view them in the `podcast_util.py` source file



## Testing

I have tested it on 121 different podcast RSS feeds

```bash
user@blue ~ time python3 testing.py

real	7m16.413s
user	1m18.394s
sys	0m1.334s
```

It takes 7 minutes and 16 seconds to parse all feeds and dump 178226 lines of JSON

