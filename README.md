CGTeamWork Python 客户端

# 用法

安装

```shell
pip install --process-dependency-links https://github.com/WuLiFang/cgtwq/archive/3.0.0-alpha.0.zip#egg=cgtwq
```

## 初始设置

### 从桌面客户端读取登录信息

```python
import cgtwq

cgtwq.DesktopClient().connect()
```

官方库不支持这样做

### 手动设置

```python
import cgtwq

token = cgtwq.login('username','password').token

# 设置服务器IP, 默认为 192.168.55.11
cgtwq.core.CONFIG.update(SERVER_IP='192.168.199.88')

# 模块级登录标识设置
cgtwq.core.CONFIG.update(DEFAULT_TOKEN=token)

# 对象级登录标识设置, 如果未设置则会自动向上一级读取
database = cgtwq.Database('proj_big')
database.token = token
module = database.module('shot')
module.token = token
select = module.select('dummy_id')
select.token = token
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","username","password")
# 之后所有操作都在 t_tw 上进行
```

## 处理字段数据

```python
module = cgtwq.Database('proj_big').module('shot', module_type='task')
select = module.filter(
    cgtwq.Field('shot.shot') == 'sc001'),
    cgtwq.Field('shot.eps_name') == 'ep01'),
    cgtwq.Field('task_name') == 'Layout'),)

# 查询单列, 返回: tuple
select['submit_file_path']

# 查询多列, 返回: cgtwq.ResultSet 对象,
# cgtwq.ResultSet 是 list 的子类,
# 内部每个元素都是 list 和每个条目对应
# 内部 list 值的顺序和输入顺序相同
# 可使用 ResultSet.column('#id') 得到指定列的 tuple
select.get_fields('#id', 'submit_file_path')

# 设置单列
select['shot.frame'] = '3333'

# 设置多列
select.set_fields(**{'shot.frame': '3333'})
```

对应官方 cgtw2 库:

```python
t_id_list = t_tw.task.get_id(
    'proj_big','shot',
    [["shot.shot","=","sc001"],
    'and',['shot.eps_name','=','ep01'],
    'and',['task.task_name','=','Layout']])

# 查询多列 返回: list[dict]
# 字典的键为输入的字段加上'id'
t_tw.task.get('proj_big', "shot",t_id_list, ['task.submit_file_path'])

# 设置多列
t_tw.task.set('proj_big',"shot", t_id_list, {'shot.frame':'3333'})
```

## 管理任务状态

```python
module = cgtwq.Database('proj_big').module('shot', module_type='task')
select = module.filter(
    cgtwq.Field('shot.shot') == 'sc001'),
    cgtwq.Field('shot.eps_name') == 'ep01'),
    cgtwq.Field('task_name') == 'Layout'),)

# 提交
select.flow.submit(['d:/1.jpg'])
# 通过
select.flow.approve('leader_status')
# 返修
select.flow.retake('leader_status')
# 关闭
select.flow.close('leader_status')
# 其他状态
select.flow.update('leader_status', 'other')
```

对应官方 cgtw2 库:

```python
t_id_list = t_tw.task.get_id(
    'proj_big','shot',
    [["shot.shot","=","sc001"],
    'and',['shot.eps_name','=','ep01'],
    'and',['task.task_name','=','Layout']])

# 提交
t_tw.task.submit('proj_big',"shot", t_id_list[0], ['d:/1.jpg'])
# 通过
t_tw.task.update_flow('proj_big',"shot", t_id_list[0], 'task.leader_status', 'Approve')
# 返修
t_tw.task.update_flow('proj_big',"shot", t_id_list[0], 'task.leader_status', 'Retake')
# 关闭
t_tw.task.update_flow('proj_big',"shot", t_id_list[0], 'task.leader_status', 'Close')
# 其他状态
t_tw.task.update_flow('proj_big',"shot", t_id_list[0], 'task.leader_status', 'other')
# 以上函数都需要检查函数返回值为True, 不能用捕获异常的方式
```

## 获取当前客户端所选条目

```python
client = cgtwq.DesktopClient()
select = client.selection()
# select 为 cgtwq.Selection 对象
# cgtwq.Selection 是 list 的子类
# 可以直接在上面进行操作
```

对应官方 cgtw2 库:

```python
t_tw = cgtw2.tw()

id_list = t_tw.client.get_id()
# id_list 为 list
# 作为其他函数的参数使用
```

## 存储数据

```python
database = cgtwq.Database('proj_big')
# 用户信息
database.userdata['test'] = 'data
database.userdata['test']
# 数据库信息
database.metadata['test'] = 'data
database.metadata['test']
```

对应官方 cgtw2 库:

```python
# 用户信息
t_tw.api_data.set("proj_big", "test", "data")
t_tw.api_data.get("proj_big", "test")
# 数据库信息
t_tw.api_data.set("proj_big", "test", "data", False)
t_tw.api_data.get("proj_big", "test", False)
```

## 获取登录信息

```python
account = cgtwq.login('username','password') # type: namedtuple
account.token
account.account
account.account_id
account.remote_ip
account.name
```

对应官方 cgtw2 库:

```python
t_tw.login.token()
t_tw.login.account()
t_tw.login.account_id()
t_tw.login.http_server_ip()
# 无法获取中文用户名
```
