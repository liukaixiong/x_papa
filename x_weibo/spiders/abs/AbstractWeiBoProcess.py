import abc
import logging
import re
import time
import traceback
from abc import abstractmethod
from time import sleep

import requests
import scrapy
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent
from scrapy import Selector

from common.reUtils import reUtils
from x_weibo import weibo_login_user
from x_weibo.spiders.utils.spiderConstants import spiderConstants


class AbstractWeiBoProcess(metaclass=abc.ABCMeta):
    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    base_url = "https://weibo.cn"
    reUtils = reUtils()

    default_cookie = weibo_login_user.default_cookie
    cookies_list = weibo_login_user.gen_cookies()

    # def __init__(self):
    #     self.cookies_list = wb_login.batch_login()
    """
        用户完整信息返回。
    """

    @abstractmethod
    def rs_process_user(self, result):
        print("未实现 --- rs_process_user")
        pass

    """
        用户信息回调返回，不包含微博粉丝、关注、分组
    """

    @abstractmethod
    def rs_weibo_user_info(self, result):
        print("未实现 --- rs_weibo_user_info")
        pass

    """
        单条微博对象回调列表
    """

    @abstractmethod
    def rs_weibo_object(self, result):
        print(" 未实现 --- rs_weibo_object")
        pass

    """
        微博列表数据回调方法
    """

    @abstractmethod
    def rs_weibo_list(self, result):
        print(" 未实现 --- rs_weibo_list")
        pass

    """
        单个评论对象抽象方法处理
    """

    @abstractmethod
    def rs_weibo_comments_object(self, pinglun, result_object):
        print(" 未实现 --- rs_weibo_comments_object")
        pass

    """
        抽象方法，当数据爬取完成之后会回调给子类去实现处理
        微博评论列表对象
    """

    @abstractmethod
    def rs_weibo_comments_list(self, pinglun_list, result_list):
        print(" 未实现 --- rs_weibo_comments_list")
        pass

    def get_headers(self, cookie_=default_cookie):
        ua = UserAgent()
        chrome = ua.chrome
        headers = {
            'User-Agent': chrome,
            'Cookie': cookie_
        }
        return headers

    def cn_process_user_info(self, user_id, reponse_append_data={}):
        url = self.base_url + "/" + user_id
        response = self.get_response(url)
        user_response = self.cn_process_user_response(response)
        user_response["用户主页"] = url
        return dict(user_response, **reponse_append_data)

        # 爬取用户信息 针对 weibo.cn

    def get_response(self, url):
        try:
            cookie = next(self.cookies_list)
        except StopIteration as e:
            self.cookies_list = weibo_login_user.gen_cookies()
            cookie = next(self.cookies_list)
        logging.info(" 获取 指定的URL : %s 对应的cookie_key : %s", url, cookie.get("username"))
        response = requests.get(url, headers=self.get_headers(cookie.get("cookie")))
        if response.status_code != 200:
            logging.error(" ERROR -  当前返回状态码 : %s , 以太过频繁处理 .. 开始休眠", response.status_code)
            sleep(5)
            return self.get_response(url)
        elif response.text.count("系统繁忙") > 0 or response.text.count("system error") > 0:
            logging.error(" ERROR - 当前返回系统繁忙, 需要休眠一段时间 ... 睡吧 ... ")
            sleep(5)
            return self.get_response(url)
        return response

    def cn_process_user_response(self, response):
        print("------------------------用户[{}]---------------------------".format(response.url))
        selector = Selector(response)
        htmlList = selector.xpath('/html/body/div[@class="u"]')
        user_id = ""
        try:
            allContent = str(htmlList.xpath("div//text()"))
            weibo = self.getDataText("微博", allContent)
            guanzhu = self.getDataText("关注", allContent)
            fensi = self.getDataText("粉丝", allContent)
            fenzu = self.getDataText("分组", allContent)
            weiboName = htmlList.xpath("table/tr/td/div/span[1]/text()[1]").get()
            renzheng = htmlList.xpath("table/tr/td/div/span[2]/text()").get()
            miaoshu = htmlList.xpath("table/tr/td/div/span[3]//text()").get()
            address = htmlList.xpath("table/tr/td/div/span[1]/text()[2]").get()
            user_id = re.findall("(\d+)/fans", selector.get())[0]
            print("用户编号 : {} 微博名称: {} 微博数 : {} 关注 : {} 粉丝 : {} 分组 : {} 认证 : {} 描述 : {} 性别地址 : {}".format(user_id,
                                                                                                         weiboName,
                                                                                                         weibo,
                                                                                                         guanzhu,
                                                                                                         fensi,
                                                                                                         fenzu,
                                                                                                         renzheng,
                                                                                                         miaoshu,
                                                                                                         address))
            response_object = self.cn_weibo_user_info(user_id)
            response_object[spiderConstants.group_type] = spiderConstants.weibo_user_info
            response_object["微博数"] = weibo
            response_object["关注"] = guanzhu
            response_object["粉丝"] = fensi
            response_object["分组"] = fenzu
            response_object["用户编号"] = user_id
            return self.rs_process_user(response_object)
        except Exception as e:

            # traceback.print_exc()
            logging.error("解析异常 : " + response.url + " 状态码 : " + response.status_code, e)

    """
        爬取用户信息
    """

    def cn_weibo_user_info(self, user_id):
        user_url = self.base_url + "/" + user_id + "/info"
        html_data = self.get_request(user_url)
        result_list = html_data.find_all(class_="tip")
        response_object = {}
        # 定义用户信息
        response_object[spiderConstants.group_type] = spiderConstants.weibo_user_info
        is_tag = False
        for result in result_list:
            if result.text == "基本信息":
                info_list = result.next_sibling.contents
                for info in info_list:
                    if type(info) == Tag:
                        continue
                    if str(info).startswith("标签") or str(info).lstrip() == "":
                        is_tag = True
                        continue
                    try:
                        content = str(info).replace("：", ":").split(":")
                        key = content[0]
                        value = content[1]
                        logging.info(" %s : %s", content[0], content[1])
                        response_object[key] = value
                    except Exception as e:
                        logging.info("---error-info-- %s", info)
                        logging.error("error - ", e)
                        traceback.print_exc()
            if result.text == "学习经历" or result.text == "工作经历":
                info_list = result.next_sibling.contents
                for info in info_list:
                    if type(info) == Tag:
                        continue
                    logging.info("%s : %s", result.text, str(info))
                    response_object[result.text] = str(info)
        if is_tag == True:
            response_object["标签"] = self.cn_user_tag(user_id)
        return self.rs_weibo_user_info(response_object)

    """
        获取用户标签
    """

    def cn_user_tag(self, user_id):
        tag_url = self.base_url + "/account/privacy/tags/?uid=" + user_id
        request = self.get_request(tag_url)
        user_tag_list = request.select("body > div:nth-child(7) > a")
        response_list = []
        for user_tag in user_tag_list:
            logging.info(" tag : %s", user_tag.text)
            response_list.append(user_tag.text)
        return response_list

    def get_request(self, tag_url):
        result = self.get_response(tag_url)
        return BeautifulSoup(result.text, features='lxml')

    def cn_process_weibo_by_single(self, weibo_no):
        url = self.base_url + "/comment/{}".format(weibo_no)
        result = self.get_request(url)
        content = result.find(attrs={"class", "ctt"}).text
        weibo_obj = result.find(attrs={"class": "pms", "id": "cmtfrm"}).previousSibling
        like = re.findall("赞\[\d+", str(weibo_obj.text))[0][2:]
        forward = re.findall("转发\[\d+", str(weibo_obj.text))[0][3:]
        comments = re.findall("评论\[\d+", str(weibo_obj.text))[0][3:]
        user_id = re.findall("uid=(\d+)", str(weibo_obj.contents))[0]
        push_time = self.reUtils.time_fix(str(result.find(attrs={"class": "ct"}).text).rstrip())
        user_url = self.base_url + "/" + user_id + "/info"
        yield self.weibo_data(comments, content, forward, like, push_time, "", user_id,
                              user_url, weibo_no)
        yield from self.cn_weibo_comments(weibo_no)
        print("=====================")

    def com_process_weibo_by_single(self, weibo_no, weibo_id, page_no=1, max_page_no=20):
        url = "https://weibo.com/aj/v6/comment/big"
        # ?ajwvr=6&id=4427778004439002" \
        #       "&page=1&filter=hot&from=singleWeiBo"
        cookie = "SINAGLOBAL=1751008789274.302.1548672475927; _s_tentry=www.techweb.com.cn; Apache=8969091951880.363.1564047653081; ULV=1564047653839:5:1:1:8969091951880.363.1564047653081:1557724148964; Ugrow-G0=589da022062e21d675f389ce54f2eae7; login_sid_t=c64015e20bed0459137a88888a05728c; cross_origin_proto=SSL; YF-Ugrow-SEO-G0=8e667ee9394bfc84054b8fa626d4b0dc; WBtopGlobal_register_version=307744aa77dd5677; YF-V5-G0=7e17aef9f70cd5c32099644f32a261c4; un=17621253557; wb_view_log=1920*10801; SCF=Amp0K_iWqOQXNBAacw3C0u_dVbzxhJVtBjTuuLjNPTIU87uTA7V-hdaCUmimZ0eGsCx_R39OkFVmzf7dPjcXmlo.; SUHB=010GTKUcTdXyuZ; wb_view_log_7319106842=1920*10801; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh4AB5YrNMTkU_5BT6Bd0d_5JpVF02NSozpeo-0SK-N; SUB=_2AkMq-grjdcPxrARSmfEUzG3qaI9H-jyZL2MVAn7uJhMyAxgv7gkFqSVutBF-XFkwZB34Wg8l7AY03azKohLr-hIy; WBStorage=384d9091c43a87a5|undefined; UOR=www.csdn.net,widget.weibo.com,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1571194344759%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; YF-Page-G0=536a03a0e34e2b3b4ccd2da6946dab22|1571194653|1571194362"
        params = {}
        params["id"] = "4427778004439002"
        params["page"] = page_no
        params["filter"] = "hot"
        params["from"] = "singleWeiBo"

        response = requests.get(url, params=params, headers=self.get_headers(cookie))
        json_result = response.json()
        html_json = json_result.get("data")
        count = html_json.get("count")
        html = html_json.get("html")
        soup = BeautifulSoup(html, features='lxml')
        list_con = soup.find_all(attrs={"node-type": "root_comment"})
        for obj in list_con:
            comment_id = obj.attrs['comment_id']
            wb_text = obj.find(attrs={"class": "WB_text"})
            user_info = wb_text.a
            username = user_info.text
            user_id = user_info.get("usercard").replace("id=", "")
            user_index = "https:" + user_info.get("href")
            content = wb_text.text
            content = content[content.index("：") + 1:].rstrip()

            push_time = obj.find(attrs={"class": "WB_from S_txt2"}).text
            like_count = obj.find(attrs={"node-type": "like_status"}).text
            like_count = self.reUtils.find_all("\d+", like_count, "0")

            huifu_object = obj.find(attrs={"action-type": "login"})
            huifu = "0"
            if huifu_object is not None:
                huifu = re.findall("\d+", huifu_object.text)[0]
            yield self.rs_comment_model(comment_id, content, like_count, push_time, user_id,
                                        user_index,
                                        username,
                                        weibo_id, huifu)
        page_no += 1
        if page_no < max_page_no:
            logging.info("开始爬起 第%s页面", page_no)
            sleep(2)
            yield from self.com_process_weibo_by_single("", "", page_no)

    """
        执行爬取微博页面
        response ： 页面返回信息
        is_collect_weibo_comments ： 是否收集用户的评论
    """

    def cn_process_weibo_by_all(self, response):
        print("------------------------微博[{}]---------------------------".format(response.url))
        selector = Selector(response)
        htmlList = selector.xpath('body/div[@class="c"]')
        try:
            for html in htmlList:
                if html.attrib.get('id'):
                    divContent = html.xpath('div//text()')
                    div1 = html.xpath("div[1]/span[@class='ctt']").getall()
                    div1string = str(div1)
                    _startIndex = '<span class="ctt">'
                    content = div1string[div1string.index(_startIndex) + len(_startIndex):div1string.index('</span>')]
                    div2 = html.xpath('div[2]/a').extract()
                    like = re.findall("赞\[\d+", str(divContent))[0][2:]
                    forward = re.findall("转发\[\d+", str(divContent))[0][3:]
                    comments = re.findall("评论\[\d+", str(divContent))[0][3:]
                    weibo_no = str(html.attrib.get('id')).replace("M_", "")
                    source = html.xpath("div/span[@class='ct']/text()")[0].root
                    sources = str(source).split("来自")
                    push_date = sources[0]
                    push_phone_type = sources[1]
                    user_id = re.findall("comment/.+?uid=(\d+\w+)", str(html.xpath("div/a").getall()))[0]
                    user_url = response.url
                    result_object = self.weibo_data(comments, content, forward, like, push_date, push_phone_type,
                                                    user_id,
                                                    user_url, weibo_no)
                    yield from self.rs_weibo_object(result_object)
                    print(" result : {} 赞 {} 转发 {} 评论 {}".format(content, like, forward, comments))
            nextUrl = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').get()
            page_no = re.findall("page=(\d+)", nextUrl)[0]
            base_next_url = self.base_url + nextUrl
            logging.info("准备爬取下一页 ： {}".format(base_next_url))
            yield scrapy.Request(base_next_url, callback=self.cn_process_weibo_by_all)
        except Exception as e:
            logging.error(e)

    def weibo_data(self, comments, content, forward, like, push_date, push_phone_type, user_id, user_url,
                   weibo_no):
        result_object = {}
        result_object["微博内容"] = content
        result_object["点赞"] = like
        result_object["评论"] = comments
        result_object["转发"] = forward
        result_object["微博编号"] = weibo_no
        result_object["用户主页"] = user_url
        result_object["用户编号"] = user_id
        result_object["发布时间"] = self.reUtils.time_fix(push_date.rstrip())
        result_object["手机型号"] = push_phone_type
        result_object[spiderConstants.group_type] = spiderConstants.weibo_weibo_info
        return result_object

    """
        爬取微博的评论信息
            weibo_id : 微博编号
            page : 当前页面
            max_page : 最大页面的元素,0表示一直爬下去
            is_collect_user_info : 是否收集评论的用户信息
    """

    def cn_weibo_comments(self, weibo_id, page=0, max_page=31, min_like_count=0):
        index_url = "https://weibo.cn/comment/hot/{}?page={}"
        url = index_url.format(weibo_id, page)
        html_data = self.get_request(url)
        pinglun_list = html_data.find_all(class_="c")
        result_list = []
        is_min_like = False
        for pinglun in pinglun_list:
            result_object = {}
            if 'id' in pinglun.attrs.keys() and pinglun.attrs["id"] != "M_":
                # print(pinglun)
                user_info = pinglun.a
                username = user_info.text
                user_index = self.base_url + user_info["href"]
                content = str(pinglun.find(class_="ctt"))
                _startIndex = '<span class="ctt">'
                content_text = content[content.index(_startIndex) + len(_startIndex):content.index('</span>')]
                dianzan = pinglun.find(class_="cc").text
                dianzan = self.reUtils.find_all_search("\d+", dianzan, 0)
                if int(dianzan) < min_like_count:
                    logging.info(" 点赞数为 : " + dianzan + " 不匹配收集规则")
                    is_min_like = True
                    continue
                source_address = pinglun.find(class_="ct").text
                source_array = str(source_address).split("来自")
                user_index[user_index.rindex("/") + 1:]
                user_id = user_index[user_index.rindex("/") + 1:]
                result_object = self.rs_comment_model("", content_text, dianzan, source_array[0], user_id, user_index,
                                                      username, weibo_id)
                logging.info(" 用户名 : %s 首页 : %s 评论内容 : %s 点赞: %s", username, user_index, content, dianzan)
                yield from self.rs_weibo_comments_object(pinglun, result_object)
        self.rs_weibo_comments_list(pinglun_list, result_list)
        # 开始爬取下一页
        next_obj = html_data.find(id="pagelist").form.div.a
        next_page = next_obj["href"]
        next_text = next_obj.text
        next_no = self.reUtils.find_all("page=(\d+)", next_page, 0)
        if next_text == "下页" and ((int(next_no) < max_page)):
            sleep(1)
            yield from self.cn_weibo_comments(weibo_id, next_no, min_like_count=min_like_count)

    def rs_comment_model(self, comment_id, content_text, dianzan, push_time, user_id, user_index, username,
                         weibo_id, huifu="0"):
        result_object = {}
        result_object[spiderConstants.group_type] = spiderConstants.weibo_comments_info
        result_object["评论编号"] = comment_id
        result_object["用户名"] = username
        result_object["用户首页"] = user_index
        result_object["评论内容"] = content_text
        result_object["点赞数"] = dianzan
        result_object["微博编号"] = weibo_id
        result_object["发布时间"] = self.reUtils.time_fix(push_time)
        # result_object["发布来源"] = source_array[1]
        result_object["用户编号"] = user_id
        result_object["回复数"] = huifu
        logging.info("微博评论 数据源 : %s", result_object)
        return result_object

    """
        获取查找页面关键字提取的元素
    """

    def com_get_mbloglist(self, is_collect_user_info=True):
        url = "https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_2788_-_ctg1_2788&from" \
              "=faxian_hot&mod=fenlei&pagebar={" \
              "}&tab=home&current_page=1&pre_page=1&page=1&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_2788_-_ctg1_2788&script_uri=/102803_ctg1_2788_-_ctg1_2788&feed_type=1&domain_op=102803_ctg1_2788_-_ctg1_2788&__rnd=1569220784826"
        logging.debug(" 关键字提取是否爬取用户信息 : %s", is_collect_user_info)
        start_index = 64
        while True:
            next_url = url.format(start_index)
            response = self.get_response(next_url)

            dataJson = response.json()
            data = dataJson["data"]
            htmlData = BeautifulSoup(data, features='lxml')
            weibo_list = htmlData.find_all(attrs={"action-type": "feed_list_item"})
            if len(weibo_list) == 0:
                print("数据被终结! 最终定格页码 :{} 返回结果 :{}".format(start_index, dataJson))
                break
            start_index = start_index + 1
            print("--------------------------------爬取第{}页数据------------------------".format(start_index))
            for weibo in weibo_list:
                try:
                    user_info = weibo.find(class_="W_f14 W_fb S_txt1")
                    username = user_info.text
                    user_index = user_info.attrs["href"]
                    user_index_response = requests.get(str(user_index).replace("com", "cn"), headers=self.get_headers())
                    content = str(weibo.find(class_="WB_text W_f14").text).strip()
                    pattern = "\d+";
                    zhuanfa = self.reUtils.find_all_search(pattern, weibo.find_all(class_="line S_line1")[1].text, 0)
                    pinglun = self.reUtils.find_all_search(pattern, weibo.find_all(class_="line S_line1")[2].text, 0)
                    dianzan = self.reUtils.find_all_search(pattern, weibo.find_all(class_="line S_line1")[3].text, 0)
                    if is_collect_user_info == True:
                        self.cn_process_user_response(user_index_response)
                    logging.info(
                        "发布人 : {} , 内容 : {} 转发 : {} ,评论 : {} 点赞 : {}".format(username, content, zhuanfa, pinglun,
                                                                             dianzan))
                except Exception as e:
                    traceback.print_exc()
                    print(e)

    # 根据数据查找文本值
    def getDataText(self, match, allContent):
        length = len(match) + 1
        return re.search("" + match + "\[\d+", allContent).group(0)[length:]

    def com_search_keyword(self, text, page=1, is_collect_user_info=True):
        url = "https://s.weibo.com/user?q={}&Refer=SUer_box&page={}".format(text, page)
        request = self.get_request(url)
        result_list = request.find_all(class_="card card-user-b s-pg16 s-brt1")
        logging.debug(" 是否爬取用户信息 : ", is_collect_user_info)
        for result in result_list:
            href_ = result.div.a["href"]
            user_id = re.findall("u/(.+)", href_)[0]
            if is_collect_user_info == True:
                self.cn_weibo_user_info(user_id)
        page = request.select("#pl_feed_main > div.m-con-l > div.m-page > div > a")[0]["href"]
        next_page = re.findall("page=(\d+)", page)[0]
        if page < int(next_page):
            self.com_search_keyword(text, next_page)
        else:
            logging.info(" 爬取完毕 : 一共爬取 -> %s", page)

# if __name__ == '__main__':
# weibo = DefaultWeiBoProcess()
# weibo.cn_weibo_comments("I7y5T2uV0", sleep_=1)
# weibo.cn_process_user_info("1684756320")
#
# weibo.cn_process_user_response(resp)
