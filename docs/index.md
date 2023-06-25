# Banano Blog 后端项目需求规格说明书

- 服务器
  - Docker
  - Nginx
  - 域名、备案
- 后端服务
  - 数据库 MySQL
  - 缓存 Redis
  - COS
  - 邮件
  - 短信SMS

## 第二章 项目概述


### 2.1 项目描述

Banano 是一个博客网站，支持多作者，可以发表技术、生活类文章。可以评论，点赞，发表态度。

`Banano` 意为 `banana` + `xiao`，属于水果系列项目。

### 2.2 产品功能

V0.1.0 实现 PC端，包括个人中心、动态、文章、心情、私信、全站搜索、消息通知等，对外提供手机号注册。

V0.2.0 实现小程序端

![Blog 项目需求分析](C:/Users/diaoh/OneDrive/assets/img/%E5%8D%9A%E5%AE%A2%E7%BD%91%E7%AB%99%E5%90%8E%E7%AB%AF%E8%AE%BE%E8%AE%A1/Blog%20%E9%A1%B9%E7%9B%AE%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90.png)

## 第三章 业务需求

### 3.1 总体需求

*   前端

*   后台管理

*   登录可查看登录可见内容

*   撰稿者可发表文章

*   普通用户可评论、点赞、发表心情。

### 3.2 个人中心

#### 3.2.1 登录、注册

*   手机号注册

*   第三方微信注册（暂未实现）

*   手机号登录

*   微信登录（暂未实现）

*   重置密码

*   修改密码

#### 3.2.2 个人信息

*   昵称

*   手机号

*   头像

*   简介

*   城市

*   职位

*   等

    用户可更新。

#### 3.2.3 信息统计

用户发表文章数量、评论数量、心情数量、点赞数量。

### 3.3 首页动态

*   每页显示10条文章

*   每条文章包括标题、简介、头像、昵称、发表时间、点赞数、评论数、分类、标签

*   对于撰稿者发表文章显示编辑按钮

### 3.4 文章模块

#### 3.4.1 文章详情页

*   显示标题、头图、内容、昵称、头像、发布时间、点赞数、评论数、标签、分类

*   点赞区（是否给文章点赞）

*   评论区，作者可设置是否开启评论功能

#### 3.4.2 发表文章

*   必填字段：标题、头图（有默认）、内容、标签、分类

*   可发表或存为草稿

#### 3.4.3 评论文章

*   登录后发表评论

*   文章作者可屏蔽评论

### 3.5 心情模块

*   登录可见

*   发表心情

*   点赞心情

*   分享心情（到朋友圈）

### 3.6 全站搜索

文章、心情、标签、分类、用户进行搜索。

### 3.7 消息通知

*   点赞我的文章

*   评论我的文章

*   回复我的评论

*   点赞心情

*   回复心情

以上互动会触发消息通知机制。

显示未读消息，标记消息已读，标记所有消息已读。查看历史消息。

### 3.8 后台模块

#### 用户管理

*   查看所有用户

*   筛选用户

*   修改用户非关键信息（如昵称）

*   封禁用户

*   设置分组

*   分配权限

#### 文章管理

*   查看所有文章

*   筛选文章

*   推荐文章

*   隐藏文章

*   修改文章非关键信息（如所属分类、标签）

*   查看所有分类、标签、来源

*   新增分类

*   修改分类

*   删除分类

#### 评论管理

*   查看所有评论

*   按文章分类查询评论

*   隐藏评论

#### 心情管理

*   查看所有心情

*   隐藏心情

#### 通知管理

*   查看系统消息

*   发送系统消息

## 第四章 技术选型

使用 docker 容器化技术。

### 4.1 前台

vue 3.0 + Element Plus

### 4.2 后台

vue 3.0 + iview

### 4.2 后端

Flask + MySQL + Redis + Celery + Nginx + gunicorn + ElasticSearch

*   Flask 提供 API 服务

*   MySQL 数据持久化存储

*   Redis 缓存、计数和任务队列

*   Celery 定时和后台任务

*   阿里云短信服务 sms

*   ElasticSearch 搜索 TODO

*   SSE 实时消息 TODO

*   gunicorn

*   Nginx 反向代理、负载均衡和静态资源

*   Docker 容器化管理

*   其它三方库

## 第五章 数据库设计

没有特别说明则为 InnoDB 引擎 + utf8mb4 字符集。utf8mb4\_0900\_ai\_ci

### 用户基本信息表 user\_basic

| 字段名             | 类型         | 为空 | 唯一 | 默认值 | 注释                                       |
| ------------------ | ------------ | ---- | ---- | ------ | ------------------------------------------ |
| id                 | bigint       | 否   | 是   |        | 主键                                       |
| username           | varchar(32)  | 否   | 是   |        | 昵称                                       |
| signature          | varchar(100) | 是   | 否   |        | 个性签名                                   |
| avatar             | varchar(255) | 是   | 否   |        | 头像                                       |
| group\_id          | bigint       | 否   | 否   | 1      | 所属分组：1-普通用户，2-撰稿者，3-虚拟用户 |
| register\_source   | tinyint      | 否   | 否   | 1      | 注册来源：1-手机号，2-微信小程序           |
| mobile             | char(16)     | 是   | 是   | null   | 手机号，如果有，则唯一                     |
| mobile\_bind\_time | datetime     | 是   | 否   | null   | 手机号绑定时间                             |
| email              | varchar(100) | 是   | 是   | null   | 邮箱，如果有，则唯一                       |
| email\_bind\_time  | datetime     | 是   | 否   | null   | 邮箱绑定时间                               |
| status             | tinyint      | 否   | 否   | 1      | 状态：0-封禁，1-可用                       |
| last\_login        | datetime     | 是   | 否   |        | 最后登录时间                               |
| article\_count     | int          | 否   | 否   | 0      | 发表文章数量                               |
| like\_count        | int          | 否   | 否   | 0      | 获得点赞数量                               |
| is\_deleted        | tinyint      | 否   | 否   | 0      | 是否删除：0-没有，1-已删除                 |

唯一约束：mobile 和 is\_deleted、username 和 is\_deleted、emial 和 is\_deleted。

### 用户其他信息 user\_profile

| 字段名       | 类型         | 为空 | 唯一 | 默认值 | 注释                       |
| ------------ | ------------ | ---- | ---- | ------ | -------------------------- |
| user\_id     | bigint       | 否   | 是   |        | user\_basic 的id，1对1     |
| gender       | tinyint      | 否   | 否   | 0      | 性别：0-未设置，1-女，2-男 |
| birthday     | date         | 是   | 否   |        | 生日                       |
| address      | varchar(100) | 否   | 否   | ''     | 所在地                     |
| company      | varchar(20)  | 是   | 否   |        | 公司                       |
| career       | varchar(20)  | 是   | 否   |        | 职业                       |
| create\_time | datetime     | 否   | 否   | now    | 创建时间                   |
| update\_time | datetime     | 否   | 否   | now    | 修改时间                   |

### 用户授权表 user\_auth

| 字段名         | 类型         | 为空 | 唯一 | 默认值 | 注释                                                 |
| -------------- | ------------ | ---- | ---- | ------ | ---------------------------------------------------- |
| id             | bigint       | 否   | 是   |        | 主键                                                 |
| user\_id       | bigint       | 否   | 否   |        | 用户基本信息表id                                     |
| identity\_type | tinyint      | 否   | 否   | 1      | 登录类型：1-手机号密码，2-手机号验证码，3-微信小程序 |
| identifier     | varchar(50)  | 否   | 否   |        | 唯一标识：手机号或 app\_id                           |
| certificate    | varchar(200) | 否   | 否   |        | 凭证：密码或 token                                   |
| create\_time   | datetime     | 否   | 否   | now    | 创建时间                                             |
| update\_time   | datetime     | 否   | 否   | now    | 修改时间                                             |
| is\_deleted    | tinyint      | 否   | 否   | 0      | 是否删除：0-没有，1-已删除                           |

唯一约束：

*   uid、identity\_type、is\_deleted

*   identifier、is\_deleted

### 分组 group

| 字段名       | 类型         | 为空 | 唯一 | 默认值 | 注释                 |
| ------------ | ------------ | ---- | ---- | ------ | -------------------- |
| id           | bigint       | 否   | 是   |        | 主键                 |
| name         | varchar(32)  | 否   | 是   |        | 分组名称             |
| info         | varchar(255) | 是   | 否   |        | 分组说明             |
| create\_time | datetime     | 否   | 否   | now    | 创建时间             |
| update\_time | datetime     | 否   | 否   | now    | 修改时间             |
| status       | tinyint      | 否   | 否   | 1      | 状态：1-有效，2-无效 |

目前设计每个用户只能属于一个分组，当前系统默认分组为：1-普通用户，2-撰稿者，3-虚拟用户。

### 权限 permission

| 字段名       | 类型         | 为空 | 唯一 | 默认值    | 注释                           |
| ------------ | ------------ | ---- | ---- | --------- | ------------------------------ |
| id           | int          | 否   | 是   |           | 主键                           |
| name         | varchar(32)  | 否   | 是   |           | 权限名称                       |
| module       | varchar(32)  | 否   | 否   | 'default' | 权限所属模块，用于分组查看权限 |
| info         | varchar(100) | 是   | 否   |           | 权限说明                       |
| create\_time | datetime     | 否   | 否   | now       | 创建时间                       |
| update\_time | datetime     | 否   | 否   | now       | 修改时间                       |

目前权限级别为函数级别。

### 分组权限 group\_permission

| 字段名         | 类型     | 为空 | 唯一 | 默认值 | 注释     |
| -------------- | -------- | ---- | ---- | ------ | -------- |
| id             | bigint   | 否   | 是   |        | 主键     |
| group\_id      | bigint   | 否   | 否   |        | 分组id   |
| permission\_id | bigint   | 否   | 否   |        | 权限id   |
| create\_time   | datetime | 否   | 否   | now    | 创建时间 |

### 文章分类 category

| 字段名       | 类型         | 为空 | 唯一 | 默认值  | 注释                       |
| ------------ | ------------ | ---- | ---- | ------- | -------------------------- |
| id           | bigint       | 否   | 是   |         | 主键                       |
| name         | varchar(32)  | 否   | 否   |         | 文章分类名称               |
| info         | varchar(255) | 是   | 否   |         | 分类说明                   |
| banner       | varchar(255) | 是   | 否   | default | 分类背景图                 |
| sort         | int          | 否   | 否   | 1       | 序号                       |
| is\_visible  | tinyint      | 否   | 否   | 1       | 是否可见：1-可见，0-不可见 |
| create\_time | datetime     | 否   | 否   | now     | 创建时间                   |
| update\_time | datetime     | 否   | 否   | now     | 修改时间                   |
| is\_deleted  | tinyint      | 否   | 否   | 0       | 是否删除：0-没有，1-已删除 |

唯一约束：

*   name 和 is\_deleted

### 文章标签 tag

| 字段名       | 类型        | 为空 | 唯一 | 默认值 | 注释     |
| ------------ | ----------- | ---- | ---- | ------ | -------- |
| id           | bigint      | 否   | 是   |        | 主键     |
| name         | varchar(32) | 否   | 是   |        | 标签名称 |
| color        | varchar(32) | 是   | 否   |        | 文字颜色 |
| bg           | varchar(32) | 是   | 否   |        | 背景颜色 |
| create\_time | datetime    | 否   | 否   | now    | 创建时间 |

### 文章来源 source （使用 Enum 代替）

| 字段名       | 类型        | 为空 | 唯一 | 默认值 | 注释     |
| ------------ | ----------- | ---- | ---- | ------ | -------- |
| id           | int         | 否   | 是   |        | 主键     |
| name         | varchar(32) | 否   | 是   |        | 来源名称 |
| create\_time | datetime    | 否   | 否   | now    | 创建时间 |
| update\_time | datetime    | 否   | 否   | now    | 修改时间 |

来源：1-原创，2-转载，3-翻译

```python
from Enum import IntEnum

class Source(IntEnum):
    ORIGIN = 1  # 原创
    REPRINTS = 2  # 转载
    TRANSLATION = 3  # 翻译
```

### 文章 article

| 字段名          | 类型         | 为空 | 唯一 | 默认值            | 注释                             |
| --------------- | ------------ | ---- | ---- | ----------------- | -------------------------------- |
| id              | bigint       | 否   | 是   |                   | 文章ID                           |
| title           | varchar(128) | 否   | 是   |                   | 标题                             |
| summary         | varchar(255) | 是   | 否   |                   | 摘要                             |
| cover           | varchar(255) | 否   | 否   | article/cover.png | 封面                             |
| category\_id    | int          | 是   | 否   | null              | 分类id，null 表示默认分类        |
| source\_id      | int          |      |      |                   | 来源id：1-原创，2-转载，3-翻译   |
| tags            | varchar(255) | 是   | 否   |                   | 标签 id，使用 , 分割             |
| publish         | tinyint      | 否   |      | 1                 | 1-公开，2-登录可见，3-仅自己可见 |
| status          | int          |      |      |                   | 1-正常，2-拉黑，3-推荐           |
| order           | tinyint      | 否   | 否   | 1                 | 排序                             |
| comment\_status | tinyint      | 否   | 否   | 1                 | 是否开启评论：1-开启，0-关闭     |
| user\_id        | bigint       | 否   | 否   |                   | 作者 id                          |
| create\_time    | datetime     | 否   | 否   | now               | 创建时间                         |
| update\_time    | datetime     | 否   | 否   | now               | 修改时间                         |
| delete\_time    | datetime     | 是   | 否   | null              | 删除时间                         |

唯一索引：

*   title 和 delete\_time

### 文章内容 article\_content

| 字段名      | 类型     | 为空 | 唯一 | 默认值 | 注释     |
| ----------- | -------- | ---- | ---- | ------ | -------- |
| article\_id | bigint   | 否   | 是   |        | 文章ID   |
| content     | longtext | 否   | 否   |        | 文章内容 |

说明：

*   MyISAM 引擎

### 文章统计 article\_statistic

| 字段名         | 类型   | 为空 | 唯一 | 默认值 | 注释   |
| -------------- | ------ | ---- | ---- | ------ | ------ |
| article\_id    | bigint | 否   | 是   |        | 文章ID |
| view\_count    | int    | 否   | 否   | 0      | 浏览量 |
| like\_count    | int    | 否   | 否   | 0      | 点赞数 |
| comment\_count | int    | 否   | 否   | 0      | 评论数 |

用户文章态度 user\_article\_attitude

| 字段名       | 类型     | 为空 | 唯一 | 默认值 | 注释                   |
| ------------ | -------- | ---- | ---- | ------ | ---------------------- |
| id           | bigint   | 否   | 是   |        | 主键                   |
| user\_id     | bigint   | 否   | 否   |        | 用户id                 |
| subject\_id  | bigint   | 否   | 否   |        | 主题id（文章id）       |
| attitude     | tinyint  | 否   | 否   | 1      | 态度：1-喜欢，0-不喜欢 |
| create\_time | datetime | 否   | 否   | now    | 创建时间               |
| update\_time | datetime | 否   | 否   | now    | 修改时间               |

暂时没有设置不喜欢，只记录点赞，如果取消点赞则删除记录。

### 上传文件 file

| 字段名       | 类型         | 为空 | 唯一 | 默认值 | 注释                                     |
| ------------ | ------------ | ---- | ---- | ------ | ---------------------------------------- |
| id           | bigint       | 否   | 是   |        | 主键                                     |
| md5          | varchar(255) | 否   | 是   |        | 唯一标识                                 |
| user\_id     | bigint       | 否   | 否   |        | 上传用户id                               |
| path         | varchar(255) | 否   | 是   |        | 文件路径或url                            |
| location     | tinyint      | 否   | 否   | 1      | 存储位置：1-本地，2-远程                 |
| type         | tinyint      | 否   | 否   | 1      | 文件类型：1-未知，2-图片，3-视频，4-音频 |
| name         | varchar(255) | 否   | 否   |        | 文件名称                                 |
| create\_time | datetime     | 否   | 否   | now    | 创建时间                                 |
| update\_time | datetime     | 否   | 否   | now    | 修改时间                                 |

### 主题-评论 subject\_comment

评论系统可以对应不同主题：文章评论、页面评论、说说评论等。此表主要存储统计信息。

| 段名          | 类型    | 为空 | 唯一 | 默认值 | 注释                                    |
| ------------- | ------- | ---- | ---- | ------ | --------------------------------------- |
| id            | bigint  | 否   | 是   |        | 主键                                    |
| subject\_id   | bigint  | 否   | 否   |        | 主题 id，如 article\_id                 |
| subject\_type | tinyint | 否   | 否   |        | 主题类型：1-article，2-page，3-shuoshuo |
| member\_id    | int     | 是   | 否   |        | 所属用户 id，页面没有，                 |
| count         | int     | 否   | 否   | 0      | 评论总数（包括删除的、隐藏的）          |
| root\_count   | int     | 否   | 否   | 0      | 根评论总数，直接对文章的评论            |
| all\_count    | int     | 否   | 否   | 0      | 评论和回复总数                          |

### 评论 comment

真正的评论列表。

| 段名         | 类型     | 为空 | 唯一 | 默认值 | 注释                                                     |
| ------------ | -------- | ---- | ---- | ------ | -------------------------------------------------------- |
| id           | bigint   | 否   | 是   |        | 主键                                                     |
| sub\_id      | bigint   | 否   | 否   |        | 主题 id，如 article\_id                                  |
| sub\_type    | tinyint  | 否   | 否   |        | 主题类型：1-article，2-page，3-shuoshuo                  |
| user\_id     | bigint   | 是   | 否   |        | 用户 id                                                  |
| root\_id     | int      | 否   | 否   | 0      | 0表示根评论，不为0表示回复所对应的最顶层的评论（根评论） |
| parent\_id   | int      | 否   | 否   | 0      | 0也表示这是根评论，不为0表示回复的对象                   |
| like\_count  | int      | 否   | 否   | 0      | 点赞数                                                   |
| status       | tinyint  | 否   | 否   | 1      | 状态：1-正常，2-隐藏，3-作者置顶，4-后台置顶             |
| create\_time | datetime | 否   | 否   | now    | 创建时间                                                 |
| is\_deleted  | tinyint  | 否   | 否   | 1      | 是否删除：1-没有，0-已删除                               |

### 评论内容 comment\_content

将评论内容单独抽离。

| 字段名      | 类型         | 为空 | 唯一 | 默认值 | 注释                   |
| ----------- | ------------ | ---- | ---- | ------ | ---------------------- |
| comment\_id | int          | 否   | 是   |        | 主键,1对1comment的id   |
| ip          | varchar(16)  |      |      |        | 评论者 ip 地址         |
| platform    | varchar(50)  |      |      |        | 评论者使用客户端       |
| device      | varchar(50)  |      |      |        | 评论者使用系统         |
| content     | varchar(400) |      |      |        | 评论内容               |
| meta        | varchar(100) |      |      |        | 评论元数据：背景、文字 |

三者的缓存：comment\_subject设置为 string 类型（24h）；comment 设置为 sorted set 类型（8h）；comment\_content设置为 string 类型（24h）。

### 评论点赞 comment\_like

| 字段名       | 类型     | 为空 | 唯一 | 默认值 | 注释                           |
| ------------ | -------- | ---- | ---- | ------ | ------------------------------ |
| id           | bigint   | 否   | 是   |        | 主键id                         |
| user\_id     | bigint   | 否   | 否   |        | 用户id                         |
| comment\_id  | bigint   | 否   | 否   |        | 评论id                         |
| is\_deleted  | tinyint  | 否   | 否   | 0      | 是否取消点赞：0-没有，1-已取消 |
| create\_time | datetime | 否   | 否   | now    | 创建时间                       |
| update\_time | datetime | 否   | 否   | now    | 修改时间                       |

### 说说 sign  暂不实现

| 字段名          | 类型     | 为空 | 唯一 | 默认值 | 注释                                       |
| --------------- | -------- | ---- | ---- | ------ | ------------------------------------------ |
| id              | int      | 否   | 是   |        | 主键                                       |
| content         | str      | 否   | 否   |        | 通知内容                                   |
| user\_id        | int      | 否   | 否   |        | 所属用户                                   |
| like\_num       | int      | 否   | 否   | 0      | 点赞数                                     |
| publish         | tinyint  | 否   | 否   | 1      | 公开范围：1-公开，2-登录可见，3-仅自己可见 |
| status          | tinyint  | 否   | 否   | 1      | 说说状态：1-正常，2-拉黑，3-置顶           |
| comment\_status | tinyint  | 否   | 否   | 1      | 评论是否开启：1-开启，2-关闭               |
| order           | tinyint  | 否   | 否   | 1      | 置顶时的排序标准                           |
| create\_time    | datetime | 否   | 否   | now    | 创建时间                                   |
| update\_time    | datetime | 否   | 否   | now    | 修改时间                                   |
| delete\_time    | datetime | 是   | 否   | null   | 删除时间                                   |

暂时不实现类似微博的图片显示，可在正文中按照Markdown语法插入。

### 通知 notice

| 字段名         | 类型         | 为空 | 唯一 | 默认值 | 注释               |
| -------------- | ------------ | ---- | ---- | ------ | ------------------ |
| id             | bigint       | 否   | 是   |        | ID                 |
| content        | varchar(200) |      |      |        | 通知内容           |
| to\_user\_id   | int          |      |      |        | 发送对象           |
| from\_user\_id | int          |      |      |        | 发送人，0-系统消息 |
| is\_read       | smallint     |      |      | 0      | 0-未读，1-已读     |
| read\_time     | date         |      |      |        | 读取时间           |
| create\_time   | datetime     | 否   | 否   | now    | 创建时间           |

### 管理员用户 admin

| 字段名   | 类型         | 为空 | 唯一 | 默认值 | 注释           |
| -------- | ------------ | ---- | ---- | ------ | -------------- |
| id       | bigint       | 否   | 是   |        | 主键ID         |
| username | varchar(32)  | 否   | 是   |        | 管理员登录账户 |
| password | varchar(255) | 否   | 否   |        | 密码           |
| name     | varchar(32)  | 否   | 是   |        | 管理员名称     |
| email    | varchar(100) |      |      |        | 电子邮箱       |
| mobile   | varchar(16)  |      |      |        | 手机           |

目前只有一个管理员，后期扩展分组、分权限。

### 管理员操作日志 admin\_operation\_log

| 字段名       | 类型         | 为空 | 唯一 | 默认值 | 注释     |
| ------------ | ------------ | ---- | ---- | ------ | -------- |
| id           | bigint       | 否   | 是   |        | 主键ID   |
| admin\_id    | bigint       | 否   | 否   |        | 管理员id |
| ip           | varchar(16)  | 否   |      |        | ip地址   |
| operation    | varchar(50)  |      |      |        | 操作     |
| info         | varchar(200) |      |      |        | 描述     |
| create\_time | datetime     | 否   |      | now    | 创建时间 |

### 统计数据 admin\_statistics\_basic

| 字段名     | 类型     | 为空 | 唯一 | 默认值 | 注释               |
| ---------- | -------- | ---- | ---- | ------ | ------------------ |
| id         | bigint   | 否   | 是   |        | 主键ID             |
| year       | smallint | 否   | 否   |        | 年                 |
| month      | tinyint  | 否   | 否   |        | 月                 |
| day        | tinyint  | 否   | 否   |        | 日                 |
| hour       | tinyint  | 否   | 否   |        | 时                 |
| type       | tinyint  | 否   | 否   |        | 统计类型：0-文章数 |
| count      | bigint   | 否   | 否   | 0      | 数量               |
| date\_time | datetime | 否   | 否   |        | 与上方一致         |

## 第六章 API 设计

### 用户相关

#### 获取验证码

**描述：**

*   通过手机号获取验证码，可用于注册、登录、找回密码、重置密码等。

**请求url：**

*   `/api/user/code`

**请求方式:**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型   | 说明                                       |
| :----- | :--- | :----- | ------------------------------------------ |
| mobile | 是   | string | 手机号                                     |
| typ    | 是   | string | 验证码类型，register, login, forget, reset |

**返回：**

```json
{
    "code": 200,
    "error_code": 0,
    'msg': '请填写接收到的验证码'
}
```

**返回参数说明：**

无

#### 查看是否已存在昵称

**描述：**

*   注册时填写昵称自动查验是否合规以及是否存在。

**请求url：**

*   `/api/user/name`

**请求方式:**

*   `GET`

**参数：**

| 参数名   | 必选 | 类型   | 说明 |
| :------- | :--- | :----- | ---- |
| username | 是   | string | 昵称 |

**返回：**

```json
{
    "is_valid": True
}
```

**返回参数说明：**

*   is\_valid: 昵称是否符合规范：字数4-20之间，只能是字母数字和汉字，数据库是否已经存在等。

#### 注册

**描述：**

*   通过手机号注册。

**请求url：**

*   `/api/user/register`

**请求方式:**

*   `POST`

**参数：**

| 参数名    | 必选 | 类型   | 说明                                                                             |
| :-------- | :--- | :----- | -------------------------------------------------------------------------------- |
| mobile    | 是   | string | 手机号                                                                           |
| password  | 是   | string | 密码，大小写字母和数字以及特殊符号\_\*&^%\$#@!.,? 等且至少单三种，位数在6-18之间 |
| password2 | 是   | string | 验证密码                                                                         |
| code      | 是   | stirng | 验证码                                                                           |
| username  | 是   | string | 用户昵称                                                                         |

**返回：**

```json
{
    "code": 200,
    "error_code": 0,
    'msg': '注册成功'
}
```

**返回参数说明：**

无

#### 登录

**描述：**

*   通过手机号登录。

**请求url：**

*   `/api/user/login`

**请求方式:**

*   `POST`

**参数：**

| 参数名      | 必选 | 类型   | 说明                                   |
| :---------- | :--- | :----- | -------------------------------------- |
| mobile      | 是   | string | 手机号                                 |
| typ         | 是   | int    | 验证类型：1-手机号密码，2-手机号验证码 |
| certificate | 是   | string | 凭证：密码或验证码                     |

**返回：**

错误

```json
{
    "code": 400,
    "error_code": 1001X,
    'msg': '信息有误'
}
```

成功

```json
{
    'access_token': 'XXX',
    'refresh_token': 'XXX'
}
```

**返回参数说明：**

无

#### 找回密码

**描述：**

*   手机号找回密码接口。

**请求URL：**

*   `/api/user/forget`

**请求方式：**

*   `POST`

**参数：**

| 参数名    | 必选 | 类型   | 说明       |
| :-------- | :--- | :----- | ---------- |
| phone     | 是   | string | 手机号     |
| code      | 是   | string | 验证码     |
| password  | 是   | string | 新密码     |
| password2 | 是   | string | 确认新密码 |

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "密码修改成功",
}
```

**返回参数说明：**

无

#### 修改密码

**描述：**

*   修改密码接口。需登录。

**请求URL：**

*   `/api/user/reset`

**请求方式：**

*   `POST`

**参数：**

| 参数名        | 必选 | 类型   | 说明       |
| :------------ | :--- | :----- | ---------- |
| old\_password | 是   | string | 原密码     |
| password      | 是   | string | 新密码     |
| password2     | 是   | string | 确认新密码 |

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "密码修改成功",
}
```

**返回参数说明：**

无

#### 修改个人基本信息

**描述：**

*   修改个人信息（不包括头像）接口。需登录。

**请求URL：**

*   `/api/user/info`

**请求方式：**

*   `PUT`

**参数：**

| 参数名    | 必选 | 类型   | 说明                        |
| :-------- | :--- | :----- | --------------------------- |
| username  | 是   | string | 昵称                        |
| gender    | 是   | int    | 性别，1-女，2-男            |
| birthday  | 是   | string | 生日，'2021-01-01 12:12:12' |
| email     | 否   | string |                             |
| address   | 是   | string | 地址                        |
| signature | 否   | string | 个人简介                    |

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "个人信息修改成功",
}
```

**返回参数说明：**

无

#### 修改头像

**描述：**

*   修改自己的头像接口。需登录。

**请求URL：**

*   `/api/user/avatar`

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型 | 说明 |
| :----- | :--- | :--- | ---- |
| avatar | 是   | File | 文件 |

```js
const form = new FormData()
form.append('file', File)
/* File 格式 */
```

**返回：**

```json
 {
     "name": "file.png",
     "url": "http://example.com/path/to"
 }

```

**返回参数说明：**

无

#### 修改绑定的手机号

**描述：**

*   更换绑定的手机号。需登录。

**请求URL：**

*   `/api/user/mobile`

**请求方式：**

*   `POST` 验证旧手机

*   `PUT` 绑定新手机

主要逻辑是先验证旧手机，并在redis 中标记目前可绑定新手机，再通过新手机和验证码换绑。

**参数：**

`POST` 标记接下来要更换手机号

| 参数名 | 必选 | 类型   | 说明   |
| :----- | :--- | :----- | ------ |
| mobile | 是   | string | 手机号 |
| code   | 是   | string | 验证码 |

`PUT` post 成功后，再发起 PUT请求，验证新手机号和验证码信息，正确则绑定，并退出当前登录（前端操作）。

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| mobile | 是   | string | 新手机号 |
| code   | 是   | string | 验证码   |

**返回：**

post成功返回

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "请绑定新的手机号",
}
```

put 成功返回

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "手机号换绑成功",
}
```

**返回参数说明：**

无

#### 修改或新增绑定邮箱

**描述：**

*   新增或更换绑定的邮箱。需登录。需要先验证手机号

**请求URL：**

*   `/api/user/email`

**请求方式：**

*   `POST` 验证手机号

*   `PUT` 绑定新邮箱

与换绑手机号一样，先post请求验证手机号，确定有权限修改。

**参数：**

| 参数名 | 必选 | 类型   | 说明   |
| :----- | :--- | :----- | ------ |
| email  | 是   | string | 邮箱   |
| code   | 是   | string | 验证码 |

#### 获取登录后信息

**描述：**

*   用户**登录**后请求获得自己个人信息。

**请求URL：**

*   `/api/user/info`

**请求方式：**

*   `GET`

**参数：**

无，header 需设置 Authentication

**返回：**

```json
{
    "username": "xiao",
    "mobile": "1234567",
    "mobile_bind_time": '2021-01-01 12:12:12',
    "email": "example@xiao.com",
    "email_bind_time": '2021-01-01 12:12:12',
    "avatar": "https://xxx.xxx.xx/static/image/avatar.png",
    "origin_avatar": "https://xxx.xxx.xx/static/image/avatar.png",
    "gender": "1",
    "birthday": "2020-01-01",
    "address": "Hello World",
    "signature": "坚定",
    "group": 1,
}
```

**返回参数说明：**

*   gender: 1-女，2-男。

*   group：所属分组

*   origin\_avatar 原始头像

*   avatar 裁剪压缩后头像

#### 获取他人信息

**描述：**

*   用户获得他人信息。常用于访问个人主页时。

**请求URL：**

*   `/api/user/<int:id>/info`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明   |
| :----- | :--- | :--- | ------ |
| id     | 是   | int  | 用户id |

**返回：**

```json
{
    "username": "xiao",
    "mobile": "1234567",
    "mobile_bind_time": '2021-01-01 12:12:12',
    "email": "example@xiao.com",
    "email_bind_time": '2021-01-01 12:12:12',
    "avatar": "https://xxx.xxx.xx/static/image/avatar.png",
    "origin_avatar": "https://xxx.xxx.xx/static/image/avatar.png",
    "gender": "1",
    "birthday": "2020-01-01",
    "address": "Hello World",
    "signature": "坚定",
    "group": 1,
}
```

**返回参数说明：**

*   gender: 1-女，2-男。

*   group：所属分组

*   origin\_avatar 原始头像

*   avatar 裁剪压缩后头像

#### 用户文章

**描述：**

*   获得自己或他人文章列表。常用于访问个人主页时。

**请求URL：**

*   `/api/user/<int:id>/article`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明   |
| :----- | :--- | :--- | ------ |
| id     | 是   | int  | 用户id |

**返回：**

```json
[{
    "id": 1,
    "title": "标题",
    "content": "markdown 格式正文",
    "summary": "简介",
    "cover": "文章头图",
    "category": {
        "id": 1,
        "name": "分类名称"
    },
    "source": {
        "id": 1,
        "name": "来源名称"
    },
    "tags": [{
        "id": 1,
        "name": "tag 名称"
    }],
    "publish": 1,
    "user": {
        "id": 1,
        "username": "xiao",
        "avatar": "头像 url"
    },
    "status": 1,
    "view_nums": 0,
    "like_num": 0,
    "sort": 1,
    "comment_status": 1,
    "create_time": "2021-01-01 12:12:12",
    "update_time": "2021-03-03 12:12:12"
}]
```

**返回参数说明：**

*   publish 可见范围 1-公开，2-登录可见，3-仅自己可见

*   status 文章状态，1-正常，2-拉黑，3-推荐

*   view\_num 浏览量

*   like\_num 点赞量

*   sort 推荐排序时候使用

*   comment\_status 文章评论开关，1-开启，2-关闭。

#### 获得点赞文章

**描述：**

*   获得自己或他人点赞文章列表。常用于访问个人主页时。

*   is\_like 用户登录时会检查自己是否点赞

**请求URL：**

*   `/api/user/<int:id>/article/like`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明   |
| :----- | :--- | :--- | ------ |
| id     | 是   | int  | 用户id |

**返回：**

```json
[{
    "id": 1,
    "title": "标题",
    "content": "markdown 格式正文",
    "summary": "简介",
    "cover": "文章头图",
    "category": {
        "id": 1,
        "name": "分类名称"
    },
    "source": {
        "id": 1,
        "name": "来源名称"
    },
    "tags": [{
        "id": 1,
        "name": "tag 名称"
    }],
    "publish": 1,
    "user": {
        "id": 1,
        "username": "xiao",
        "avatar": "头像 url"
    },
    "status": 1,
    "view_nums": 0,
    "like_num": 0,
    "sort": 1,
    "comment_status": 1,
    "create_time": "2021-01-01 12:12:12",
    "update_time": "2021-03-03 12:12:12",
    "is_like": True
}]
```

**返回参数说明：**

*   publish 可见范围 1-公开，2-登录可见，3-仅自己可见

*   status 文章状态，1-正常，2-拉黑，3-推荐

*   view\_num 浏览量

*   like\_num 点赞量

*   sort 推荐排序时候使用

*   comment\_status 文章评论开关，1-开启，2-关闭。

*   is\_like 用户登录时会检查自己是否点赞

#### 用户说说

**描述：**

*   获得自己或他人说说列表。常用于访问个人主页时。

**请求URL：**

*   `/api/user/<int:id>/sign`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明   |
| :----- | :--- | :--- | ------ |
| id     | 是   | int  | 用户id |

**返回：**

```json
[{
    "id": 1,
    "content": "markdown 格式正文",
    "publish": 1,
    "user": {
        "id": 1,
        "username": "xiao",
        "avatar": "头像 url"
    },
    "status": 1,
    "like_num": 0,
    "sort": 1,
    "comment_status": 2,
    "create_time": "2021-01-01 12:12:12",
    "update_time": "2021-03-03 12:12:12",
    "is_like": True
}]
```

**返回参数说明：**

*   publish 可见范围 1-公开，2-登录可见，3-仅自己可见

*   status 文章状态，1-正常，2-拉黑，3-推荐

*   like\_num 点赞量

*   sort 推荐排序时候使用

*   comment\_status 文章评论开关，1-开启，2-关闭。暂时不开放评论。

*   is\_like 用户登录时会检查自己是否点赞

### 文章相关

#### 文章列表

**描述：**

*   获得所有文章列表接口。登录可查看隐藏文章。支持分页、分类、分标签查询。

**请求URL：**

*   `/api/article`

**请求方式：**

*   `GET`

**参数：**

| 参数名   | 必选 | 类型 | 说明                    |
| :------- | :--- | :--- | ----------------------- |
| start    | 否   | int  | 开始页数，默认为1       |
| count    | 否   | int  | 每页条数，默认20        |
| category | 否   | int  | 分类，默认0（全部分类） |
| tag      | 否   | int  | 标签，默认0（所有标签） |

**返回：**

```json
[{
    "id": 1,
    "title": "标题",
    "content": "markdown 格式正文",
    "summary": "简介",
    "cover": "文章头图",
    "category": {
        "id": 1,
        "name": "分类名称"
    },
    "source": {
        "id": 1,
        "name": "来源名称"
    },
    "tags": [{
        "id": 1,
        "name": "tag 名称"
    }],
    "publish": 1,
    "user": {
        "id": 1,
        "username": "xiao",
        "avatar": "头像 url"
    },
    "status": 1,
    "view_nums": 0,
    "like_num": 0,
    "sort": 1,
    "comment_status": 1,
    "create_time": "2021-01-01 12:12:12",
    "update_time": "2021-03-03 12:12:12"
}]
```

**返回参数说明：**

*   publish 可见范围 1-公开，2-登录可见，3-仅自己可见

*   status 文章状态，1-正常，2-拉黑，3-推荐

*   view\_num 浏览量

*   like\_num 点赞量

*   sort 推荐排序时候使用

*   comment\_status 文章评论开关，1-开启，2-关闭。

TODO 要不要在列表中添加 content 字段？添加的话在访问文章详情可以直接显示，但会额外浪费流量，且如果缓存在 redis 也会造成存储压力。

#### 文章详情

**描述：**

*   获得文章详情接口。登录可查看隐藏文章。

**请求URL：**

*   `/api/article/<int:id>`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "id": 1,
    "title": "标题",
    "content": "markdown 格式正文",
    "summary": "简介",
    "cover": "文章头图",
    "category": {
        "id": 1,
        "name": "分类名称"
    },
    "source": {
        "id": 1,
        "name": "来源名称"
    },
    "tags": [{
        "id": 1,
        "name": "tag 名称"
    }],
    "publish": 1,
    "user": {
        "id": 1,
        "username": "xiao",
        "avatar": "头像 url"
    },
    "status": 1,
    "view_nums": 0,
    "like_num": 0,
    "sort": 1,
    "comment_status": 1,
    "create_time": "2021-01-01 12:12:12",
    "update_time": "2021-03-03 12:12:12"
}
```

**返回参数说明：**

*   publish 可见范围 1-公开，2-登录可见，3-仅自己可见

*   status 文章状态，1-正常，2-拉黑，3-推荐

*   view\_num 浏览量

*   like\_num 点赞量

*   sort 推荐排序时候使用

*   comment\_status 文章评论开关，1-开启，2-关闭。

#### 发表文章

**描述：**

*   发表文章接口。需要成为撰稿者。

**请求URL：**

*   `/api/article`

**请求方式：**

*   `POST`

**参数：**

| 参数名   | 必选 | 类型   | 说明                                             |
| :------- | :--- | :----- | ------------------------------------------------ |
| title    | 是   | string | 标题                                             |
| content  | 是   | string | 内容                                             |
| cover    | 是   | string | 头图url                                          |
| category | 是   | int    | 分类id                                           |
| source   | 是   | int    | 来源id：原创，转载，翻译                         |
| tags     | 否   |        | \["a","b"]                                       |
| publish  | 是   | int    | 0-对所有人可见（默认），1-登录可见，2-仅自己可见 |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "创建文章成功"
}
```

**返回参数说明：**

*   publish：0-所有人可见，1-登录可见，2-仅自己可见

#### 上传文章头图

**描述：**

*   上传文章头图接口。需要成为撰稿者。

**请求URL：**

*   `/api/article/cover`

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型 | 说明         |
| :----- | :--- | :--- | ------------ |
| cover  | 是   | blob | 文章头图文件 |

**返回：**

```json
{
    "name": "cover",
    "url": "https://xxx.xxx.xx/static/iamge/cover.png"
}

```

**返回参数说明：**

无

**描述：**

*   修改文章接口。文章所有者登录。

**请求URL：**

*   `/api/article/id`

**请求方式：**

*   `PUT`

**参数：**

| 参数名       | 必选 | 类型   | 说明                                             |
| :----------- | :--- | :----- | ------------------------------------------------ |
| title        | 是   | string | 标题                                             |
| content      | 是   | string | 内容                                             |
| cover        | 是   | string | 头图url                                          |
| category\_id | 是   | int    | 分类id                                           |
| source\_id   | 是   | string | 原创，转载，翻译                                 |
| tags         | 否   |        | \["a","b"]                                       |
| publish      | 是   | int    | 0-对所有人可见（默认），1-登录可见，2-仅自己可见 |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "文章修改成功"
}
```

**返回参数说明：**

*   publish：0-所有人可见，1-登录可见，2-仅自己可见

#### 删除文章

**描述：**

*   删除文章接口。文章所有者。

**请求URL：**

*   `/api/article/<int:id>`

**请求方式：**

*   `DELETE`

**参数：**

无

**返回：**

```json
{
    "code": 204,
    "error_code": 0,
    "msg": "删除文章成功"
}
```

**返回参数说明：**

无

#### 获得分类列表

**描述：**

*   获得所有分类接口，分类数据量较少，直接全部返回。

*   前台只允许用户读取分类，后台增删改。

**请求URL：**

*   `/api/article/category`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
 [{
     "id": 1,
     "name": "分类名称"
 }]
```

**返回参数说明：**

无

#### 获得来源列表

**描述：**

*   获得所有来源接口，来源数据量较少，直接全部返回。原创、转载、翻译。是否可以直接写死在前端页面？

*   前台只允许用户读取来源，后台增删改。

**请求URL：**

*   `/api/article/source`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
 [{
     "id": 1,
     "name": "来源名称"
 }]
```

**返回参数说明：**

无

#### 获得标签列表

**描述：**

*   获得所有标签接口，数据量较少，直接全部返回。

*   前台除允许用户读取外，还可以增加，后台删改。

**请求URL：**

*   `/api/article/tag`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
 [{
     "id": 1,
     "name": "标签名称"
 }]
```

**返回参数说明：**

无

#### 新增标签

**描述：**

*   允许撰稿者新增标签。作为新增或修改文章一部分进行添加。不单独暴露接口

**请求URL：**

*   无，编辑文章时添加

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型 | 说明                      |
| :----- | :--- | :--- | ------------------------- |
| tags   | 是   | list | 标签名称\["tag1", "tag2"] |

**返回：**

作为编辑文章结果返回成功提示。

**返回参数说明：**

无

#### 文章点赞

**描述：**

*   点赞或取消点赞文章，**需登录**。

**请求URL：**

*   `/api/article/<int:id>/like`

**请求方式：**

*   `POST`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "点赞/取消点赞成功"
}
```

**返回参数说明：**

无

#### 查询是否点赞

**描述：**

*   判断当前登录用户是否点赞文章。

**请求URL：**

*   `/api/article/<int:id>/like`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "is_like": true
}
```

**返回参数说明：**

无

#### 文章浏览量

**描述：**

*   获得文章浏览量接口，此处主要涉及后端 redis 缓存相关操作。为减少前端请求，合并到获取文章信息。

**请求URL：**

*   `/api/article/<int:id>/view` 不对外暴露

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "view_num": 1
}
```

**返回参数说明：**

作为获取文章信息，一并返回。

### 评论相关

#### 获取文章评论列表

**描述：**

*   获得文章评论列表，分为两级（评论+回复）。评论默认加载最新的10条，回复默认加载最早的3条。

*   TODO 按热度（点赞数、回复数）排序

**请求URL：**

*   `/api/article/<int:id>/comment`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明              |
| :----- | :--- | :--- | ----------------- |
| page   | 否   | int  | 开始页数，默认为1 |
| size   | 否   | int  | 每页条数，默认10  |

**返回：**

```json
{
    "all_count": 100,
    "root_count": 10,
    "item": [{
        "id": 1,
        "sub_id": 1,
        "sub_type": "article",
        "user": {
            "id": 1,
            "username": "xiao",
            "avatar": "https://xx"
        },
        "status": 1,
        "content": "评论内容",
        "ip": "北京市",
        "platform": "Chrome100",
        "device": "Windows 11",
        "is_like": false,
        "replay": {
            "replay_count": 12,
            "item":[{
                "root_id": 1,
                "parent_id": 1,
                "id": 1,
                "sub_id": 1,
                "sub_type": "article",
                "user": {
                    "id": 1,
                    "username": "xiao",
                    "avatar": "https://xx"
                },
                "status": 1,
                "content": "评论内容",
                "ip": "北京市",
                "platform": "Chrome100",
                "device": "Windows 11",
                "is_like": false,
        	}]
		}
    }]
}
```

**返回参数说明：**

*   all\_count 所有评论数

*   root\_count 根评论数

*   sub\_id 对应文章 id

*   sub\_type  文章评论为 article

*   root\_id 所属根评论 id（直接评论文章的），为0表示根评论

*   parent\_id 回复的评论 id，为 0 表示根评论

*   status 状态：1-正常，2-隐藏，3-作者置顶，4-后台置顶

*   is\_like 当前登录用户是否点赞

#### 发表评论

**描述：**

*   登录用户发表评论或回复。

**请求URL：**

*   `/api/article/<int:id>/comment`

**请求方式：**

*   `POST`

**参数：**

| 参数名     | 必选 | 类型   | 说明                        |
| :--------- | :--- | :----- | --------------------------- |
| sub\_id    | 是   | int    | 文章 id                     |
| sub\_type  | 是   | int    | 1-article                   |
| parent\_id | 是   | int    | 0-表示根评论，回复评论id    |
| root\_id   | 是   | int    | 0-表示根评论，所属根评论 id |
| content    | 是   | string | 评论内容                    |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论成功成功"
}
```

**返回参数说明：**

无

#### 删除评论

**描述：**

*   前台删除评论接口，只能管理员和文章作者删除，评论者不可删除。删除成功后会显示`已删除`。

*   后端需判断当前登录用户是否是文章作者或管理员

**请求URL：**

*   `/api/article/<int:id>/comment/<int:cid>`

**请求方式：**

*   `DELETE`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论删除成功"
}
```

**返回参数说明：**

无

#### 点赞评论

**描述：**

*   点赞或取消点赞评论接口，需登录

**请求URL：**

*   `/api/article/<int:id>/comment/<int:cid>/like`

**请求方式：**

*   `POST`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论点赞成功"
}
```

**返回参数说明：**

无

#### 置顶评论

**描述：**

*   置顶或取消置顶评论

*   每个主题（文章）最多可以10个置顶

*   除管理员外，文章作者也可置顶评论。

**请求URL：**

*   `/api/article/<int:id>/comment/<int:cid>/top`

**请求方式：**

*   `POST`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论置顶成功"
}
```

**返回参数说明：**

无

### 说说相关

#### 说说列表

**描述：**

*   获得说说信息流接口，按照时间倒序

**请求URL：**

*   `/api/feed`

**请求方式：**

*   `GET`

**参数：**

**参数：**

| 参数名 | 必选 | 类型 | 说明              |
| :----- | :--- | :--- | ----------------- |
| page   | 否   | int  | 开始页数，默认为1 |
| size   | 否   | int  | 每页条数，默认10  |

**返回：**

```json
{
    "count": 100,
    "item": [{
        id: 1,
        content: "",
        "user": {
            "id": 1,
            "username": "name",
            "avatar": "https://xx"
        },
        "publish": 1,
        "status": 1,
        "order": 0,
        "like_num": 0,
        "comment_status": 2,
        "create_time": "2022-01-01 12:12:12"
    }]
}
```

**返回参数说明：**

*   publish 1- 公开 2- 登录可见 3-仅自己可见

*   status 1-正常 2-隐藏 3-置顶

*   order 置顶时排序依据

*   like\_num 点赞人数

*   comment\_status 是否可评论，1-可以2-不可

#### 新增说说

**描述：**

*   发表说说信息流接口，**撰稿者**

**请求URL：**

*   `/api/feed`

**请求方式：**

*   `POST`

**参数：**

| 参数名  | 必选 | 类型   | 说明     |
| :------ | :--- | :----- | -------- |
| content | 是   | string | 说说内容 |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "发表说说成功"
}
```

**返回参数说明：**

无

#### 删除说说

**描述：**

*   删除说说接口

**请求URL：**

*   `/api/feed/<int:id>`

**请求方式：**

*   `DELETE`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "删除说说成功"
}
```

**返回参数说明：**

无

### 消息相关

消息目前只有收到评论或点赞以及系统会发送消息。

#### 获得所有消息

**描述：**

*   登录后获取自己的消息

**请求URL：**

*   `/api/message`

**请求方式：**

*   `GET`

**参数：**

| 参数名 | 必选 | 类型 | 说明       |
| :----- | :--- | :--- | ---------- |
| page   | 否   | int  | 页码默认1  |
| size   | 否   | int  | 个数默认10 |

**返回：**

```json
{
    "count": 100,
    "item": [{
        "id": 1,
        "content": "消息内容(html?)",
        "from_user": {
            "id": 1,
            "username": "",
            "avatar": ""
        },
        "is_read": false
    }]
}
```

**返回参数说明：**

无

#### 获得未读消息

同上， is\_read 为false 过滤。

#### 标记消息已读

**描述：**

*   登录后标记自己的消息已读

**请求URL：**

*   `/api/message/<int:id>`

**请求方式：**

*   `PUT`

**参数：**

无

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "已读成功"
}
```

**返回参数说明：**

无

#### 标记所有消息已读

**描述：**

*   登录后标记自己的所有未读消息为已读

**请求URL：**

*   `/api/message`

**请求方式：**

*   `PUT`

**参数：**

无

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "所有已读成功"
}
```

**返回参数说明：**

无

#### 获得未读消息数量

获取未读消息时得到，不单独作为接口暴露。

#### 在线消息提醒

使用 websoket 技术。用户在线时，实时提醒。

## 第七章 后台 API

### 用户管理

#### 查看所有用户

**描述：**

*   后台查看所有用户，包括正常、拉黑、测试等类型。

**请求URL：**

*   `/api/admin/user`

**请求方式：**

*   `GET`

**参数：**

| 参数名           | 必选 | 类型   | 说明                     |
| :--------------- | :--- | :----- | ------------------------ |
| group            | 否   | int    | 所属分组，默认0-所有分组 |
| register\_source | 否   | int    | 注册来源，默认0-所有来源 |
| start            | 否   | int    | 开始页数，默认为1        |
| count            | 否   | int    | 每页条数，默认20         |
| status           | 否   | int    | 账户状态，正常、拉黑     |
| start\_time      | 否   | string | 注册时间起始             |

**返回：**

```json
{
    "count": 10,
    "item": [
        {
            "username": "xiao",
            "mobile": "1234567",
            "mobile_bind_time": '2021-01-01 12:12:12',
            "email": "example@xiao.com",
            "email_bind_time": '2021-01-01 12:12:12',
            "avatar": "https://xxx.xxx.xx/static/image/avatar.png",
            "origin_avatar": "https://xxx.xxx.xx/static/image/avatar.png",
            "gender": "1",
            "birthday": "2020-01-01",
            "address": "Hello World",
            "signature": "坚定",
            "group": 1,
            "is_delete": 0,
            "create_time": '2021',
            "register_source": 1
        }
    ]
}
```

**返回参数说明：**

无

#### 设置用户状态

**描述：**

*   后台设置用户状态，拉黑。

**请求URL：**

*   `/api/admin/user/status`

**请求方式：**

*   `PUT`

**参数：**

| 参数名 | 必选 | 类型 | 说明   |
| :----- | :--- | :--- | ------ |
| id     | 否   | int  | 用户id |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "拉黑或恢复成功"
}
```

**返回参数说明：**

无

#### 分配用户角色

**描述：**

*   后台设置用户分组，目前所在组必须唯一。

**请求URL：**

*   `/api/admin/user/dispatch`

**请求方式：**

*   `PUT`

**参数：**

| 参数名    | 必选 | 类型 | 说明   |
| :-------- | :--- | :--- | ------ |
| id        | 是   | int  | 用户id |
| group\_id | 是   | int  | 分组id |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "设置成功"
}
```

**返回参数说明：**

无

### 分组（角色）管理

#### 查看所有权限

**描述：**

*   后台查询所有权限，在初始化程序时自动添加到数据库，不支持人工增删改只能查看。

**请求URL：**

*   `/api/admin/permission`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "count": 3,
    "item": {
        "module_name": [{
            "id": 1,
            "name": "权限名称"
        }]
    }
}
```

**返回参数说明：**

无

#### 查看所有分组

**描述：**

*   后台查询所有分组，分组较少直接全部返还。

**请求URL：**

*   `/api/admin/group`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "count": 3,
    "item": [{
        "id": 1,
        "name": "普通用户",
        "info": "注册后默认分组",
        "create_time": "2021-",
        "permissions": []
    }]
}
```

**返回参数说明：**

无

#### 新增分组

**描述：**

*   后台新增分组。

**请求URL：**

*   `/api/admin/group`

**请求方式：**

*   `POST`

**参数：**

| 参数名      | 必选 | 类型       | 说明        |
| :---------- | :--- | :--------- | ----------- |
| name        | 是   | string     | 分类名称    |
| info        | 否   | string     | 简介        |
| permissions | 是   | list\[int] | 拥有权限ids |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增分组成功"
}
```

**返回参数说明：**

无

#### 修改分组

**描述：**

*   后台新增分组。

**请求URL：**

*   `/api/admin/group`

**请求方式：**

*   `POST`

**参数：**

| 参数名      | 必选 | 类型       | 说明        |
| :---------- | :--- | :--------- | ----------- |
| name        | 是   | string     | 分类名称    |
| info        | 否   | string     | 简介        |
| permissions | 是   | list\[int] | 拥有权限ids |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增分组成功"
}
```

**返回参数说明：**

无

### 分类管理

#### 查看所有分类

**描述：**

*   后台获得所有分类接口。

**请求URL：**

*   `/api/admin/article/category`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "count": 10,
    "item": [{
        "id": 1,
        "name": "分类名称",
        "info": "介绍"
    }]
}
```

**返回参数说明：**

无

#### 新增分类

**描述：**

*   后台新增分类。

**请求URL：**

*   `/api/admin/category`

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 分类名称 |
| info   | 否   | string | 简介     |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增分类成功"
}
```

**返回参数说明：**

无

#### 修改分类

**描述：**

*   后台修改分组。

**请求URL：**

*   `/api/admin/category`

**请求方式：**

*   `PUT`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 分类名称 |
| info   | 否   | string | 简介     |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "修改分类成功"
}
```

**返回参数说明：**

无

#### 删除分类

**描述：**

*   后台删除分组。

**请求URL：**

*   `/api/admin/category/<int:id>`

**请求方式：**

*   `PUT`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "删除分类成功"
}
```

**返回参数说明：**

无

### 标签管理

#### 查看所有标签

**描述：**

*   后台获得所有标签接口。

**请求URL：**

*   `/api/admin/tag`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "count": 10,
    "item": [{
        "id": 1,
        "name": "标签名称",
        "info": "介绍"
    }]
}
```

**返回参数说明：**

无

#### 新增标签

**描述：**

*   后台新增标签。

**请求URL：**

*   `/api/admin/tag`

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 标签名称 |
| info   | 否   | string | 简介     |
| color  | 否   | string | 字体颜色 |
| bg     | 否   | string | 背景颜色 |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增标签成功"
}
```

**返回参数说明：**

无

#### 修改标签

**描述：**

*   后台修改标签。

**请求URL：**

*   `/api/admin/tag`

**请求方式：**

*   `PUT`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 标签名称 |
| info   | 否   | string | 简介     |
| color  | 否   | string | 字体颜色 |
| bg     | 否   | string | 背景色   |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "修改标签成功"
}
```

**返回参数说明：**

无

#### 删除标签

**描述：**

*   后台删除标签。

*   还需要删除文章中的标签，如何删除？惰性删除：在获取文章信息时，判断标签是否存在？不存在则从列表中删除。

**请求URL：**

*   `/api/admin/tag/<int:id>`

**请求方式：**

*   `PUT`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "删除标签成功"
}
```

**返回参数说明：**

无

### 来源管理

#### 查看所有来源

**描述：**

*   后台获得所有来源接口。

*   默认只有 原创、转载、翻译三种。

**请求URL：**

*   `/api/admin/source`

**请求方式：**

*   `GET`

**参数：**

无

**返回：**

```json
{
    "count": 10,
    "item": [{
        "id": 1,
        "name": "来源名称"
    }]
}
```

**返回参数说明：**

无

#### 新增来源

**描述：**

*   后台新增来源。

**请求URL：**

*   `/api/admin/source`

**请求方式：**

*   `POST`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 来源名称 |
| info   | 否   | string | 简介     |
| color  | 否   | string | 字体颜色 |
| bg     | 否   | string | 背景颜色 |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增来源成功"
}
```

**返回参数说明：**

无

#### 修改标签

**描述：**

*   后台修改来源。

**请求URL：**

*   `/api/admin/source`

**请求方式：**

*   `PUT`

**参数：**

| 参数名 | 必选 | 类型   | 说明     |
| :----- | :--- | :----- | -------- |
| name   | 是   | string | 来源名称 |
| info   | 否   | string | 简介     |
| color  | 否   | string | 字体颜色 |
| bg     | 否   | string | 背景色   |

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "修改来源成功"
}
```

**返回参数说明：**

无

#### 删除标签

**描述：**

*   后台删除来源。

*   已有文章放入 defualt ？

**请求URL：**

*   `/api/admin/source/<int:id>`

**请求方式：**

*   `PUT`

**参数：**

无

**返回：**

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "删除来源成功"
}
```

**返回参数说明：**

无

### 文章管理

#### 获取文章列表

#### 封禁文章

#### 删除文章

#### 置顶文章

### 评论管理

#### 查询评论列表

#### 删除评论

#### 置顶评论

#### 审核评论

## 第八章 附录

### 8.1 参考

*   黑马人工智能6.0-黑马头条项目。
