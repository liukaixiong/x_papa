import pymysql

from common.mysql_connect import MysqldbHelper
from x_weibo.spiders.abs.AbstractDBProcess import AbstractDBProcess

"""
    Excel 导出
"""


class WeiBoMysqlDBProcess(AbstractDBProcess):
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '1234',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    db_name = "pachong"

    db = MysqldbHelper(config)

    # db.selectDataBase("pachong")

    def connect(self):
        self.db.selectDataBase(self.db_name)

    def process_item(self, items, spider):
        data_type = items["groupType"]
        table_name = ""
        request_data = {}
        if data_type == "用户信息":
            table_name = "wb_user"
            request_data["user_id"] = items.get("用户编号", "")
            request_data["nike_name"] = items.get("昵称", "")
            request_data["ren_zheng"] = items.get("认证", "")
            request_data["sex"] = items.get("性别", "")
            request_data["area"] = items.get("地区", "")
            request_data["birthday"] = items.get("生日", "")
            request_data["remark"] = items.get("认证信息", "")
            request_data["tag"] = "|".join(items.get("标签", ""))
            request_data["weibo"] = items.get("微博数", "")
            request_data["guanzhu"] = items.get("关注", "")
            request_data["fensi"] = items.get("粉丝", "")
            request_data["fenzu"] = items.get("分组", "")
            request_data["user_home_page"] = items.get("首页", "")
            request_data["daren"] = items.get("达人", "")
            request_data["study"] = items.get("学习经历", "")
            request_data["xing"] = items.get("性取向", "")
            request_data["ganqing"] = items.get("感情状况", "")
            request_data["work"] = items.get("工作经历", "")
            request_data["source_id"] = items.get("来源编号", "")
            request_data["source_type"] = items.get("来源类型", "")
            # request_data["created_time"] = time.localtime(time.time())
        elif data_type == "微博信息":
            table_name = "wb_weibo"
            request_data["user_id"] = items["用户编号"]
            request_data["home_page"] = items["用户主页"]
            request_data["like_count"] = items["点赞"]
            request_data["pinglun_count"] = items["评论"]
            request_data["zhuanfa_count"] = items["转发"]
            request_data["weibo_no"] = items["微博编号"]
            request_data["push_time"] = items["发布时间"]
            request_data["push_source"] = items["手机型号"]
            request_data["content"] = items["微博内容"]
            # request_data["created_time"] = items[""]
        elif data_type == "评论信息":
            table_name = "wb_pinglun"
            request_data["user_id"] = items["用户编号"]
            request_data["username"] = items["用户名"]
            request_data["home_page"] = items["用户首页"]
            request_data["content"] = items["评论内容"]
            request_data["like_count"] = items["点赞数"]
            request_data["weibo_no"] = items["微博编号"]
            request_data["push_time"] = items["发布时间"]
            # request_data["created_time"] = items[""]
        self.db.insert(table_name, request_data)

    def close_spider(self, spider):
        print("Mysql  执行完成 ....")
        # self.db.save('test_data.xlsx')
