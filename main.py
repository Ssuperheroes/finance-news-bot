from news import get_news
from volcengine import summary
from feishu import send



def main():


    news=get_news()


    result=summary(news)



    send(

        "📰 每日财经资讯\n\n"

        +result

    )



if __name__=="__main__":

    main()
