# Subscriber

一个使用存储于数据库中的参数登录网站并完成自定义任务的模块.

- [Subscriber](#subscriber)
- [依赖](#依赖)
- [安装](#安装)
- [使用](#使用)
  - [1. 添加自定义任务](#1-添加自定义任务)
  - [2. 调用 `Subscriber`](#2-调用-subscriber)
- [数据](#数据)
  - [数据库配置](#数据库配置)
    - [数据模型](#数据模型)
      - [Website (网站)](#website-网站)
      - [Account (账号)](#account-账号)
      - [Task (任务)](#task-任务)
      - [Execution (执行)](#execution-执行)
  - [网站](#网站)
    - [简介](#简介)
      - [登录方式](#登录方式)
      - [网站选项](#网站选项)
      - [账号选项](#账号选项)
      - [任务选项](#任务选项)
      - [执行选项](#执行选项)
    - [通用](#通用)
      - [网站选项](#网站选项-1)

# 依赖

- Python 3
  - aiohttp
  - requests

# 安装

```sh
pip install git+https://github.com/Ane794/subscriber.git
```

# 使用

## 1. 添加自定义任务

本模块的一部分目录结构如下:

```yml
- subscriber  # 本项目或调用本项目的项目的根目录
  - websites/  # 自定义脚本的根目录; 名称可自定义, 在本文档中记作 `website_module`
    - example_website/  # 网站的名称
      - example_task.py  # 自定义任务的脚本
```

当用户需要添加一个自定义任务时, 需要如下步骤:

1. 添加一个新网站:
   1. 更新数据库的表格 `website`, 为新网站添加一条记录 (详见 [数据模型 - 网站];
   2. 在 [`website_module`] (自定义脚本根目录) 为网站新建一个目录, 名称与表格 `website` 的字段 `name` 保持一致;
2. 编写一个任务脚本:
   在网站的目录下为任务新建一个脚本 `<任务名>.py`, 继承 [`TaskRunner`] 或 [`TaskAsyncRunner`] 定义一个类 `WebsiteTask`, 重写 `run()` 方法, 在其中编写该任务的主要流程; 如:

   ```py
   """ 文件 websites/example_website/example_task.py """

   from subscriber import Execution, TaskRunner


   class WebsiteTask(TaskRunner):
       """ 示例任务 """

       _BASE_URL = 'https://google.com/'

       def run(self) -> tuple[int, str]:
           """ 任务主要流程. """

           _res = self._get(self._BASE_URL)

           if _res.status_code != 200:
               self._err(_res.text)
           else:
               self._info(_res.text)

           return _res.status_code, _res.text
   ```

3. 添加用户:
   更新数据表的表格 `account`, 为该网站的新用户添加记录 (详见 [数据模型 - 账号]);
4. 添加任务:
   更新数据表的表格 `task`, 为该脚本添加记录 (详见 [数据模型 - 任务]), 字段 `name` 与该脚本名称 (不包含后缀) 保持一致;
5. 添加执行:
   更新数据表的表格 `execution`, 为 _该用户执行该脚本_ 添加记录 (详见 [数据模型 - 执行])

## 2. 调用 `Subscriber`

```py
from subscriber import Subscriber

# 准备实例化 `Subscriber` 所需的参数, 包含了数据库连接配置, 日志存放目录等.
_config = {
  'sql': {  # 数据库连接配置
    'engine': 'sqlite3',  # Python 连接数据库所使用的模块, 如 `sqlite3`, `pymysql` 等
    'database': 'subscriber.sqlite',  # 数据库名
    # 以及其它连接数据库所使用的参数, 如 `host`, `user` 等
  },

  'log': {
    'log_dir': 'logs', # 日志存放目录
  },
}
""" `Subscriber` 配置 """

# 实例化 `Subscriber`.
_subscriber = Subscriber(**_config)

# 执行任务.
website_module = 'websites'
""" 自定义脚本根模块 """
_execution_id: int = 0
""" 执行 ID """
_subscriber.start(website_module, _execution_id)
```

# 数据

## 数据库配置

利用文件 [others/generator-*.sql] 依次创建数据表 `website`, `account`, `task` 和 `execution`.

### 数据模型

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

#### Task (任务)

| 字段名     | 数据类型    | 举例                         | 描述                      |
| ---------- | ----------- | ---------------------------- | ------------------------- |
| id         | int(11)     | `0`                          | 任务 ID                   |
| name       | varchar(21) | `MyUserName`                 | 任务名称                  |
| options    | json        | `{"选项1": 值, "选项2": 值}` | 任务选项; 详见 [任务选项] |
| website_id | int(11)     | `0`                          | 网站 ID                   |

#### Execution (执行)

| 字段名     | 数据类型 | 举例                         | 描述                      |
| ---------- | -------- | ---------------------------- | ------------------------- |
| id         | int(11)  | `1`                          | 执行 ID                   |
| options    | json     | `{"选项1": 值, "选项2": 值}` | 执行选项; 详见 [执行选项] |
| task_id    | int(11)  | `1`                          | 任务 ID                   |
| account_id | int(11)  | `1`                          | 账号 ID                   |

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

_网站选项_ 描述了一个网站的所有执行都共用的选项.

例如, 网站 [`example_website`] 当前需要配置代理, 而其他网站不需要,
因此选项 `proxies` 是 [`example_website`] 的 _网站选项_.

#### 账号选项

_账号选项_ 描述了一个账号在执行时与其他账号不同的选项.
_网站选项_ 中的同名选项会被覆盖.

例如, [`example_website`] 的每个账号都有不同的地区,  
所以它选项 `region` 是 [`example_website`] 的账号的 _账号选项_.

#### 任务选项

_任务选项_ 描述了一个任务在执行时与其他任务不同的选项.
_账号选项_ 和 _网站选项_ 中的同名选项会被覆盖.

#### 执行选项

_执行选项_ 描述了一个执行与其他执行不同的选项.
_任务选项_, _账号选项_ 和 _网站选项_ 中的同名选项会被覆盖.

### 通用

#### 网站选项

| 选项名  | 非空 | 数据类型 | 举例                                 | 描述                                       |
| ------- | ---- | -------- | ------------------------------------ | ------------------------------------------ |
| debug   | 否   | bool     | `true`                               | debug 模式; 为 `true` 时会输出更详细的日志 |
| proxies | 否   | json     | `{"HTTP": "http://localhost:1080/"}` | Requests 所使用的代理                      |

[数据模型 - 网站]: #website-网站
[数据模型 - 账号]: #account-账号
[数据模型 - 任务]: #task-任务
[数据模型 - 执行]: #execution-执行
[登录方式]: #登录方式
[网站选项]: #网站选项
[账号选项]: #账号选项
[任务选项]: #任务选项
[执行选项]: #执行选项
[main.py]: main.py
[others/generator-*.sql]: others/
[`example_website`]: websites/example_website/
[`website_module`]: websites/
[`TaskRunner`]: subscriber/utils/task_runner/__init__.py
[`TaskAsyncRunner`]: subscriber/utils/task_runner/__init__.py
