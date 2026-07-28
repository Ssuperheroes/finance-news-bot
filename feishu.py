import requests
import os
import time
import hmac
import hashlib
import base64



# ==========================
# 飞书签名
# ==========================

def gen_sign(secret):

    timestamp = str(
        int(time.time())
    )


    string_to_sign = (
        timestamp
        + "\n"
        + secret
    )


    hmac_code = hmac.new(

        string_to_sign.encode("utf-8"),

        digestmod=hashlib.sha256

    ).digest()


    sign = base64.b64encode(
        hmac_code
    ).decode("utf-8")


    return timestamp, sign



# ==========================
# JSON日报转换Markdown
# ==========================

def format_report(report):


    content = ""


    # 标题

    content += (
        f"# 📰 {report.get('title','AI财经早报')}\n\n"
    )


    # 今日总结

    content += (
        "## 📌 今日一句话\n\n"
    )

    content += (
        report.get(
            "summary",
            ""
        )
        + "\n\n"
    )


    content += "---\n\n"



    # 全球市场

    content += (
        "## 🌍 全球市场\n\n"
    )


    for item in report.get(
        "global_market",
        []
    ):

        content += (

            f"🔹 **{item.get('title','')}**\n\n"

            f"事件：{item.get('event','')}\n\n"

            f"影响：{item.get('analysis','')}\n\n"

            f"关注：{item.get('focus','')}\n\n"

        )



    content += "---\n\n"



    # 中国市场

    content += (
        "## 🇨🇳 中国市场\n\n"
    )


    for item in report.get(
        "china_market",
        []
    ):

        content += (

            f"🔹 **{item.get('title','')}**\n\n"

            f"事件：{item.get('event','')}\n\n"

            f"影响：{item.get('analysis','')}\n\n"

            f"关注：{item.get('focus','')}\n\n"

        )



    content += "---\n\n"



    # 科技产业

    content += (
        "## 🤖 科技产业观察\n\n"
    )


    for item in report.get(
        "technology",
        []
    ):


        content += (

            f"🔹 **{item.get('title','')}**\n\n"

            f"事件：{item.get('event','')}\n\n"

            f"影响：{item.get('analysis','')}\n\n"

            f"关注：{item.get('focus','')}\n\n"

        )



    content += "---\n\n"



    # 产业趋势

    content += (
        "## 🏭 产业趋势\n\n"
    )


    for item in report.get(
        "industry",
        []
    ):


        content += (

            f"🔹 **{item.get('title','')}**\n\n"

            f"{item.get('analysis','')}\n\n"

        )



    content += "---\n\n"



    # 今日重点

    content += (
        "## ⭐ 今日重点关注\n\n"
    )


    for index,item in enumerate(

        report.get(
            "important_events",
            []
        ),

        1

    ):


        content += (

            f"{index}. "
            f"{item.get('title','')}\n"

            f"原因："
            f"{item.get('reason','')}\n\n"

        )



    content += "---\n\n"



    # 风险

    content += (
        "⚠️ 风险提示："
        +
        report.get(
            "risk_warning",
            ""
        )
    )


    return content




# ==========================
# 发送飞书卡片
# ==========================

def send_feishu_card(content):


    webhook = os.getenv(
        "FEISHU_WEBHOOK"
    )


    secret = os.getenv(
        "FEISHU_SECRET"
    )


    if not webhook:

        raise Exception(
            "缺少 FEISHU_WEBHOOK"
        )


    if not secret:

        raise Exception(
            "缺少 FEISHU_SECRET"
        )



    timestamp, sign = gen_sign(
        secret
    )



    headers = {

        "Content-Type":
        "application/json"

    }



    card = {


        "msg_type":
        "interactive",


        "timestamp":
        timestamp,


        "sign":
        sign,


        "card":{


            "config":{

                "wide_screen_mode":
                True

            },


            "header":{


                "title":{

                    "tag":
                    "plain_text",

                    "content":
                    "📰 AI财经早报"

                },


                "template":
                "blue"

            },


            "elements":[


                {

                    "tag":
                    "div",

                    "text":{

                        "tag":
                        "lark_md",

                        "content":
                        content

                    }

                },


                {

                    "tag":
                    "hr"

                },


                {

                    "tag":
                    "note",

                    "elements":[

                        {

                            "tag":
                            "plain_text",

                            "content":
                            "AI自动生成 · 财经资讯分析"

                        }

                    ]

                }


            ]

        }

    }



    response = requests.post(

        webhook,

        headers=headers,

        json=card,

        timeout=10

    )


    print(
        "飞书返回:"
    )


    print(
        response.text
    )




# ==========================
# 本地测试
# ==========================

if __name__ == "__main__":


    test_report = {


        "title":
        "AI财经早报",


        "summary":
        "AI硬件进入调整阶段，市场开始关注产业兑现能力。",


        "global_market":[

            {

                "title":
                "美联储政策会议",

                "event":
                "市场关注未来利率路径。",

                "analysis":
                "货币政策变化可能影响全球风险资产估值。",

                "focus":
                "美元、科技股表现"

            }

        ],


        "china_market":[

            {

                "title":
                "AI产业链调整",

                "event":
                "算力硬件板块出现波动。",

                "analysis":
                "市场开始关注企业订单和盈利兑现。",

                "focus":
                "产业需求"

            }

        ],


        "technology":[

            {

                "title":
                "人工智能产业发展",

                "event":
                "AI应用持续推进。",

                "analysis":
                "产业进入从技术验证到商业落地阶段。",

                "focus":
                "应用生态"

            }

        ],


        "industry":[

            {

                "title":
                "半导体周期",

                "analysis":
                "国产供应链建设持续推进。"

            }

        ],


        "important_events":[

            {

                "title":
                "美联储政策信号",

                "reason":
                "影响全球流动性环境"

            }

        ],


        "risk_warning":
        "短期市场波动增加，需要关注政策和产业数据。"

    }



    content = format_report(
        test_report
    )


    send_feishu_card(
        content
    )
