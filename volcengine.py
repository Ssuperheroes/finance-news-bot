import requests
import os



def summary(news):


    prompt=f"""

你是一名专业财经新闻编辑。

根据以下新闻生成《每日财经资讯早报》。

要求：

1. 今日全球财经大事件
2. 中国市场重要新闻
3. 政策消息
4. 科技产业热点
5. 消费与制造业动态
6. 今日市场关注方向


规则：

- 只总结新闻事实
- 不预测股票涨跌
- 不提供投资建议
- 标注重要程度
- 中文输出


新闻：

{news}

"""


    response=requests.post(

        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",

        headers={

        "Authorization":
        f"Bearer {os.getenv('VOLC_API_KEY')}",

        "Content-Type":
        "application/json"

        },


        json={

        "model":
        "doubao-pro-32k",


        "messages":[

            {

            "role":"user",

            "content":prompt

            }

        ]

        }

    )


    return response.json()["choices"][0]["message"]["content"]
