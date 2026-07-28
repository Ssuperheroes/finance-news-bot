import requests
import os
import json

from news import get_news, format_news



# =========================
# 火山豆包分析
# =========================

def summary(news_text):


    prompt = f"""

你是一名专业财经研究员。

根据以下过去24小时财经新闻，
生成《每日财经研究早报》。

你的任务不是简单摘要，
而是：

事件发生了什么？
为什么重要？
影响哪些产业？
未来关注什么？


请严格输出 JSON。

不要输出 Markdown。
不要输出解释文字。


JSON格式：

{{
"title":"AI财经早报",

"date":"北京时间日期",

"summary":
"今日一句话总结",


"global_market":[

    {{
    "title":"",
    "event":"",
    "analysis":"",
    "focus":""
    }}

],


"china_market":[

    {{
    "title":"",
    "event":"",
    "analysis":"",
    "focus":""
    }}

],


"technology":[

    {{
    "title":"",
    "event":"",
    "analysis":"",
    "focus":""
    }}

],


"industry":[

    {{
    "title":"",
    "event":"",
    "analysis":""
    }}

],


"important_events":[

    {{
    "title":"",
    "reason":""
    }}

],


"risk_warning":

""

}}



规则：

1. 所有内容必须来自新闻。
2. 不编造事实。
3. 不预测股票涨跌。
4. 不推荐股票。
5. 可以分析产业影响。
6. 每个分类最多3条。
7. 每条控制100字以内。
8. 优先级：
政策 > 全球市场 > 科技产业 > 企业事件。
9. 输出必须是合法JSON。


新闻：

{news_text}

"""



    url = (
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    )



    headers = {


        "Authorization":

        f"Bearer {os.getenv('VOLC_API_KEY')}",


        "Content-Type":

        "application/json"

    }



    data = {


        "model":

        os.getenv(
            "VOLC_MODEL"
        ),



        "messages":[

            {

                "role":
                "user",

                "content":
                prompt

            }

        ],



        "temperature":

        0.2

    }



    print(
        "正在请求火山豆包..."
    )



    response = requests.post(

        url,

        headers=headers,

        json=data,

        timeout=120

    )



    if response.status_code != 200:


        print(
            response.text
        )


        raise Exception(
            "火山API调用失败"
        )



    result = response.json()



    content = (

        result["choices"][0]

        ["message"]

        ["content"]

    )



    # 去除可能存在的代码块

    content = content.strip()


    if content.startswith(
        "```"
    ):

        content = (

            content
            .replace("```json","")
            .replace("```","")
            .strip()

        )



    try:

        report = json.loads(
            content
        )


    except Exception:


        print(
            "JSON解析失败:"
        )


        print(content)


        raise



    return report





# =========================
# 测试
# =========================

if __name__ == "__main__":


    print(
        "正在获取新闻..."
    )


    news = get_news()



    print(
        "新闻数量:",
        len(news)
    )



    news_text = format_news(
        news
    )



    report = summary(
        news_text
    )



    print(
        "\n======日报JSON======\n"
    )


    print(

        json.dumps(

            report,

            ensure_ascii=False,

            indent=2

        )

    )
