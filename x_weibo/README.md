# 微博

## 环境

1. 首先最好是自己登陆完成之后，拿到Cookie到 [settings.py](./settings.py)中的DEFAULT_REQUEST_HEADERS进行配置



## 1. 启动类

x_weibo/spiders/weibo_run.py

## 2. 爬取微博的模版

`AbstractWeiBoProcess` : 类似java中的抽象类，解析所有数据，并将获取到的数据传递给指定的抽象方法。

- rs_process_user : 微博的完整的用户信息
- rs_weibo_user_info : 用户信息回调返回，不包含微博粉丝、关注、分组
- rs_weibo_object: 单条微博数据对象
- rs_weibo_list : 一整页的微博对象，也就是一页的微博列表
- rs_weibo_comments_object : 单条评论数据
- rs_weibo_comments_list : 单条微博的一页评论数据

**与scrapy结合使用**

`DefaultWeiBoProcess`: 默认的微博执行对象，继承父类`AbstractWeiBoProcess` ，将所有数据进行处理。

数据处理包含了数据的递归爬取

> 我爬取了一条微博信息，但是我想知道微博下面有哪些评论，评论的用户有哪些？



## 3. 存储

这里存储没有做过多的实现，只是将数据导出到excel中。

### 1. Excel

由于微博的里面的用户数据字段不全，有的人填写的信息不固定，所以就用了K/V形式存储，K为header，V为指定数据，一开始K不固定，后续往后追加。

参考类 : [excelUtils](../common/excelUtils.py)



