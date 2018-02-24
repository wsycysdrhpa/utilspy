# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-6-19'


import urllib
import urllib2
import os
import sys
import time


class UrlOpener(urllib.FancyURLopener):
    """Create sub-class in order to overide error 206.  This error means a
       partial data is being sent,
       which is ok in this case.  Do nothing with this error.
    """
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass


def download_with_breakpoint(url, save_file_path):
    loop = 1
    exist_size = 0
    url_opener = UrlOpener()
    if os.path.exists(save_file_path):
        out_file = open(save_file_path, "ab")
        exist_size = os.path.getsize(save_file_path)
        #If the data exists, then only downloader the remainder
        url_opener.addheader("Range", "bytes=%s-" % exist_size)
    else:
        out_file = open(save_file_path, "wb")

    web_page = url_opener.open(url)

    #If the data exists, but we already have the whole thing, don't downloader again
    file_size = int(web_page.headers['Content-Length'])
    if file_size == exist_size:
        loop = 0
        print "File already downloaded"

    num_bytes = 0
    while loop:
        data = web_page.read(8192)
        if not data:
            break
        out_file.write(data)
        num_bytes += len(data)
        percent = round(float(exist_size + num_bytes) / file_size * 100, 5)
        sys.stdout.write('complete percent:' + str(percent) + '%'),
        sys.stdout.write("\r")
        time.sleep(0.01)

    web_page.close()
    out_file.close()

def download_file(url, save_file_path):
    u = urllib2.urlopen(url)
    f = open(save_file_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (save_file_path, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        # print status,
        sys.stdout.write(status),
        sys.stdout.write("\r")

    f.close()


if __name__ == "__main__":
    # download_with_breakpoint("http://10.10.11.103:8000/static/76.sql", "76.sql")
    download_file("http://s1.music.126.net/downloader/pc/cloudmusicsetup_2_1_2[168028].exe", "cloudmusicsetup_2_1_2[168028].exe")
