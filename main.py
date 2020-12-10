import feedparser, os, webbrowser, curses


class RssFeed:

    def __init__(self):
        self.rssFeeds = []

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

    def printFeeds(self, stdscr, current_row):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, i in enumerate(self.rssFeeds):
            key_name = str([key for key in i]).strip("'[]'")
            x = w//2 - len(key_name)//2
            y = h//2 - len(self.rssFeeds)//2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, key_name)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, key_name)
        stdscr.refresh()

    def main(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_row = 0
        self.printFeeds(stdscr, current_row)

        while 1:
            key = stdscr.getch()
            #stdscr.clear()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.rssFeeds)-1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.showChannel(stdscr, current_row)
                stdscr.refresh()
                stdscr.getch()

            self.printFeeds(stdscr, current_row)
            stdscr.refresh()

    def printVideos(self, stdscr, current_row):
        print(current_row)


    def showChannel(self, stdscr, current_row):
        self.printVideos(stdscr, current_row)




if __name__=='__main__':
    root = RssFeed()
    curses.wrapper(root.main)
