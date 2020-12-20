import feedparser
import webbrowser
import curses
from curses.textpad import Textbox, rectangle
from downloader import Download

class RssFeed:

    def __init__(self):
        self.rssFeeds = []
        self.main_loop = True
        self.second_loop = False
        self.current_row = 0
        self.current_video = 0
        self.video_count = 0
        self.showVideo = False
        self.videoName = ""
        self.key = ""
        self.startDowanloder = False
        self.index_download = 0
        self.download_options = ["MP3 DOWNLOAD", "MP4 DOWNLOAD"]

        with open('urls.txt', 'r') as urls:
            for line in urls:
                self.parseUrls(line)


    def parseUrls(self, url):
        newFeed = feedparser.parse(url)
        feedData = {}
        for entry in newFeed['entries']:
            feedData[entry['title']] = [
            entry['title'],
            entry['link'],
            entry['summary'],
            entry['authors'][0]['name'],
            entry['authors'][0]['href']
            ]
        fullFeed = {newFeed['feed']['title']: feedData}
        self.rssFeeds.append(fullFeed)


    def printFeeds(self, stdscr):
        stdscr.clear()
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        h, w = stdscr.getmaxyx()
        for idx, i in enumerate(self.rssFeeds):
            key_name = str([key for key in i]).strip("'[]'")
            x = w//2 - len(key_name)//2
            y = h//2 - len(self.rssFeeds)//2 + idx
            if idx == self.current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, key_name)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, key_name)
        stdscr.refresh()


    def main(self, stdscr):
        self.second_loop = False
        curses.curs_set(0)
        self.printFeeds(stdscr)

        while self.main_loop:
            key = stdscr.getch()
            stdscr.clear()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.rssFeeds)-1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.showChannel(stdscr)
                self.main_loop = False
            elif key == curses.KEY_RIGHT:
                self.downloader(stdscr)
            elif key == curses.KEY_LEFT:
                break
            self.printFeeds(stdscr)
            stdscr.refresh()


    def printVideos(self, stdscr):
        stdscr.clear()
        curses.init_pair(1, curses.COLOR_RED, -1)
        h, w = stdscr.getmaxyx()
        for k, v in self.rssFeeds[self.current_row].items():
            for idx, i in enumerate(self.rssFeeds[self.current_row][k]):
                self.video_count += 1
                x = w//2 - len(i)//2
                y = h//2 - 15//2 + idx
                if self.showVideo == True:
                    self.showVideoDetails(stdscr, i, k)
                    break
                elif idx == self.current_video:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, i)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, i)
        stdscr.refresh()


    def showChannel(self, stdscr):
        self.showVideo = False
        self.second_loop = True
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.printVideos(stdscr)

        while self.second_loop:
            key = stdscr.getch()
            if key == curses.KEY_UP and self.current_video > 0:
                self.current_video -= 1
            elif key == curses.KEY_DOWN and self.current_video < self.video_count:
                self.current_video += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.showVideo = True
            elif key == curses.KEY_LEFT:
                self.main_loop = True
                self.main(stdscr)
            self.printVideos(stdscr)
            stdscr.refresh()


    def printVideoDetails(self, stdscr, videoName, key):
        details = ['Title:', videoName, 'URL:',
        self.rssFeeds[self.current_row][key][videoName][1],
        'Author:', self.rssFeeds[self.current_row][key][videoName][3],
        'Channel:', self.rssFeeds[self.current_row][key][videoName][4],
        ]
        h, w = stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        for idx, i in enumerate(details):
            x = w//2 - len(i)//2
            y = h//2 - len(details)//2 + idx
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, i)
            stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()


    def showVideoDetails(self, stdscr, videoName, key):
        self.second_loop = False
        self.main_loop = False
        self.key = key
        self.videoName = videoName
        self.printVideoDetails(stdscr, self.videoName, self.key)

        while self.showVideo:
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                webbrowser.open(self.rssFeeds[self.current_row][self.key][self.videoName][1])
            elif key == curses.KEY_LEFT:
                self.second_loop = True
                self.showChannel(stdscr)
            elif key == curses.KEY_RIGHT:
                Download.mp4Download(self.rssFeeds[self.current_row][self.key][self.videoName][1],
                self.videoName)
            elif key == curses.KEY_DOWN:
                Download.mp3Download(self.rssFeeds[self.current_row][self.key][self.videoName][1],
                self.videoName)
                stdscr.clear()
            self.printVideoDetails(stdscr, self.videoName, self.key)
            stdscr.refresh()

    def printDownloader(self, stdscr):
        h, w = stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_RED, -1)
        for idx, i in enumerate(self.download_options):
            x = w//2 - len(i)//2
            y = h//2 - len(self.download_options)//2 + idx
            if idx == self.index_download:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, i)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, i)
        stdscr.refresh()

    def downloader(self, stdscr):
        main_loop = False
        self.startDowanloder = True

        self.printDownloader(stdscr)
        while self.startDowanloder:
            key = stdscr.getch()
            if key == curses.KEY_LEFT:
                self.main_loop = True
                self.startDowanloder = False
                self.showChannel(stdscr)
            elif key == curses.KEY_UP and self.index_download > 0:
                self.index_download -= 1
            elif key == curses.KEY_DOWN and self.index_download < 1:
                self.index_download += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.downloadMp4ByURL(stdscr, self.download_options[self.index_download])

            self.printDownloader(stdscr)
            stdscr.refresh()

    def downloadMp4ByURL(self, stdscr, format):
        stdscr.addstr(0, 0, "Enter YouTube URL: (hit Ctrl-G to download)")
        editwin = curses.newwin(1,80, 2,1)
        rectangle(stdscr, 1,0, 1+1+1, 1+80+1)
        stdscr.refresh()
        box = Textbox(editwin)
        box.edit()
        url = box.gather()
        if format == "MP3 DOWNLOAD":
            Download.mp3Download(url, "test")
        elif format == "MP4 DOWNLOAD":
            Download.mp4Download(url, "test")



if __name__=='__main__':
    root = RssFeed()
    curses.wrapper(root.main)
