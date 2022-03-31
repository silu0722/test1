# -*- coding: utf-8 -*-

import asyncio
import requests
import json
import threading


async def profile():

    model = "http://113.31.111.86:19025/generate"
    query = "http://113.31.111.86:19025/fetch"

    req_params = {"text": "我是华院数字人",
                  "voice_id": "dahu",
                  "image_id": "s007",
                  "mode": "mp4",
                  "speed": "1.2"
                  }

    with requests.session() as session:
        resp = session.post(model, json=req_params)
        print(resp.status_code)
        resp = json.loads(resp.text)
        task_id = resp.get("task_id")
        req_params = {'task_id': task_id}
        # 查询结果
        resp = session.post(query, json = req_params)
        jsres = json.loads(resp.text)
        while jsres.get("progress") != "100":
            print(jsres.get('progress'))
            await asyncio.sleep(1)
            print("wait")
            resp = session.post(query, json=req_params)
            jsres = json.loads(resp.text)
        print("---------Finished----------")


def run():
    def _run():
        asyncio.run(profile())
    th = threading.Thread(target=_run())
    th.start()
    return th


if __name__ == '__main__':
    import time

    start = time.time()
    threads = [run() for i in range(3)]
    [th.join() for th in threads]
    end = time.time()

    print("Time cost: {0}".format(end - start))
