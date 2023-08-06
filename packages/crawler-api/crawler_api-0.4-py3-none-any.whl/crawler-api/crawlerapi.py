import requests
import time


def get_create_time(cls):
    creat_time = int(round(time.time() * 1000))
    return creat_time

# class CrawlAPI(object):
#     VERSION = 0.2
#
#     @classmethod
#     def wrap_api(cls, json_data):
#         json_data["meta"]["version"] = CrawlAPI.VERSION
#
#     @classmethod
#     def get_task_id(cls):
#         url = 'http://127.0.0.1:3000/get-task-id'
#         task_id = requests.get(url).text
#         return task_id
#
#     @classmethod
#
#
#     @classmethod
#     def upload(cls, data):
#         url_post = 'http://127.0.0.1:3000/kno-storage-req'
#         input = requests.post(url_post, json=data)
#         if input.status_code == 200:
#             print("插入成功")
#         else:
#             raise Exception("插入失败")
#         return input.status_code
