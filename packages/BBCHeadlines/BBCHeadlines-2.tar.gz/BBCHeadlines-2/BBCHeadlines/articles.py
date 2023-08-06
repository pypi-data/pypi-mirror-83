import feedparser

def setup():
    entries = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')['entries']
    list = []
    for i in range(len(entries)):
        list.append(entries[i])
    return(list)

set = setup()

def title():
    list = []
    for i in range (len(set)):
        list.append((set[i]['title']))
    return(list)

def description():
    list = []
    for i in range (len(set)):
        list.append((set[i]['summary']))
    return(list)

def link():
    list = []
    for i in range (len(set)):
        list.append((set[i]['links'][0]['href']))
    return(list)
