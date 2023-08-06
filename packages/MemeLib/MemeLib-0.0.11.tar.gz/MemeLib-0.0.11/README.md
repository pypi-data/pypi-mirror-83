# MemeLib
## A python lib to get dank memes
<p align="center">
<a href="https://pypi.org/project/memelib/">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/memelib?color=g&style=flat-square">
</a>
<a href="https://github.com/CraziiAce/memelib/blob/master/LICENSE">
  <img alt="License" src="https://img.shields.io/github/license/craziiace/memelib?color=g&style=flat-square">
</a>
<a href="https://www.python.org/downloads/">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/memelib?color=g&style=flat-square">
</a>
<a href="https://github.com/CraziiAce/memelib/issues">
  <img alt="Issues" src="https://img.shields.io/github/issues/craziiace/memelib?color=g&style=flat-square">
</a>
<a href="http://makeapullrequest.com">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?color=g&style=flat-square">
</a>
<a href="https://github.com/craziiace/memelib">
  <img src="https://img.shields.io/tokei/lines/github/craziiace/memelib?style=flat-square&color=g">
</a>

### Installation

MemeLib is installed through PyPi

```
pip install MemeLib
```

### Usage

```py
from memelib.api import DankMemeClient

myclient = DankMemeClient()

await myclient.meme(subreddit="dankmemes")
```
That returns a dict.
```
{'title': 'Creeping in', 'author': 'u/charles2x2', 'subreddit': 'r/dankmemes', 'upvotes': 117, 'comments': 6, 'img_url': 'https://i.redd.it/c1onsrvplnu51.jpg', 'post_url': 'https://reddit.com/r/dankmemes/comments/jg0ax7/creeping_in/'}
```
Params for the `DankMemeClient` call:

`reddit_user_agent`: str | The reddit user agent. Preferrably, this would be the name of your application.

`return_embed`: bool | Whether to return a Discord.py embed.

`embed_color` | A color for the discord embed. Must be in 0xFFFFFF format.

If `return_embed` is true, this will automatically return a nicely formatted embed.

Example:

<img src="https://craziiace.reeee.ee/GfxTbo.png">
