---
title: 数据模型
---
## 数据库设计

- 使用 Mysql8.0 varchar(32)表示32个字符，汉字也是32个。对应的sqlalchemy 也是 String(32) 表示字符。

### 用户表（users）

| 字段名      | 类型         | 可空 | 唯一 | 默认值 | 备注                                               |
| ----------- | ------------ | ---- | ---- | ------ | -------------------------------------------------- |
| id          | bigint       |      | 是   |        | 自增主键                                           |
| username    | varchar(32)  |      | 是   |        | 昵称                                               |
| mobile      | char(16)     |      | 是   |        | 手机号                                             |
| password    | varchar(255) |      |      |        | 密码                                               |
| role_id     | bigint       |      |      | 1      | 所属角色：1-普通用户，2-撰稿者，3-虚拟用户         |
| signature   | varchar(200) | 是   |      |        | 个性签名                                           |
| avatar      | varchar(255) | 是   |      |        | 头像                                               |
| email       | varchar(255) | 是   | 是   | ''     | 邮箱，保留字段                                     |
| last_login  | datetime     | 是   |      |        | 最后登录时间                                       |
| status      | tinyint      |      |      | 1      | 状态：0-未激活，1-正常，2-禁言，3-拉黑，管理员操作 |
| is_deleted  | tinyint      |      |      | 0      | 是否删除：0-没有，1-已删除                         |
| gender      | tinyint      |      |      | 0      | 性别：0-未设置，1-女，2-男                         |
| birthday    | date         | 是   |      |        | 生日                                               |
| address     | varchar(100) |      |      | ''     | 所在地                                             |
| company     | varchar(50)  | 是   |      |        | 公司                                               |
| career      | varchar(50)  | 是   |      |        | 职业                                               |
| create_time | datetime     |      |      | now    | 创建时间                                           |
| update_time | datetime     |      |      | now    | 修改时间                                           |

### 角色表（role）

| 字段名      | 类型         | 可空 | 唯一 | 默认值 | 备注     |
| ----------- | ------------ | ---- | ---- | ------ | -------- |
| id          | bigint       |      | 是   |        | 自增主键 |
| name        | varchar(32)  |      | 是   |        | 角色名称 |
| info        | varchar(255) | 是   |      | ''     | 角色说明 |
| create_time | datetime     |      |      | now    | 创建时间 |
| update_time | datetime     |      |      | now    | 修改时间 |

### 角色权限关联表（role_permissions）

| 字段名        | 类型     | 可空 | 唯一 | 默认值 | 备注     |
| ------------- | -------- | ---- | ---- | ------ | -------- |
| id            | bigint   |      | 是   |        | 自增主键 |
| role_id       | bigint   |      |      |        | 角色 ID  |
| permission_id | bigint   |      |      |        | 权限 ID  |
| create_time   | datetime |      |      | now    | 创建时间 |

### 权限表（permissions）

| 字段名      | 类型         | 可空 | 唯一 | 默认值    | 备注                           |
| ----------- | ------------ | ---- | ---- | --------- | ------------------------------ |
| id          | int          |      | 是   |           | 主键                           |
| name        | varchar(32)  |      | 是   |           | 权限名称                       |
| module      | varchar(32)  |      |      | 'default' | 权限所属模块，用于分组查看权限 |
| info        | varchar(255) | 是   |      |           | 权限说明                       |
| create_time | datetime     |      |      | now       | 创建时间                       |
| update_time | datetime     |      |      | now       | 修改时间                       |

### 文章表（article）

| 字段名        | 类型         | 可空 | 唯一 | 默认值            | 备注                                     |
| ------------- | ------------ | ---- | ---- | ----------------- | ---------------------------------------- |
| id            | bigint       |      | 是   |                   | 文章ID                                   |
| title         | varchar(128) |      | 是   |                   | 标题                                     |
| summary       | varchar(255) | 是   |      |                   | 摘要                                     |
| content       | longtext     |      |      |                   | 内容                                     |
| cover         | varchar(255) |      |      | article/cover.png | 封面                                     |
| category_id   | int          | 是   |      | null              | 分类 ID，null 表示默认分类               |
| source        | int          |      |      |                   | 来源 ID：1-原创，2-转载，3-翻译          |
| publish       | tinyint      |      |      | 1                 | 1-公开，2-登录可见，3-仅自己可见         |
| status        | int          |      |      |                   | 1可见, 0-不可见,2-作者置顶, 3-管理员置顶 |
| sort          | tinyint      |      |      | 1                 | 排序 ，管理员操作                        |
| allow_comment | tinyint      |      |      | 1                 | 是否开启评论：1-开启，0-关闭             |
| user_id       | bigint       |      |      |                   | 作者 id                                  |
| create_time   | datetime     |      |      | now               | 创建时间                                 |
| update_time   | datetime     |      |      | now               | 修改时间                                 |
| delete_time   | datetime     | 是   |      | null              | 删除时间                                 |

### 文章点赞表（article_like）

| 字段名      | 类型     | 可空 | 唯一 | 默认值 | 备注     |
| ----------- | -------- | ---- | ---- | ------ | -------- |
| id          | bigint   | 否   | 是   |        | 主键     |
| user_id     | bigint   | 否   | 否   |        | 用户 ID  |
| article_id  | bigint   | 否   | 否   |        | 文章 ID  |
| create_time | datetime | 否   | 否   | now    | 创建时间 |

### 标签表（tag）

| 字段名      | 类型        | 可空 | 唯一 | 默认值 | 备注     |
| ----------- | ----------- | ---- | ---- | ------ | -------- |
| id          | bigint      |      | 是   |        | 主键     |
| name        | varchar(32) |      | 是   |        | 标签名称 |
| create_time | datetime    |      |      | now    | 创建时间 |

### 文章-标签关联表（article_tag）

| 字段名      | 类型     | 可空 | 唯一 | 默认值 | 备注     |
| ----------- | -------- | ---- | ---- | ------ | -------- |
| id          | bigint   |      | 是   |        | 主键     |
| article_id  | bigint   |      |      |        | 文章 ID  |
| tag_id      | bigint   |      |      |        | 标签 ID  |
| create_time | datetime |      |      | now    | 创建时间 |

article_id 和 tag_id 联合唯一。

### 分类表（category）

| 字段名      | 类型         | 可空 | 唯一 | 默认值  | 备注                       |
| ----------- | ------------ | ---- | ---- | ------- | -------------------------- |
| id          | bigint       | 否   | 是   |         | 主键                       |
| name        | varchar(32)  | 否   | 否   |         | 文章分类名称               |
| info        | varchar(200) | 是   | 否   |         | 分类说明                   |
| banner      | varchar(255) | 是   | 否   | default | 分类背景图                 |
| sort        | int          | 否   | 否   | 1       | 序号                       |
| status      | tinyint      | 否   | 否   | 1       | 是否可见：1-可见，0-不可见 |
| create_time | datetime     | 否   | 否   | now     | 创建时间                   |
| update_time | datetime     | 否   | 否   | now     | 修改时间                   |
| is_deleted  | tinyint      | 否   | 否   | 0       | 是否删除：0-没有，1-已删除 |

### 评论表（comment）

| 字段名       | 类型         | 可空 | 唯一 | 默认值 | 备注                                                     |
| ------------ | ------------ | ---- | ---- | ------ | -------------------------------------------------------- |
| id           | bigint       |      | 是   |        | 主键                                                     |
| article_id   | bigint       |      |      |        | 文章 ID                                                  |
| user_id      | bigint       | 是   |      |        | 用户 ID                                                  |
| content      | varchar(400) |      |      |        | 内容                                                     |
| root_id      | int          |      |      | 0      | 0表示根评论，不为0表示回复所对应的最顶层的评论（根评论） |
| parent_id    | int          |      |      | 0      | 0也表示这是根评论，不为0表示回复的对象                   |
| replay_count | int          |      |      | 0      | 如果是 root, 需要统计它的回复数量                        |
| like_count   | int          |      |      | 0      | 点赞数                                                   |
| ip           | varchar(16)  |      |      |        | 评论者 IP                                                |
| status       | tinyint      |      |      | 1      | 状态：1-正常，0-隐藏，2-置顶，管理员操作                 |
| create_time  | datetime     |      |      | now    | 创建时间                                                 |
| is_deleted   | tinyint      |      |      | 1      | 是否删除：1-没有，0-已删除                               |

### 评论点赞表（comment_like）

| 字段名      | 类型     | 为空 | 唯一 | 默认值 | 备注     |
| ----------- | -------- | ---- | ---- | ------ | -------- |
| id          | bigint   |      | 是   |        | 主键     |
| user_id     | bigint   |      |      |        | 用户 ID  |
| comment_id  | bigint   |      |      |        | 评论 ID  |
| create_time | datetime |      |      | now    | 创建时间 |

### 通知表 (notice)

| 字段名       | 类型         | 可空 | 唯一 | 默认值 | 备注                |
| ------------ | ------------ | ---- | ---- | ------ | ------------------- |
| id           | bigint       |      | 是   |        | 主键                |
| to_user_id   | bigint       |      |      |        | 用户 ID             |
| from_user_id | bigint       |      |      |        | 通知来源用户 ID     |
| content      | varchar(255) |      |      |        | 通知内容            |
| status       | tinyint      |      |      |        | 状态, 0-未读 1-已读 |
| create_time  | datetime     |      |      | now    | 创建时间            |
