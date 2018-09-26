CGTeamWork Python 客户端

# 用法

安装

```shell
pip install https://github.com/WuLiFang/cgtwq/archive/2.5.0.zip#egg=cgtwq
```

## 查询字段

```python
import cgtwq

# 从桌面客户端读取登录信息
cgtwq.DesktopClient().connect()
# 或手动设置
cgtwq.core.CONFIG.update(
    SERVER_IP='192.168.199.88',
    DEFAULT_TOKEN=cgtwq.login('xiaoying','cgteamwork').token)


# 访问数据库
module = cgtwq.Database('proj_xiaoying').module('shot', module_type='task')
select = module.filter(
    cgtwq.Field('shot.shot') == 'sc001'),
    cgtwq.Field('shot.eps_name') == 'ep01'),
    cgtwq.Field('task_name') == 'Layout'),)
print(select['submit_file_path']) # 返回: tuple
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","xiaoying","cgteamwork")

t_id_list = t_tw.task.get_id('proj_xiaoying','shot',[["shot.shot","=","sc001"],'and',['shot.eps_name','=','ep01'],'and',['task.task_name','=','Layout']])
print t_tw.task.get('proj_xiaoying', "shot",t_id_list, ['task.submit_file_path']) # 返回: list
```

## 提交任务

```python
import cgtwq

# 从桌面客户端读取登录信息
cgtwq.DesktopClient().connect()
# 或手动设置
cgtwq.core.CONFIG.update(
    SERVER_IP='192.168.199.88',
    DEFAULT_TOKEN=cgtwq.login('xiaoying','cgteamwork').token)

# 访问数据库
module = cgtwq.Database('proj_xiaoying').module('shot', module_type='task')
select = module.filter(
    cgtwq.Field('shot.shot') == 'sc001'),
    cgtwq.Field('shot.eps_name') == 'ep01'),
    cgtwq.Field('task_name') == 'Layout'),)
select.flow.submit(['d:/1.jpg'])
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","xiaoying","cgteamwork")
t_id_list = t_tw.task.get_id('proj_xiaoying','shot',[["shot.shot","=","sc001"],'and',['shot.eps_name','=','ep01'],'and',['task.task_name','=','Layout']])

print t_tw.task.submit('proj_xiaoying',"shot", t_id_list[0], ['d:/1.jpg'])
```

## 获取当前客户端所选

```python
import cgtwq

client = cgtwq.DesktopClient()
select = client.selection()
print(select) # cgtwq.Selection 对象
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw()

print t_tw.client.get_id() # 返回: list
```

## 存储数据

```python
import cgtwq

# 从桌面客户端读取登录信息
cgtwq.DesktopClient().connect()
# 或手动设置
cgtwq.core.CONFIG.update(
    SERVER_IP='192.168.199.88',
    DEFAULT_TOKEN=cgtwq.login('xiaoying','cgteamwork').token)

# 访问数据库
database = cgtwq.Database('proj_big')
database.userdata['test'] = 'data
database.userdata['test']
database.metadata['test'] = 'data
database.metadata['test']
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","xiaoying","cgteamwork")

t_tw.api_data.set("proj_big", "test", "data")
t_tw.api_data.get("proj_big", "test")
t_tw.api_data.set("proj_big", "test", "data", False)
t_tw.api_data.get("proj_big", "test", False)
```

## 获取帐号信息

```python
import cgtwq

# 从桌面客户端读取登录信息
cgtwq.DesktopClient().connect()
# 或手动设置
cgtwq.core.CONFIG.update(
    SERVER_IP='192.168.199.88')

account = cgtwq.login('xiaoying','cgteamwork') # type: namedtuple
account.token
account.account
account.account_id
account.remote_ip
account.name
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","xiaoying","cgteamwork")

t_tw.login.token()
t_tw.login.account()
t_tw.login.account_id()
t_tw.login.http_server_ip()
# 无法获取中文用户名
```
