-- 使用数据库
-- USE pmoe;
CREATE TABLE `user` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '',
    `username` varchar(32) NOT NULL COMMENT '昵称',
    `mobile` char(16) NULL COMMENT '手机号',
    `password` varchar(255) NOT NULL COMMENT '密码',
    `role_id` bigint(20) unsigned NOT NULL DEFAULT '1' COMMENT '角色 ID: 1-普通用户, 2-撰稿者, 3-虚拟用户',
    `signature` varchar(200) NULL COMMENT '个性签名',
    `avatar` varchar(255) NULL COMMENT '头像',
    `email` varchar(255) NULL UNIQUE COMMENT '邮箱账号',
    `last_login` datetime NULL COMMENT '最后登录时间',
    `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态: 0-未激活, 1-正常, 2-禁言, 3-拉黑',
    `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除: 0-没有, 1-已删除',
    `gender` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别: 0-未设置, 1-女, 2-男',
    `birthday` date NULL COMMENT '生日',
    `address` varchar(32) COMMENT '地区',
    `company` varchar(32) COMMENT '公司',
    `career` varchar(32) COMMENT '职业',
    `home_url` varchar(255) COMMENT '个人主页',
    `github` varchar(255) COMMENT 'GitHub 主页',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    `article_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '发文数量',
    `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计点赞数',
    PRIMARY KEY (`id`),
    UNIQUE KEY `username_del` (`username`, `is_deleted`),
    UNIQUE KEY `mobile_del` (`mobile`, `is_deleted`),
    UNIQUE KEY `email_del` (`email`, `is_deleted`),
    KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

CREATE TABLE `role` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '角色 ID',
    `name` varchar(32) NOT NULL COMMENT '角色名称',
    `info` varchar(255) NULL COMMENT '描述',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    -- `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态: 1-有效, 0-无效',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色';

-- 初始化 role 数据
INSERT INTO `role` (`name`) VALUES ('普通用户'), ('撰稿者'), ('虚拟用户');

CREATE TABLE `permission` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` varchar(32) NOT NULL COMMENT '权限名称',
    `module` varchar(32) NOT NULL DEFAULT 'default' COMMENT '所属模块, 分类权限',
    `info` varchar(255) NULL COMMENT '描述',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

CREATE TABLE `role_permission` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `role_id` bigint(20) unsigned NOT NULL COMMENT '角色 ID',
    `permission_id` bigint(20) unsigned NOT NULL COMMENT '权限 ID',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `role_permission` (`role_id`, `permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限表';

CREATE TABLE `category` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` varchar(32) NOT NULL COMMENT '分类名称',
    `info` varchar(200)  COMMENT '描述',
    `banner` varchar(255) NULL COMMENT '分类背景图',
    `sort` int(11) unsigned NOT NULL DEFAULT '1' COMMENT '排序',
    `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否可见: 1-可见, 0-不可见',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除: 0-没有, 1-已删除',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name_del` (`name`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章分类表';


CREATE TABLE `tag` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `name` varchar(32) NOT NULL COMMENT '分类名称',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章标签表';


CREATE TABLE `article` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `title` varchar(128) NOT NULL COMMENT '文章标题',
    `summary` varchar(255) COMMENT '摘要',
    `content` longtext Not NULL COMMENT '文章内容',
    `cover` varchar(255) COMMENT '封面',
    `category_id` bigint(20) unsigned NULL COMMENT '分类: null 未分类',
    `source` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '来源: 1-原创, 2-转载、3-翻译',
    `publish` tinyint(1) NOT NULL DEFAULT '1' COMMENT '可见范围: 1-公开, 2-登录可见, 3-仅自己可见',
    `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态: 0-不可见, 1-正常, 2-作者置顶, 3-管理员置顶',
    `sort` int(11) NOT NULL DEFAULT '1' COMMENT '推荐排序',
    `allow_comment` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否允许评论: 1-允许, 0-不允许',
    `user_id` bigint(20) unsigned NOT NULL COMMENT '用户 ID',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除: 0-没有, 1-已删除',
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

CREATE TABLE `article_like` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` bigint(20) unsigned NOT NULL COMMENT '用户 ID',
    `article_id` bigint(20) unsigned NOT NULL COMMENT '文章 ID',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '文章点赞表';

CREATE TABLE `article_tag` (
    `article_id` bigint(20) unsigned NOT NULL COMMENT '文章 ID',
    `tag_id` bigint(20) unsigned NOT NULL COMMENT '标签 ID',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`article_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COMMENT '文章内容表';

CREATE TABLE `file` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `md5` varchar(100) NOT NULL COMMENT '文件唯一标识',
    `user_id` bigint(20) unsigned NOT NULL COMMENT '用户 ID',
    `location` tinyint(1) unsigned NULL DEFAULT '1' COMMENT '存储位置: 1-本地, 2-远程',
    `type` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '素材类型: 0-未知, 1-图片, 2-视频, 3-音频',
    `ext` varchar(10) COMMENT '后缀',
    `path` varchar(100) NOT NULL COMMENT '文件路径或url',
    `name` varchar(50) NOT NULL COMMENT '文件名称',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_file` (`user_id`, `md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '上传文件表';

CREATE TABLE `comment` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章 ID',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户 ID',
  `content` varchar(400) COMMENT '评论内容',
  `root_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '所属根评论 ID, 0表示自身就是根评论',
  `parent_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '父级评论 ID, 0表示根评论',
  `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
  `reply_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '回复数',
  `ip` varchar(16) NULL COMMENT 'ip 地址',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态: 1-正常, 0-隐藏, 2-作者置顶, 3-后台置顶',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除: 0-没有, 1-已删除',
  PRIMARY KEY (`id`),
  KEY `root_id` (`root_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

CREATE TABLE `comment_like` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `user_id` bigint(20) unsigned NOT NULL COMMENT '用户 ID',
    `comment_id` bigint(20) unsigned NOT NULL COMMENT '主键 ID',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_comment` (`user_id`, `comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论点赞表';

CREATE TABLE `notice` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    `content` varchar(200) NOT NULL COMMENT '内容',
    `to_user_id` bigint(20) unsigned NOT NULL COMMENT '接收消息用户 ID',
    `from_user_id` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '发送消息用户 ID, 0-系统',
    `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已读: 0-未读, 1-已读',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `from_user` (`from_user_id`),
    KEY `to_user` (`to_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通知表';
