import feedparser


RSS_LIST = [

"https://rsshub.app/cls/telegraph",

"https://rsshub.app/eastmoney/news",

]


def get_news():

    news=[]

    for url in RSS_LIST:

        feed = feedparser.parse(url)


        for item in feed.entries[:10]:

            news.append(
                item.title
            )


    return "\n".join(news)


