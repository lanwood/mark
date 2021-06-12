from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
import threading
import time
import os
import json
from enum import Enum

from mock import AnomalyServer
from mock import TrainServer

# from .mock import AnomalyServer
# from train_server.train_server import TrainServer


import multiprocessing as mp


class TaskType(Enum):
    FIITER_ANOMALY = 0 
    GENERATE_TEMPLATE = 1


class TaskStatus(Enum):
    IDLE = 0 
    RUNNING = 1
    ERROR = 2
    AOBRTED = 3
    FINISHED = 4


class TaskManager():
    def __init__(self, config):
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.anomaly_dict = {}
        self.template_dict = {}

        self.manager_id = ""

        self.target_task = None
        self.status_dict = {}
        self.task_type = TaskType.FIITER_ANOMALY.value
        self.history = {}

        # 获取状态保存路径
        self.status_path = self.config.get('workspace','task_list_path')

        # 子进程处理
        CPU_NUM = 1
        self.pools = mp.Pool(CPU_NUM)



    def start(self):
        # TODO 检测未完成的任务, 更新状态任务
        if self.status_path and os.path.exists(self.status_path):
            print(self.status_path)
            with open(self.status_path, 'r') as f:
                self.history = json.load(f)
                print("TaskManager: history task" ,self.history)



    def close(self):
        pass


    def _running_status(self):
        print("TaskManager: status monitor ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        task_msg = self.target_task.get_status()
        print("TaskManager:" ,task_msg)
 
        if self.task_type == TaskType.FIITER_ANOMALY.value:
            if task_msg.get('aiTaskIdList'):
                self.status_dict['ai_taskId_list'] = task_msg.get('aiTaskIdList')
                self.status_dict['progress'] = min(task_msg['progress'] // 2, 50)
                if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                    # 开始异常检测
                    self._create_anomaly(self.anomaly_dict.get('anomalyDetectList'))
                    
                    # 子进程处理
                    # f = self.pools.apply_async(self._create_anomaly, [self.anomaly_dict.get('anomalyDetectList')])
                    # f.get()

                    # 子线程处理
                    # t= threading.Thread(target=self._create_anomaly, args=(self.anomaly_dict.get('anomalyDetectList'),))
                    # t.setDaemon(False)
                    # t.start()

            else:
                self.status_dict['progress'] = min(50  +  (task_msg['progress'] // 2), 100)
                if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                    self.stop_manager_task()

            if self.status_dict.get('progress') > 0 and self.status_dict.get('progress') < 100:
                self.status_dict['state'] = TaskStatus.RUNNING.name
            else:
                self.status_dict['state'] = task_msg['state']

        if self.task_type == TaskType.GENERATE_TEMPLATE.value:
            self.status_dict = task_msg
            if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                self.stop_manager_task()

        # 更新状态
        self.status_dict['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.history[self.manager_id] = self.status_dict
        with open(self.status_path, 'w+') as f: 
            json.dump(self.history, f)



    def _create_anomaly(self, detect_dict):
        self.target_task = AnomalyServer(detect_dict)
        self.target_task.start()


    def _create_template(self, train_dict, task_id=None):

        if task_id:
            train_dict['taskIdList'] = self.history[task_id].get('taskIdList', ["", ""])
            self.status_dict = self.history[task_id]
        else:
            train_dict['taskIdList'] = ["", ""]
            self.status_dict = {
                "progress": 0,
                "state": "IDLE",
                'task_id': self.manager_id,
                'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }

        self.target_task = TrainServer(train_dict)
        self.target_task.start()

        
    # 筛选异常
    def create_anomaly_task(self, detect_dict, task_id=None):
        if self.manager_id:
            return False
        print("TaskManager: create anomaly task")
        self.manager_id = str(int(time.time()))
        self.task_type = TaskType.FIITER_ANOMALY.value

        self.anomaly_dict.update(detect_dict)

        self._create_template(self.anomaly_dict, task_id)

        self.status_dict.update({
            'type': TaskType.FIITER_ANOMALY.name
        })

        self.scheduler.add_job(self._running_status, 'interval', seconds=5, id=self.manager_id)
        
        return True

    # 生成模板 
    def create_generate_template_task(self, train_dict, task_id=None):
        if self.manager_id:
            return False
        print("TaskManager: create generate template task")
        self.manager_id = str(int(time.time()))
        self.task_type = TaskType.GENERATE_TEMPLATE.value

        self.template_dict.update(train_dict)

        self._create_template(self.template_dict, task_id)

        self.status_dict.update({
            'type': TaskType.GENERATE_TEMPLATE.name
        })

        self.scheduler.add_job(self._running_status, 'interval', seconds=5, id=self.manager_id)

        return True

    # 停止任务
    def stop_manager_task(self):
        print("TaskManager: stop task")
        self.target_task.close()
        self.scheduler.remove_job(self.manager_id, jobstore=None)
        self.manager_id = ""

    # 获取任务状态
    def get_status(self):
        print("labelImg: get status")
        return self.status_dict

    # 获取历史任务状态
    def get_history(self):
        print("labelImg: get history")
        return list(self.history.values())

    # 获取历史任务状态
    def set_config(self):
        print("labelImg: set config")
        self.config = config
