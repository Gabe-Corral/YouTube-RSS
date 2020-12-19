# YouTube-RSS

**Description:**

A command line RSS feed for YouTube written in Python.

**Setup:**

Requires Python3

```
git clone https://github.com/Gabe-Corral/YouTube-RSS.git
pip3 install feedparser
```

You will need to add xml feeds to urls.txt. The urls should look something like this: https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>. Add as many as you want.

```
cd YouTube-RSS
python3 main.py
```

**Usage:**

- Use up and down arrows to navigate
- Use left arrow to go back
- Use enter to select a channel/video
- Press enter on a video to open the video in your browser
