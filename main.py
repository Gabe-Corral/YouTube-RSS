import feedparser, os, webbrowser, curses


class RssFeed:

    def __init__(self):
        self.rssFeeds = []
        self.main_loop = True
        self.second_loop = False
        self.current_row = 0
        self.current_video = 0
        self.video_count = 0

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
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        #current_row = 0
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
                stdscr.refresh()
                stdscr.getch()

            self.printFeeds(stdscr)
            stdscr.refresh()

    def printVideos(self, stdscr):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for k, v in self.rssFeeds[self.current_row].items():
            for idx, i in enumerate(self.rssFeeds[self.current_row][k]):
                self.video_count += 1
                x = w//2 - len(i)//2
                y = h//2 - 15//2 + idx
                if idx == self.current_video:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, i)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, i)
        stdscr.refresh()



    def showChannel(self, stdscr):
        self.second_loop = True
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row = 0
        self.printVideos(stdscr)

        while self.second_loop:
            key = stdscr.getch()
            if key == curses.KEY_UP and self.current_video > 0:
                self.current_video -= 1
            elif key == curses.KEY_DOWN and self.current_video < self.video_count:
                self.current_video += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                print("enter")
            elif key == curses.KEY_LEFT:
                self.main_loop = True
                self.main(stdscr)
            self.printVideos(stdscr)
            stdscr.refresh()




if __name__=='__main__':
    root = RssFeed()
    curses.wrapper(root.main)
