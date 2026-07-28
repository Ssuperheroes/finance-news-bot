from news import get_news, format_news
from volcengine import summary
from feishu import send_feishu_card, format_report


def main():

    news = get_news()

    news_text = format_news(news)

    report = summary(news_text)

    content = format_report(report)

    send_feishu_card(content)



if __name__ == "__main__":
    main()
