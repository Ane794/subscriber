# Subscriber

一个使用存储于数据库中的参数登录网站并完成自定义任务的模块.

# 依赖

- Python 3
- [requirements] 所列出的 Python 3 模块

# 运行

使用以下命令获取帮助:

```shell
python -m main -h
```

日志默认存储在目录 [logs] 下.

# 数据

## 数据库配置

1. 在 [config.yml] 中的 `sql` 字段配置连接的数据库与账号, 密码等;  
   默认为目录下的 [subscriber.sqlite].

2. 利用文件 [others/generator-*.sql] 依次创建数据表 `website`, `account` 和 `work`.

## 数据模型

#### Website (网站)

| 字段名  | 数据类型 | 举例                         | 描述                      |
| ------- | -------- | ---------------------------- | ------------------------- |
| id      | int(11)  | `0`                          | 网站 ID                   |
| name    | longtext | `AWebsiteName`               | 网站名称                  |
| options | json     | `{"选项1": 值, "选项2": 值}` | 网站选项; 详见 [网站选项] |

#### Account (账号)

| 字段名     | 数据类型    | 举例                         | 描述                                 |
| ---------- | ----------- | ---------------------------- | ------------------------------------ |
| id         | int(11)     | `0`                          | 账号 ID                              |
| name       | varchar(21) | `MyUserName`                 | 账号名称                             |
| login_key  | longtext    | `MyPassword`                 | 登录密钥; 详见 [登录方式]            |
| nick_name  | longtext    | `My Nickname`                | 账号昵称; 用于显示在日志或其他 UI 上 |
| options    | json        | `{"选项1": 值, "选项2": 值}` | 账号选项; 详见 [账号选项]            |
| website_id | int(11)     | `0`                          | 网站 ID                              |

#### Work (任务)

| 字段名     | 数据类型    | 举例                         | 描述                      |
| ---------- | ----------- | ---------------------------- | ------------------------- |
| id         | int(11)     | `1`                          | 任务 ID                   |
| name       | varchar(21) | `AWorkName`                  | 任务名称                  |
| options    | json        | `{"选项1": 值, "选项2": 值}` | 任务选项; 详见 [任务选项] |
| account_id | int(11)     | `1`                          | 账号 ID                   |

## 网站

### 简介

#### 登录方式

本项目的不同网站可能使用不同的 _登录方式_, 目前有 _用户名(账号)密码登录_ 和 _Cookies 登录_ 两种.

`login_key` 是登录密钥, 可能是账号的密码或 Cookies 等; 这取决于网站的登录方式.

例如:

- 当 _登录方式_ 是 `账号名, 密码` 时, `login_key` 是账号的密码;
- 当 _登录方式_ 是 `Cookies: {uuid, sid}` 时, `login_key` 是账号的 Cookies, 且需要 `uuid`, `sid` 两个字段,
  形如 `{"uuid": "...", "sid": "..."}`.

#### 网站选项

_网站选项_ 描述了一个网站的所有账号都共用的参数.

例如, 网站 [`example_website`] 当前需要配置代理, 而其他网站不需要,
因此代理对应的参数 `proxies` 是 [`example_website`] 独有的;  
[`example_website`] 的每个账号都共用同一个代理, 因此 `proxies` 是 [`example_website`] 的 _网站选项_.

#### 账号选项

_账号选项_ 描述了一个网站的每个账号不同的参数.

例如, [`example_website`] 的每个账号都有不同的地区, 且其他网站的账号没有这个选项,
所以它对应的参数 `region` 是 [`example_website`] 独有的;  
且每个账号的这个参数是不同的, 因此 `region` 是 [`example_website`] 的 _账号选项_.

#### 任务选项

例如, 网站 [`example_website`] 的任务 [`example_work`] 当前需要配置代理, 而其他任务不需要,  
因此代理对应的参数 `proxies` 是 [`example_work`] 独有的;  
[`example_work`] 的每个账号都共用同一个代理, 因此 `proxies` 是 [`example_work`] 的 _任务选项_.

### 通用

#### 网站选项

| 选项名  | 非空 | 数据类型 | 举例                                 | 描述                                       |
| ------- | ---- | -------- | ------------------------------------ | ------------------------------------------ |
| debug   | 否   | bool     | `true`                               | debug 模式; 为 `true` 时会输出更详细的日志 |
| proxies | 否   | json     | `{"HTTP": "http://localhost:1080/"}` | Requests 所使用的代理                      |

[登录方式]: #登录方式
[网站选项]: #网站选项
[账号选项]: #账号选项
[任务选项]: #任务选项
[logs]: logs/
[main.py]: test.py
[config.yml]: config.yml
[others/generator-*.sql]: others/
[requirements]: requirements
[subscriber.sqlite]: subscriber.sqlite
[`example_website`]: websites/example_website/
[`example_work`]: websites/example_website/example_work.py
