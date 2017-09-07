import urllib.request
from wechat_sender import Sender
from html.parser import HTMLParser
import re


base = r'https://www.amazon.cn'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
data = {}

req = urllib.request.Request(base, data, headers)

source = urllib.request.urlopen(req)
b_content = source.read()
content = b_content.decode('utf-8')
source.close()

#############################
# 从亚马逊首页对图书品类的url进行提取
bookurl_pattern = re.compile(r'图书","url1":"(.*?)"', re.S)
entireurl = base+re.search(bookurl_pattern, content).group(1)
print(entireurl)


#############################
req_book = urllib.request.Request(entireurl, data, headers)
source_book = urllib.request.urlopen(req_book)
b_book_content = source_book.read()
book_content = b_book_content.decode('utf-8')
source_book.close()


def match(value):
    model = r'.*满200元减.*'
    return re.match(model, value)


def sendmessage(value):
    Sender().send(value)


def savemessage(value):
    return value


class AMZparser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.keyword = []

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            if len(attrs) ==0:pass
            else:
                for(varible, value) in attrs:
                    if varible == 'title':
                        if match(value) is not None:
                            savemessage(value)
                            # sendmessage(value)


if __name__ == '__main__':
    parser = AMZparser()
    parser.feed(book_content)
    parser.close()
    print("check end")