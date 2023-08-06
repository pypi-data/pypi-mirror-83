# Author: Thoxvi <A@Thoxvi.com>

__all__ = [
    "WorkWechatRobotAPI",
]

import base64
import hashlib
import json
import logging
from typing import List

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class WorkWechatRobotAPI(object):
    def __init__(self, web_hook: str):
        self.__web_hook_addr = web_hook
        self.__header = {'content-type': 'application/json'}

    def send_raw_data(self, data: dict):
        logger.debug("Request: " + str(data))
        try:
            response = requests.post(self.__web_hook_addr, data=json.dumps(data), headers=self.__header)
            logger.debug("Response code: " + str(response.status_code))
            if response.status_code == 200:
                rjson = response.json()
                logger.debug("Response data: " + str(rjson))
                if rjson.get("errcode", 1) == 0:
                    return True
                else:
                    logger.error(rjson.get("errmsg", "No msgs"))
                    return False
            else:
                logger.error("Response content: " + response.content.decode())
                return False

        except Exception as err:
            logger.error(err)
            return False

    def send_markdown(self, markdown: str, at_list: List[str] = None) -> bool:
        if at_list is None:
            at_list = []
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": markdown,
                "mentioned_list": at_list
            }
        }
        return self.send_raw_data(data)

    def send_pic(self, uri: str) -> bool:
        if uri.startswith("https://") or uri.startswith("http://"):
            context = requests.get(uri).content
        else:
            with open(uri, "rb") as f:
                context = f.read()

        b64code = base64.b64encode(context).decode("utf-8")
        md5 = hashlib.md5(context).hexdigest()

        data = {
            "msgtype": "image",
            "image": {
                "base64": b64code,
                "md5": md5
            }
        }

        return self.send_raw_data(data)
