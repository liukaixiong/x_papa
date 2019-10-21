import datetime
import re


class reUtils:

    def find_all_search(self, pattern, content, default_text):
        result = re.search(pattern, content)
        if result is None or result == "":
            return default_text
        return result.group()

    def find_all(self, pattern, content, default_text):
        result = re.findall(pattern, content)
        if result is None or len(result) == 0:
            return default_text
        return result[0]

    def time_fix(self, time_string):

        if time_string is None or time_string == "":
            return ""

        now_time = datetime.datetime.now()
        if '分钟前' in time_string:
            minutes = re.search(r'^(\d+)分钟', time_string).group(1)
            created_at = now_time - datetime.timedelta(minutes=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M')

        if '小时前' in time_string:
            minutes = re.search(r'^(\d+)小时', time_string).group(1)
            created_at = now_time - datetime.timedelta(hours=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M')

        if '今天' in time_string:
            return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

        if '月' in time_string:
            time_string = time_string.replace('月', '-').replace('日', '')
            time_string = str(now_time.year) + '-' + time_string
            return time_string.rstrip()

        return time_string

    def get_request_by_json(self, request):
        request_params_list = request.split("&")
        result = {}
        for params in request_params_list:
            param = params.split("=")
            result[param[0]] = param[1]
        return result


if __name__ == '__main__':
    utils = reUtils()
    # print(utils.time_fix("7分钟前"))
    print("",utils.get_request_by_json("id=4427778004439002&root_comment_max_id=14518664228627463&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=4216&filter_tips_before=0"))
