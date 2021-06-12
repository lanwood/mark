from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
import threading
import time
import os
import json
from enum import Enum, unique

from mock import AnomalyServer
from mock import TrainServer

import multiprocessing as mp


@unique
class TaskType(Enum):
    FILTER_ANOMALY = 0
    GENERATE_TEMPLATE = 1


@unique
class TaskStatus(Enum):
    IDLE = 0
    RUNNING = 1
    ERROR = 2
    ABORTED = 3
    FINISHED = 4


@unique
class SubTaskMode(Enum):
    MAIN = 0
    THREAD = 1
    PROCESS = 2


def _create_anomaly_process(task_process):
    task_process.start()


class TaskManager:
    def __init__(self, config, callback=None):
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.anomaly_dict = {}
        self.template_dict = {}

        self.manager_id = ""

        self.target_task = None
        self.status_dict = {}
        self.task_type = TaskType.FILTER_ANOMALY.value
        self.history = {}

        # 获取状态保存路径
        self.status_path = self.config.get('workspace', 'task_history.json')

        self.callback = callback

        # 子进程处理
        cpu_num = mp.cpu_count()
        self.pools = mp.Pool(cpu_num)
        print("cpu_num: ", cpu_num)
        self.start_mode = SubTaskMode.PROCESS.value
        print("sub_task_mode:", SubTaskMode(self.start_mode))

    def start(self):
        # TODO 检测未完成的任务, 更新状态任务
        if self.status_path and os.path.exists(self.status_path):
            print(self.status_path)
            with open(self.status_path, 'r') as f:
                self.history = json.load(f)
                print("TaskManager: history task", self.history)

    def close(self):
        pass

    def _running_status(self):
        print("TaskManager: status monitor ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        task_msg = self.target_task.get_status()
        print("TaskManager:", task_msg)

        # 更新任务进度
        if self.task_type == TaskType.FILTER_ANOMALY.value:
            if task_msg.get('aiTaskIdList'):
                self.status_dict['ai_taskId_list'] = task_msg.get('aiTaskIdList')
                self.status_dict['progress'] = min(task_msg['progress'] // 2, 50)
                if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                    # # 开始异常检测
                    if self.start_mode == SubTaskMode.MAIN.value:
                        self._create_anomaly(self.anomaly_dict.get('anomalyDetectList'))

                    # # 子线程处理
                    if self.start_mode == SubTaskMode.THREAD.value:
                        t = threading.Thread(target=self._create_anomaly,
                                             args=(self.anomaly_dict.get('anomalyDetectList'),))
                        t.setDaemon(False)
                        t.start()

                    # # 子进程处理
                    if self.start_mode == SubTaskMode.PROCESS.value:
                        self.target_task = AnomalyServer(self.anomaly_dict.get('anomalyDetectList'))
                        f = self.pools.apply_async(_create_anomaly_process, [self.target_task])
                        f.get()
            else:
                self.status_dict['progress'] = min(50 + (task_msg['progress'] // 2), 100)
                if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                    self.stop_manager_task()

            if 0 < self.status_dict.get('progress') < 100:
                self.status_dict['state'] = TaskStatus.RUNNING.name
            else:
                self.status_dict['state'] = task_msg['state']

        if self.task_type == TaskType.GENERATE_TEMPLATE.value:
            self.status_dict = task_msg
            if task_msg.get('progress') >= 100 and task_msg.get('state') == "FINISHED":
                self.stop_manager_task()

        # 更新历史任务列表
        self.status_dict['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if self.history.get(self.manager_id) \
                and \
                (self.history.get(self.manager_id).get('state') != self.status_dict.get('state')
                 or
                 self.history.get(self.manager_id).get('progress') // 10 != self.status_dict.get('progress') // 10):
            self.history[self.manager_id] = self.status_dict
            with open(self.status_path, 'w+') as f:
                json.dump(self.history, f)
        else:
            self.history[self.manager_id] = self.status_dict

        # 调用回调
        if self.callback:
            self.callback(self.history)

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
                "state": TaskStatus.IDLE.name,
                'task_id': self.manager_id,
                'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }

        self.target_task = TrainServer(train_dict)
        self.target_task.start()

    def _task_process(self, param_dict, task_type, target_dict, task_id):
        self.task_type = task_type
        self.manager_id = str(int(time.time()))
        target_dict.update(param_dict)
        self._create_template(target_dict, task_id)
        self.status_dict.update({
            'type': task_type
        })
        self.scheduler.add_job(self._running_status, 'interval', seconds=5, id=self.manager_id)

    # 筛选异常
    def create_anomaly_task(self, detect_dict, task_id=None):
        if self.manager_id:
            return False, self.status_dict
        print("TaskManager: create anomaly task")
        self._task_process(detect_dict, TaskType.FILTER_ANOMALY.value, self.anomaly_dict, task_id)
        self.task_type = TaskType.FILTER_ANOMALY.value
        return True, self.status_dict

    # 生成模板 
    def create_generate_template_task(self, train_dict, task_id=None):
        if self.manager_id:
            return False, self.status_dict
        print("TaskManager: create generate template task")
        self._task_process(train_dict, TaskType.GENERATE_TEMPLATE.value, self.template_dict, task_id)
        return True, self.status_dict

    # 停止任务
    def stop_manager_task(self):
        print("TaskManager: stop task")
        self.target_task.close()
        self.scheduler.remove_job(self.manager_id)
        self.manager_id = ""

    # 获取当前任务状态
    def get_status(self):
        print("labelImg: get status")
        return self.status_dict

    # 获取历史任务状态
    def get_history(self):
        print("labelImg: get history")
        return list(self.history.values())

    # 更新config
    def set_config(self, config):
        print("labelImg: set config")
        self.config = config
