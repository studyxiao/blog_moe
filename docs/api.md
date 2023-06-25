## 5. API 设计

- 前缀 `/api/v1/`

### 5.1 用户模块

#### 5.1.1 获取验证码

**描述：**

- 通过手机号获取验证码，可用于注册、登录、找回密码、重置密码等。

**请求url：**

- `/user/code`

**请求方式:**

- `GET`

**参数：**

| 参数名 | 必选 | 类型   | 描述                                       |
| ------ | ---- | ------ | ------------------------------------------ |
| mobile | 是   | string | 手机号                                     |
| cate   | 是   | string | 验证码类型，register, login, forget, reset |

**返回：**

```json
{
    "code": 200,
    "error_code": 0,
    "msg": "请填写接收到的验证码"
}
```

**返回参数说明：**

无

#### 5.1.2 检测昵称

- 描述：注册时填写昵称自动查验是否合规以及是否存在。

- 请求URL：`/user/name`

- 请求方式：`GET`

- 请求参数：

| 参数名   | 必选 | 类型   | 描述 |
| -------- | ---- | ------ | ---- |
| username | 是   | string | 昵称 |

- 响应参数：

```json
{
    "is_valid": true
}
```

> is_valid: 昵称是否符合规范：字数4-20之间，只能是字母数字和汉字，数据库是否已经存在等。

#### 5.1.3 注册

- 请求URL：/user/register
- 请求方法：POST
- 请求参数：

| 参数名    | 类型   | 必选 | 说明     |
| --------- | ------ | ---- | -------- |
| mobile    | string | 是   | 手机号   |
| password  | string | 是   | 密码     |
| password2 | string | 是   | 验证密码 |
| code      | stirng | 是   | 验证码   |
| username  | string | 是   | 用户昵称 |

> password: 大小写字母和数字以及特殊符号_*&^%$#@!.,? 等且至少单三种，位数在6-18之间

- 响应参数：

```json
{
    "code": 200,
    "error_code": 0,
    "msg": "注册成功"
}
```

#### 5.1.4 登录

- 描述：通过手机号登录。

- 请求url：`/user/login`

- 请求方式：`POST`

- 请求参数：

| 参数名   | 类型   | 必选 | 说明                                   |
| -------- | ------ | ---- | -------------------------------------- |
| mobile   | string | 是   | 手机号                                 |
| cate     | int    | 是   | 验证类型：1-手机号密码，2-手机号验证码 |
| password | string | 是   | 凭证：密码或验证码                     |

**返回：**

错误

```json
{
    "code": 400,
    "error_code": 10010,
    "msg": "信息有误"
}
```

成功

```json
{
    "access_token": "XXX",
    "refresh_token": "XXX"
}
```

#### 5.1.5 找回密码

- 请求URL：`/user/forget`

- 请求方式：`POST`

- 请求参数：

| 参数名    | 类型   | 必选 | 说明       |
| --------- | ------ | ---- | ---------- |
| mobile    | string | 是   | 手机号     |
| code      | string | 是   | 验证码     |
| password  | string | 是   | 新密码     |
| password2 | string | 是   | 确认新密码 |

**返回：**

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "密码修改成功"
}
```

#### 5.1.6 修改密码

- 请求URL：`/user/reset`

- 请求方式：`POST`

- 请求参数：

| 参数名       | 类型   | 必选 | 说明       |
| ------------ | ------ | ---- | ---------- |
| old_password | string | 是   | 原密码     |
| password     | string | 是   | 新密码     |
| password2    | string | 是   | 确认新密码 |

- 响应参数：

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "密码修改成功"
}
```





- 用户信息查询接口：GET /v1/users/:user_id
- 用户信息修改接口：PUT /v1/users/:user_id
- 用户密码修改接口：PUT /v1/users/:user_id/password

#### 5.1.7 用户信息

- 请求URL：`/v1/user/<int:id>/info`
- 请求方法：`GET`
- 请求参数：

| 参数    | 类型 | 必选 | 描述    |
| ------- | ---- | ---- | ------- |
| user_id | int  | 是   | 用户 ID |

- 响应参数：

```json
{
    "username": "xiao",
    "mobile": "1234567",
    "mobile_bind_time": "2021-01-01 12:12:12",
    "email": "example@xiao.com",
    "email_bind_time": "2021-01-01 12:12:12",
    "avatar": "https://xxx.xxx.xx/static/image/avatar.png",
    "gender": "1",
    "birthday": "2020-01-01",
    "address": "Hello World",
    "signature": "坚定",
    "role": 1,
}
```

#### 5.1.8 修改个人信息

- 请求URL：`/user/info`
- 请求方法：`PUT`
- 请求参数：

| 参数名    | 类型   | 必选 | 描述                        |
| --------- | ------ | ---- | --------------------------- |
| username  | string | 是   | 昵称                        |
| gender    | int    | 是   | 性别，1-女，2-男            |
| birthday  | string | 是   | 生日，'2021-01-01 12:12:12' |
| email     | string | 否   |                             |
| address   | string | 是   | 地址                        |
| signature | string | 否   | 个人简介                    |

- 返回参数：

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "个人信息修改成功"
}
```

### 5.2 文章模块

#### 5.2.1 文章列表

- 请求URL：`/article`
- 请求方法：`GET`
- 请求参数：

| 参数名     | 类型   | 必选 | 描述                                     |
| ---------- | ------ | ---- | ---------------------------------------- |
| page       | int    | 否   | 页码，默认为1                            |
| count      | int    | 否   | 每页条数，默认为10                       |
| query      | string | 否   | 关键字，用于搜索文章标题和内容           |
| tag_id     | int    | 否   | 标签 ID，用于筛选文章                    |
| cate_id    | int    | 否   | 分类 ID，用于筛选文章                    |
| author_id  | int    | 否   | 作者 ID，用于筛选文章                    |
| start_date | string | 否   | 开始日期，用于筛选文章，格式为YYYY-MM-DD |
| end_date   | string | 否   | 结束日期，用于筛选文章，格式为YYYY-MM-DD |

- 响应参数：

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

#### 5.2.2 文章详情

- 请求URL：`/article/<int:id>`
- 请求方法：`GET`
- 请求参数：

| 参数名     | 类型 | 是否必选 | 描述   |
| ---------- | ---- | -------- | ------ |
| article_id | int  | 是       | 文章ID |

- 响应参数：

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

#### 5.2.3 文章创建

- 请求URL：`/article`
- 请求方法：`POST`
- 请求参数：

| 参数名    | 类型   | 必选 | 说明                                             |
| --------- | ------ | ---- | ------------------------------------------------ |
| title     | string | 是   | 标题                                             |
| content   | string | 是   | 内容                                             |
| cover     | string | 是   | 头图url                                          |
| category  | int    | 是   | 分类id                                           |
| source    | int    | 是   | 来源id：原创，转载，翻译                         |
| tags      |        | 否   | ["a","b"]                                        |
| author_id | int    | 是   | 作者 ID                                          |
| publish   | int    | 是   | 0-对所有人可见（默认），1-登录可见，2-仅自己可见 |

- 响应参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "创建文章成功"
}
```

#### 5.2.4 文章修改

- 请求URL：`/article/<int:id>`
- 请求方法：`PUT`
- 请求参数：

| 参数名    | 类型   | 必选 | 说明                                             |
| --------- | ------ | ---- | ------------------------------------------------ |
| title     | string | 是   | 标题                                             |
| content   | string | 是   | 内容                                             |
| cover     | string | 是   | 头图url                                          |
| category  | int    | 是   | 分类id                                           |
| source    | int    | 是   | 来源id：原创，转载，翻译                         |
| tags      |        | 否   | ["a","b"]                                        |
| author_id | int    | 是   | 作者 ID                                          |
| publish   | int    | 是   | 0-对所有人可见（默认），1-登录可见，2-仅自己可见 |

- 响应参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "修改文章成功"
}
```

#### 5.2.5 文章删除

- 请求URL：`/article/<int:id>`
- 请求方法：DELETE
- 请求参数：无

- 响应参数：

```json
{
    "code": 204,
    "error_code": 0,
    "msg": "删除文章成功"
}
```

#### 5.2.6 分类列表

- 请求URL：`/article/category`
- 请求方法：`GET`
- 请求参数：无

- 响应参数：

```json
 [{
     "id": 1,
     "name": "分类名称"
 }]
```

#### 5.2.7 标签列表

- 请求URL：`/article/tag`

- 请求方式：`GET`

- 请求参数：

| 参数名 | 类型   | 必选 | 说明                           |
| ------ | ------ | ---- | ------------------------------ |
| tag    | string | 是   | 选择标签时根据输入实时查询标签 |

- 返回参数：

```json
 [{
     "id": 1,
     "name": "标签名称"
 }]
```

#### 5.2.8 标签创建

- 请求URL：`/article/tag`

- 请求方式：`POST`

- 请求参数：

| 参数名 | 类型   | 必选 | 说明     |
| ------ | ------ | ---- | -------- |
| tag    | string | 是   | 标签名称 |

- 返回参数：

```json
 {
     "id": 1,
     "name": "标签名称"
 }
```

#### 5.2.9 来源列表

前端直接使用：1-原创，2-转载，3-翻译。

#### 5.2.10 点赞文章

- 请求URL：`/article/<int:id>/like`

- 请求方式：`POST`

- 请求参数：无

- 返回参数：

```json
 {
    "code": 204,
    "error_code": 0,
    "msg": "点赞文章成功"
}
```

#### 5.2.11 取消点赞

- 请求URL：`/article/<int:id>/like`

- 请求方式：`DELETE`

- 请求参数：无

- 返回参数：

```json
 {
    "code": 204,
    "error_code": 0,
    "msg": "取消点赞文章成功"
}
```

### 5.3 静态资源

#### 5.3.1 上传图片

- 请求URL：`/image`

- 请求方式：`POST`

- 请求参数：

| 参数名 | 类型      | 必选 | 说明         |
| ------ | --------- | ---- | ------------ |
| cover  | blob/file | 是   | 文章头图文件 |

```js
const form = new FormData()
form.append('file', File)
/* File 格式 */
```

- 返回参数：

```json
 {
    "name": "cover",
    "url": "https://xxx.xxx.xx/static/iamge/cover.png"
}
```

### 5.4 评论模块

#### 5.4.1 评论列表

- 请求URL：`/article/<int:id>/comment`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型 | 必选 | 说明              |
| ------ | ---- | ---- | ----------------- |
| page   | int  | 否   | 开始页数，默认为1 |
| size   | int  | 否   | 每页条数，默认10  |

- 返回参数：

```json
{
    "all_count": 100,
    "root_count": 10,
    "item": [{
        "id": 1,
        "article_id": 1,
        "user": {
            "id": 1,
            "username": "xiao",
            "avatar": "https://xx"
        },
        "status": 1,
        "content": "评论内容",
        "ip": "北京市",
        "is_like": false,
        "replay": {
            "replay_count": 12,
            "item":[{
                "root_id": 1,
                "parent_id": 1,
                "id": 1,
                "article_id": 1,
                "user": {
                    "id": 1,
                    "username": "xiao",
                    "avatar": "https://xx"
                },
                "status": 1,
                "content": "评论内容",
                "ip": "北京市",
                "is_like": false
        	}]
		}
    }]
}
```

#### 5.4.2 发表评论

- 请求URL：`/article/<int:id>/comment`
- 请求方法：`POST`
- 请求参数：

| 参数名     | 必选 | 类型   | 说明                          |
| ---------- | ---- | ------ | ----------------------------- |
| article_id | 是   | int    | 文章 ID                       |
| parent_id  | 是   | int    | 0-表示根评论，要回复的评论 ID |
| root_id    | 是   | int    | 0-表示根评论，所属根评论 ID   |
| content    | 是   | string | 评论内容                      |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论成功成功"
}
```

#### 5.4.3 点赞评论

- 请求URL：`/article/<int:id>/comment/<int:id>/like`
- 请求方法：`POST`
- 请求参数：无
- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "评论点赞成功"
}
```

#### 5.4.3 取消点赞评论

- 请求URL：`/article/<int:id>/comment/<int:id>/like`
- 请求方法：`DELETE`
- 请求参数：无
- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "取消评论点赞成功"
}
```

### 5.5 消息模块

#### 5.5.1 消息列表

- 请求URL：`/message`
- 请求方式：`GET`
- 请求参数：

| 参数名  | 类型 | 必选 | 说明                   |
| ------- | ---- | ---- | ---------------------- |
| page    | int  | 否   | 页码默认1              |
| count   | int  | 否   | 个数默认10             |
| is_read | bool | 否   | 是否已读 0-全部 1-未读 |

- 返回参数：

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

#### 5.5.2 标记已读

- 请求URL：`/message/<int:id>`
- 请求方法：`PUT`
- 请求参数：无
- 返回参数：

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "消息已读"
}
```

#### 5.5.3 标记所有已读

- 请求URL：`/message`
- 请求方法：`PUT`
- 请求参数：无
- 返回参数：

```json
{
    "code": 202,
    "error_code": 0,
    "msg": "所有消息已读"
}
```

#### 5.5.4 实时通知

- 请求URL：`ws://url/message/`
- 请求方式`GET`
- 请求参数：无
- 返回参数：

```json
{
    "unread_num": 1,
    "new_article": 3,
}
```

### 5.6 搜索模块

#### 5.6.1 文章搜索

- 请求URL：`/search`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明       |
| ------ | ------ | ---- | ---------- |
| query  | string | 是   | 查询字段   |
| page   | int    | 否   | 页码默认1  |
| count  | int    | 否   | 个数默认10 |

- 返回参数：

```json
[{}]
```

#### 5.6.2 标签/分类文章列表

不单独实现，由文章列表接口实现，通过传入不同参数获得数据。

### 5.7 统计模块

#### 5.7.1 用户点赞、评论、文章

- 请求URL：`/user/<int:id>/stastic`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型 | 必选 | 说明                                |
| ------ | ---- | ---- | ----------------------------------- |
| page   | int  | 否   | 页码默认1                           |
| count  | int  | 否   | 个数默认10                          |
| cate   | int  | 否   | 默认1，1-like，2-comment，3-article |

- 返回参数：

```json
{
    "count": 10,
    data:[{
        "date": "2020",
        "message": "点赞/评论了文章<xxx>"
	}]
}
```

#### 5.7.2 文章精选（点赞、查看、评论）

- 请求URL：`/article/hot`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型 | 必选 | 说明                                        |
| ------ | ---- | ---- | ------------------------------------------- |
| cate   | int  | 否   | 默认0，0-所有，1-like，2-comment，3-article |

- 返回参数

```json
{
    "like": [],
    "comment": [],
    "article": []
}
```

返回前10。

## 6 后台API

### 6.1 管理员登录

- 请求URL：`/admin/login`
- 请求方法：`GET`
- 请求参数：

| 参数名   | 类型   | 必选 | 说明   |
| -------- | ------ | ---- | ------ |
| mobile   | string | 是   | 手机号 |
| password | string | 是   | 密码   |

- 返回参数：

```json
{
    "code": 200,
    "error_code": 11001,
    "msg": "登录成功"
}
```

### 6.2 用户管理

#### 6.2.1 用户列表

- 请求URL：`/admin/user`
- 请求方法：`GET`
- 请求参数：

| 参数名        | 类型   | 必选 | 说明                     |
| ------------- | ------ | ---- | ------------------------ |
| username      | string | 否   | 要搜索的用户名           |
| role_id       | int    | 否   | 所属角色，默认0-所有角色 |
| mobile        | string | 否   | 根据手机号搜索           |
| status        | int    | 否   | 账户状态，1-正常、0-拉黑 |
| register_time | string | 否   | 某日注册搜索             |
| page          | int    | 否   | 开始页数，默认为1        |
| count         | int    | 否   | 每页条数，默认20         |

- 返回参数：

```json
{
    "count": 10,
    "item": [
        {
            "username": "xiao",
            "mobile": "1234567",
            "email": "example@xiao.com",
            "avatar": "https://xxx.xxx.xx/static/image/avatar.png",
            "gender": "1",
            "birthday": "2020-01-01",
            "address": "Hello World",
            "signature": "坚定",
            "group": 1,
            "is_delete": 0,
            "create_time": "2021",
            "register_source": 1
        }
    ]
}
```

#### 6.2.2 设置用户状态

- 请求URL：`/admin/user/status`
- 请求方法：`PUT`
- 请求参数：

| 参数名   | 类型      | 必选 | 说明     |
| -------- | --------- | ---- | -------- |
| user_ids | list[int] | 是   | 用户 IDs |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "拉黑或恢复成功"
}
```

#### 6.2.3 分配用户角色

- 请求URL：`/admin/user/dispatch`
- 请求方法：`PUT`
- 请求参数：

| 参数名  | 类型 | 必选 | 说明    |
| ------- | ---- | ---- | ------- |
| user_id | int  | 是   | 用户 ID |
| role_id | int  | 是   | 角色 ID |

### 6.3 角色管理

#### 6.3.1 权限列表

- 请求URL：`/admin/permission`
- 请求方法：`GET`
- 请求参数：无
- 返回参数：

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

#### 6.3.2 角色列表

- 请求URL：`/admin/role`
- 请求方法：`GET`
- 请求参数：无
- 返回参数：

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

角色较少，所以不再分页，一次获取。

#### 6.3.3 角色详情

- 请求URL：`/admin/role/<int:id>`
- 请求方法：`GET`
- 请求参数：无
- 返回参数：

```json
{
    "id": 1,
    "name": "普通用户",
    "info": "注册后默认分组",
    "create_time": "2021-",
    "permissions": []
}
```

#### 6.3.4 角色创建

- 请求URL：`/admin/role`
- 请求方法：`POST`
- 请求参数：

| 参数名         | 类型      | 必选 | 说明     |
| -------------- | --------- | ---- | -------- |
| name           | string    | 是   | 角色名称 |
| info           | string    | 否   | 角色说明 |
| permission_ids | list[int] | 是   | 权限 IDs |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "新增分组成功"
}
```

#### 6.3.5 角色修改

- 请求URL：`/admin/role`
- 请求方法：`PUT`
- 请求参数：

| 参数名         | 类型      | 必选 | 说明     |
| -------------- | --------- | ---- | -------- |
| name           | string    | 是   | 角色名称 |
| info           | string    | 否   | 角色说明 |
| permission_ids | list[int] | 是   | 权限 IDs |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "修改分组成功"
}
```

#### 6.3.6 角色删除

- 请求URL：`/admin/role/`
- 请求方法：`DELETE`
- 请求参数：

| 参数名   | 类型      | 必选 | 说明             |
| -------- | --------- | ---- | ---------------- |
| role_ids | list[int] | 是   | 要删除的角色 IDs |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "删除分组成功"
}
```

### 6.4 文章管理

#### 6.4.1 文章列表

- 请求URL：`/admin/article`
- 请求方法：`GET`
- 请求参数：

| 参数名     | 类型   | 必选 | 描述                                     |
| ---------- | ------ | ---- | ---------------------------------------- |
| page       | int    | 否   | 页码，默认为1                            |
| count      | int    | 否   | 每页条数，默认为10                       |
| query      | string | 否   | 关键字，用于搜索文章标题和内容           |
| tag_id     | int    | 否   | 标签 ID，用于筛选文章                    |
| cate_id    | int    | 否   | 分类 ID，用于筛选文章                    |
| author_id  | int    | 否   | 作者 ID，用于筛选文章                    |
| start_date | string | 否   | 开始日期，用于筛选文章，格式为YYYY-MM-DD |
| end_date   | string | 否   | 结束日期，用于筛选文章，格式为YYYY-MM-DD |

- 返回参数：

```json
{
    "count": 10,
    "item": [{
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
}
```

#### 6.4.2 设置文章状态

- 请求URL：`/admin/user/status`
- 请求方法：`PUT`
- 请求参数：

| 参数名     | 类型 | 必选 | 说明                          |
| ---------- | ---- | ---- | ----------------------------- |
| article_id | int  | 是   | 文章 ID                       |
| cate       | int  | 否   | 默认1，1-正常，2-拉黑，3-置顶 |

- 返回参数：

```json
{
    "code": 201,
    "error_code": 0,
    "msg": "拉黑或恢复成功"
}
```

#### 6.4.3 标签列表

- 请求URL：`/admin/article/tag`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明              |
| ------ | ------ | ---- | ----------------- |
| query  | string | 否   | 标签名称          |
| page   | int    | 否   | 开始页数，默认为1 |
| count  | int    | 否   | 每页条数，默认20  |

- 返回参数：

```json
{
    "count": 12,
    "data": [{
        "id": 1,
        "name": "tag",
        "article_num": 10
    }]
}
```

#### 6.4.4 标签创建

- 请求URL：`/admin/tag`
- 请求方法：`POST`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明     |
| ------ | ------ | ---- | -------- |
| name   | string | 是   | 标签名称 |

- 返回参数：

```json
 {
     "id": 1,
     "name": "标签名称"
 }
```

#### 6.4.5 标签修改

- 请求URL：`/admin/tag`
- 请求方法：`PUT`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明     |
| ------ | ------ | ---- | -------- |
| name   | string | 是   | 标签名称 |

- 返回参数：

```json
 {
     "id": 1,
     "name": "标签名称"
 }
```

#### 6.4.6 标签删除

- 请求URL：`/admin/tag`
- 请求方法：`DELETE`
- 请求参数：

| 参数名  | 类型      | 必选 | 说明     |
| ------- | --------- | ---- | -------- |
| tag_ids | list[int] | 是   | 标签 IDs |

- 返回参数：

```json
 {
     "code": 200,
     "error_code": 11002,
     "msg": "删除成功"
 }
```

#### 6.4.7 分类列表

- 请求URL：`/admin/article/category`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明              |
| ------ | ------ | ---- | ----------------- |
| query  | string | 否   | 分类名称          |
| page   | int    | 否   | 开始页数，默认为1 |
| count  | int    | 否   | 每页条数，默认20  |

- 返回参数：

```json
{
    "count": 12,
    "data": [{
        "id": 1,
        "name": "category",
        "article_num": 10
    }]
}
```

#### 6.4.8 分类创建

- 请求URL：`/admin/category`
- 请求方法：`POST`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明     |
| ------ | ------ | ---- | -------- |
| name   | string | 是   | 分类名称 |

- 返回参数：

```json
 {
     "id": 1,
     "name": "分类名称"
 }
```

#### 6.4.9 分类修改

- 请求URL：`/admin/category`
- 请求方法：`PUT`
- 请求参数：

| 参数名 | 类型   | 必选 | 说明     |
| ------ | ------ | ---- | -------- |
| name   | string | 是   | 分类名称 |

- 返回参数：

```json
 {
     "id": 1,
     "name": "分类名称"
 }
```

#### 6.4.10 分类删除

- 请求URL：`/admin/category`
- 请求方法：`DELETE`
- 请求参数：

| 参数名   | 类型      | 必选 | 说明     |
| -------- | --------- | ---- | -------- |
| cate_ids | list[int] | 是   | 分类 IDs |

- 返回参数：

```json
 {
     "code": 200,
     "error_code": 11002,
     "msg": "删除成功"
 }
```

### 6.5 评论管理

#### 6.5.1 评论列表

- 请求URL：`/admin/comment`
- 请求方法：`GET`
- 请求参数：

| 参数名     | 类型     | 必选 | 说明              |
| ---------- | -------- | ---- | ----------------- |
| query      | string   | 否   | 评论内容包含词汇  |
| article_id | int      | 否   | 所属文章 ID       |
| user_id    | int      | 否   | 用户 ID           |
| page       | int      | 否   | 开始页数，默认为1 |
| count      | int      | 否   | 每页条数，默认20  |
| date       | datetime | 否   | 起止时间          |

- 返回参数：

```json
{
    "count": 100,
    "data": [{
        "id": 1,
        "article_id": 1,
        "user": {
            "id": 1,
            "username": "xiao",
            "avatar": "https://xx"
        },
        "status": 1,
        "content": "评论内容",
        "ip": "北京市",
        "is_like": false,
        "replay": {
            "replay_count": 12,
            "item":[{
                "root_id": 1,
                "parent_id": 1,
                "id": 1,
                "article_id": 1,
                "user": {
                    "id": 1,
                    "username": "xiao",
                    "avatar": "https://xx"
                },
                "status": 1,
                "content": "评论内容",
                "ip": "北京市",
                "is_like": false
        	}]
		}
    }]
}
```

#### 6.5.2 评论拉黑

- 请求URL：`/admin/comment`
- 请求方法：`DELETE`
- 请求参数：

| 参数名      | 类型      | 必选 | 说明             |
| ----------- | --------- | ---- | ---------------- |
| comment_ids | list[int] | 是   | 要拉黑的评论 IDs |

- 返回参数：

```json
 {
     "code": 200,
     "error_code": 11002,
     "msg": "拉黑成功"
 }
```

### 6.6 通知管理

#### 6.6.1 通知列表

- 请求列表：`/admin/notice`
- 请求方法：`GET`
- 请求参数：

| 参数名     | 类型     | 必选 | 说明              |
| ---------- | -------- | ---- | ----------------- |
| user_id    | int      | 否   | 所属用户 ID       |
| to_user_id | int      | 否   | 发送对象用户 ID   |
| page       | int      | 否   | 开始页数，默认为1 |
| count      | int      | 否   | 每页条数，默认20  |
| date       | datetime | 否   | 起止时间          |

- 返回参数：

```json
{
    "count": 100,
    "data": [{
        "id": 1,
        "user": {
            "id": 1,
            "username": "hello",
            "avatar": "avatar",
        },
        "to_user": {
            "id": 1,
            "username": "hello",
            "avatar": "avatar",
        },
        "content": "消息内容"
    }]
}
```

#### 6.6.2 系统消息创建

- 请求URL：`/admin/notice`
- 请求方法：`POST`
- 请求参数：

| 参数名      | 类型      | 必选 | 说明                  |
| ----------- | --------- | ---- | --------------------- |
| user_id     | int       | 否   | 0 or -1? 表示系统发出 |
| to_user_ids | list[int] | 否   | 发送对象用户 IDs      |
| content     | string    | 否   | 发送内容              |

- 返回参数：

```json
 {
     "code": 200,
     "error_code": 11002,
     "msg": "创建成功"
 }
```

### 6.7 统计信息

- 请求URL：`/admin/stastic`
- 请求方法：`GET`
- 请求参数：无
- 返回参数：

```json
 {
     "user_num": 200,
     "article_num": 100,
     "comment_num": 50
 }
```
