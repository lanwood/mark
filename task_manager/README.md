## TaskManage 使用

```shell
# 替换 AnomalyServer 和 TrainServer
from mock import AnomalyServer
from mock import TrainServer
```



### TaskManager init and start

```shell
from task_manager import TaskManager as tm
task = tm(template_config)
# template_config 中 任务列表地址对应字段名为 task_list_path
task.start()
```

### create task: anomaly detection 

```shell
task.create_anomaly_task(task_config)  # task_config 内容参考 test_anomaly.py
```

### create task: generate template 

```shell
task.create_generate_template_task(task_config)  # task_config 内容参考 test_template.py
```

### 获取当前任务进度

```shell
task.get_status()
```

```json
// 返回
{"progress": 75, "state": "RUNNING", "type": "FIITER_ANOMALY", "task_id": "1623415302", "create_time": "2021-06-11 20:41:42", "ai_taskId_list": ["1623116143661", ""], "update_time": "2021-06-11 20:42:57"}
```

### 获取任务列表

```shell
task.get_history()
```

```json
{"1623414650": {"progress": 100, "state": "FINISHED", "type": "FIITER_ANOMALY", "task_id": "1623414650", "create_time": "2021-06-11 20:30:50", "ai_taskId_list": ["1623116143661", ""]}, "": {"progress": 100, "state": "FINISHED", "type": "FIITER_ANOMALY", "task_id": "1623414650", "create_time": "2021-06-11 20:30:50", "ai_taskId_list": ["1623116143661", ""]}, "1623415302": {"progress": 75, "state": "RUNNING", "type": "FIITER_ANOMALY", "task_id": "1623415302", "create_time": "2021-06-11 20:41:42", "ai_taskId_list": ["1623116143661", ""], "update_time": "2021-06-11 20:42:57"}}
```

### 重启任务

```shell
// manager_id: task.get_history() 返回的key
task.create_anomaly_task(task_config, task_id)
task.create_generate_template_task(task_config, task_id)
```

