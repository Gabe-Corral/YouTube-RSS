from pytube import YouTube
import os
import subprocess
import time


class Download:

    def mp4Download(url, filename):
        filename = filename.split(" ")
        filename = "".join(filename)
        YouTube(url).streams.filter(file_extension='mp4').first().download(filename=filename)

    def mp3Download(url, filename):
        filename = filename.split(" ")
        filename = "".join(filename)
        YouTube(url).streams.first().download(filename=filename)
        time.sleep(1)
        mp4 = "'%s'.mp4" % filename
        mp3 = "'%s'.mp3" % filename
        ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
        subprocess.call(ffmpeg, shell=True)
        os.remove(filename + ".mp4")
