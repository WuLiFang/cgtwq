CGTeamWork Python 客户端

# 用法

安装

```shell
pip install https://github.com/WuLiFang/cgtwq/archive/2.5.0.zip#egg=cgtwq
```

查询字段

```python
import cgtwq

cgtwq.DesktopClient().connect()
module = cgtwq.Database('proj_xiaoying').module('shot', module_type='task')
select = module.filter(
    cgtwq.Field('shot.shot') == 'sc001'),
    cgtwq.Field('shot.eps_name') == 'ep01'),
    cgtwq.Field('task_name') == 'Layout'),)
print(select['submit_file_path'])
```

对应官方 cgtw2 库:

```python
import sys,os
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw2
t_tw = cgtw2.tw("192.168.199.88","xiaoying","cgteamwork")

t_id_list = t_tw.task.get_id('proj_xiaoying','shot',[["shot.shot","=","sc001"],'and',['shot.eps_name','=','ep01'],'and',['task.task_name','=','Layout']])
print t_tw.task.get('proj_xiaoying', "shot",t_id_list, ['task.submit_file_path'])
```
