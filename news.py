import feedparser
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


# =========================
# 新闻关键词
# =========================

KEYWORDS = [

    "中国经济",
    "A股市场",
    "人工智能",
    "AI产业",
    "半导体",
    "芯片",
    "英伟达",
    "美股",
    "美联储",
    "全球金融市场",
    "科技产业"

]


# =========================
# 新闻重要性权重
# =========================

IMPORTANCE_KEYWORDS = {


    # 宏观政策
    "美联储": 10,
    "降息": 10,
    "加息": 10,
    "利率": 8,
    "央行": 10,
    "国务院": 10,
    "财政部": 8,
    "商务部": 8,
    "政策": 7,


    # AI产业
    "英伟达": 10,
    "OpenAI": 10,
    "人工智能": 8,
    "AI": 7,
    "算力": 8,
    "GPU": 8,
    "数据中心": 7,


    # 半导体
    "半导体": 8,
    "芯片": 8,
    "先进制程": 9,
    "光刻机": 9,
    "存储": 7,
    "晶圆": 7,


    # 宏观经济
    "GDP": 8,
    "通胀": 8,
    "就业": 7,
    "贸易": 6,
    "出口": 6,


    # 市场事件
    "暴跌": 8,
    "大跌": 7,
    "上涨": 5,
    "创新高": 7,
    "调整": 5,
    "波动": 5,


    # 产业关键词
    "机器人": 7,
    "新能源": 6,
    "汽车": 5,
    "消费": 5

}



# =========================
# 北京时间
# =========================

BEIJING_TZ = timezone(
    timedelta(hours=8)
)



def get_beijing_time():

    return datetime.now(
        BEIJING_TZ
    )



# =========================
# 时间解析
# =========================

def parse_time(item):

    try:

        dt = parsedate_to_datetime(
            item.published
        )


        return dt.astimezone(
            BEIJING_TZ
        )


    except Exception:

        return None



# =========================
# 判断24小时
# =========================

def is_recent(item):

    pub_time = parse_time(item)


    if not pub_time:

        return False


    now = get_beijing_time()


    diff = now - pub_time


    return (
        timedelta(0)
        <= diff
        <= timedelta(hours=24)
    )



# =========================
# 新闻评分
# =========================

def calculate_score(title):

    score = 0


    title_lower = title.lower()


    for keyword, weight in IMPORTANCE_KEYWORDS.items():


        if keyword.lower() in title_lower:

            score += weight


    return score



# =========================
# 获取新闻
# =========================

def get_news():

    news = []

    seen = set()



    for keyword in KEYWORDS:


        url = (
            "https://news.google.com/rss/search?"
            "q="
            + quote(keyword)
            + "&hl=zh-CN"
            "&gl=CN"
            "&ceid=CN:zh-Hans"
        )


        print(
            "\n正在抓取:",
            keyword
        )


        feed = feedparser.parse(url)


        print(
            "获取:",
            len(feed.entries),
            "条"
        )


        valid = 0


        for item in feed.entries:


            # 过滤24小时
            if not is_recent(item):

                continue



            title = item.title.strip()



            # 去重
            if title in seen:

                continue


            seen.add(title)


            pub_time = parse_time(item)


            score = calculate_score(
                title
            )


            news.append({

                "title": title,

                "time":
                pub_time.strftime(
                    "%Y-%m-%d %H:%M"
                ),

                "score":
                score

            })


            valid += 1



        print(
            "有效:",
            valid,
            "条"
        )



    # =========================
    # 排序
    # 优先级：
    # 1. 新闻重要程度
    # 2. 发布时间
    # =========================


    news.sort(

        key=lambda x:

        (
            x["score"],

            x["time"]

        ),

        reverse=True

    )



    return news[:30]



# =========================
# 给AI模型格式化
# =========================

def format_news(news):

    text = ""


    for i,item in enumerate(news):


        text += (

            f"{i+1}. "

            f"[重要度:{item['score']}]\n"

            f"{item['title']}\n"

            f"时间:"
            f"{item['time']}\n\n"

        )


    return text



# =========================
# 测试
# =========================

if __name__ == "__main__":


    news = get_news()



    print(
        "\n====== 北京时间24小时财经新闻 ======\n"
    )


    for i,item in enumerate(news):


        print(

            f"{i+1}."

            f" [{item['score']}分] "

            f"{item['title']}"

        )


        print(
            "时间:",
            item["time"]
        )


        print()



    print(
        "新闻数量:",
        len(news)
    )
