import requests
import os



def send(msg):


    url=os.getenv(
        "FEISHU_WEBHOOK"
    )


    data={

        "msg_type":"text",

        "content":{

            "text":msg

        }

    }


    requests.post(
        url,
        json=data
    )
