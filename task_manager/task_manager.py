from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
import threading
import time
import os
import json
from enum import Enum, unique

from mock import AnomalyServer
from mock import TrainServer

# from anomaly_detect.AnomalyDetection import AnomalyDetection as AnomalyServer
# from train_server.train_server import TrainServer


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
    FINISH = 4


@unique
class SubTaskMode(Enum):
    MAIN = 0
    THREAD = 1
    PROCESS = 2


    
def _create_anomaly_process(task_process):
    task_process.start()
    
class TaskManager():
    def __init__(self, config, callback=None):
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.anomaly_dict = {}
        self.template_dict = {}

        self.target_task = {}
        self.history = {}

        self.is_overleap = True # whether to skip Stage One

        # 获取状态保存路径
        self.status_path = self.config.get('workspace', 'task_list_path')

        self.callback = callback
                
        self.start_mode = SubTaskMode.MAIN.value
        print("sub_task_mode:", SubTaskMode(self.start_mode))

        # 子进程处理
        cpu_num = mp.cpu_count()
        self.pools = mp.Pool(cpu_num)
        print("cpu_num: ", cpu_num)

    def start(self):
        if self.status_path and os.path.exists(self.status_path):
            with open(self.status_path, 'r') as f:
                self.history = json.load(f)

                # 检测未完成的任务, 重启任务
                running_history = [t for (k, t) in self.history.items() if t.get('state') in [TaskStatus.RUNNING.name,  TaskStatus.IDLE.name]]

                # 多个未完成任务，只启动最后的任务
                if len(running_history) > 0:
                    running_history = running_history[-1:]

                for retask in running_history:
                    task_key = retask.get('task_id')
                    if retask.get('param') and task_key:
                        target_update = None
                        if retask.get('type') == TaskType.FILTER_ANOMALY.name:
                            if retask.get('progress', 100) < 50:
                                target_update = TrainServer(retask.get('param', {}))
                            else:
                                retask['progress'] = 50
                                target_update = AnomalyServer(retask.get('param', {}).get('anomalyDetectList', []), task_key)
                        elif retask.get('type') == TaskType.GENERATE_TEMPLATE.name:
                            target_update = TrainServer(retask.get('param'), {})
                        if target_update:
                            self.target_task[task_key] = target_update
                            self.target_task[task_key].start()
                            print("TaskManager: restart task ", task_key, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), retask['progress'], retask.get('type'))
                            self.scheduler.add_job(self._running_status, 'interval', seconds=5, args=[task_key], id=task_key)
                            self.history.get(task_key, {})['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            self._dump_history()


    def close(self, task_id=None):
        return self.stop_manager_task(task_id)

    def stop(self, task_id=None):
        if not task_id:
            return
        return self.stop_manager_task(task_id)

    def _running_status(self, manager_id=None):
        if not manager_id:
            return
        print("TaskManager: status monitor ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), manager_id)
        task_msg = self.target_task.get(manager_id).get_status()
        print("TaskManager: receive ", task_msg)

        # 按需更新
        # status_dict = self.history.get(manager_id).copy()
        # 实时更新
        status_dict = self.history.get(manager_id)

        task_type = status_dict.get('type')

        # 返回的进度小于历史任务进度时，不更新任务进度
        if task_msg.get('state') in [TaskStatus.RUNNING.name, TaskStatus.IDLE.name] \
            and ((task_type == TaskType.FILTER_ANOMALY.name and task_msg.get('aiTaskIdList') and min(task_msg['progress'] // 2, 50) <= status_dict['progress'])
            or (task_type == TaskType.GENERATE_TEMPLATE.name and task_msg['progress'] <= status_dict['progress'])
            or (task_type == TaskType.FILTER_ANOMALY.name and not task_msg.get('aiTaskIdList') and min(50 + (task_msg['progress'] // 2), 100) <= status_dict['progress'])):
            record_ts = time.mktime(time.strptime(status_dict.get('update_time'),'%Y-%m-%d %H:%M:%S'))
            current_ts = int(time.time())
            overtime = current_ts - record_ts
            print("TaskManager: Status not updated ", manager_id, status_dict.get('update_time'), "+", overtime, "s;", "record progress: ", status_dict['progress'])
            if overtime > 300: # 超出5min进度未更新, 停止任务
                print("TaskManager: Task Overtime")
                self.stop(manager_id)
            return
  
        status_dict.update(task_msg)
        if task_type == TaskType.FILTER_ANOMALY.name:
            if task_msg.get('aiTaskIdList'):
                status_dict['progress'] = min(task_msg['progress'] // 2, 50)
                if task_msg.get('progress') >= 100 and task_msg.get('state') == TaskStatus.FINISH.name:
                    # 更新 anomalyDetectList
                    model_param = task_msg.get('modelParam', [])
                    anomaly_detect_list = status_dict.get('param', {}).get('anomalyDetectList', [])
                    if len(model_param) >= len(anomaly_detect_list):
                        for index, anomaly_detect in enumerate(anomaly_detect_list):
                            anomaly_detect['scoreMapThre'] = model_param[index].get('scoreMapThre')

                    # # 开始异常检测
                    if self.start_mode == SubTaskMode.MAIN.value:
                        self._create_anomaly(self.anomaly_dict.get('anomalyDetectList'), status_dict.get('task_id'))

                    # # 子线程处理
                    if self.start_mode == SubTaskMode.THREAD.value:
                        t = threading.Thread(target=self._create_anomaly,
                                             args=(self.anomaly_dict.get('anomalyDetectList'), status_dict.get('task_id'),))
                        t.setDaemon(False)
                        t.start()

                    # # 子进程处理
                    if self.start_mode == SubTaskMode.PROCESS.value:
                        self.target_task = AnomalyServer(self.anomaly_dict.get('anomalyDetectList'))
                        f = self.pools.apply_async(_create_anomaly_process, [self.target_task, status_dict.get('task_id')])
                        f.get()
                        
                if not task_msg.get('state') in [TaskStatus.RUNNING.name, TaskStatus.FINISH.name]:
                    # self.stop_manager_task(manager_id)
                    task_list = self.scheduler.get_jobs()
                    task_id_list = [task.id for task in task_list]
                    if manager_id in task_id_list:
                        print("TaskManager: stop timer ", manager_id)
                        self.scheduler.remove_job(manager_id)
                        
            else:
                status_dict['progress'] = min(
                    50 + (task_msg['progress'] // 2), 100)
                if not task_msg.get('state') in [TaskStatus.RUNNING.name]:
                    self.stop_manager_task(manager_id)

                    # 调用回调
                    if self.callback:
                        self.callback()

                    # task_list = self.scheduler.get_jobs()
                    # task_id_list = [task.id for task in task_list]
                    # if manager_id in task_id_list:
                    #     print("TaskManager: stop timer ", manager_id)
                    #     self.scheduler.remove_job(manager_id)

        if task_type == TaskType.GENERATE_TEMPLATE.name:
            if not task_msg.get('state') in [TaskStatus.RUNNING.name]:
                # self.stop_manager_task(manager_id)
                task_list = self.scheduler.get_jobs()
                task_id_list = [task.id for task in task_list]
                if manager_id in task_id_list:
                    print("TaskManager: stop timer ", manager_id)
                    self.scheduler.remove_job(manager_id)

        # 更新历史任务列表
        status_dict['update_time'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        if 0 < status_dict.get('progress') < 100 and task_msg['state'] == TaskStatus.FINISH.name:
            status_dict['state'] = TaskStatus.RUNNING.name
        else:
            status_dict['state'] = task_msg['state']
        print("TaskManager: processed ", status_dict)
        print("TaskManager: update history task file ", status_dict.get('task_id'))

        # # 按需更新
        # key_id = status_dict.get('task_id')
        # if key_id and (not self.history.get(key_id) or self.history[key_id].get('progress') > 80 or (
        #         self.history.get(key_id) and (
        #         self.history[key_id].get('state') != status_dict.get('state') or
        #         self.history[key_id].get('progress') // 10 != status_dict.get('progress') // 10))):
        #     self.history[key_id] = status_dict
        #     self._dump_history()
        # else:
        #     self.history[key_id] = status_dict

        # 实时更新
        self._dump_history()

        # # 调用回调, 更新UI状态列表
        # if self.callback:
        #     self.callback(self.get_history())

    # 更新任务列表文件
    def _dump_history(self):
        print("TaskManager: " + "====" * 20)
        with open(self.status_path, 'w+') as f:
            json.dump(self.history, f)

    def _create_anomaly(self, detect_dict, manager_id):
        self.target_task[manager_id] = AnomalyServer(detect_dict, manager_id)
        self.target_task[manager_id].start()
        print("TaskManager: start task ", manager_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def _create_template(self, train_dict):

        manager_id = train_dict.get('managerId')
        if self.history.get(manager_id):
            train_dict['taskIdList'] = self.history[manager_id].get(
                'aiTaskIdList', ["", ""])
        else:
            train_dict['taskIdList'] = ["", ""]
            self.history[train_dict.get('managerId')] = {
                "progress": 0,
                "state": TaskStatus.IDLE.name,
                'task_id': train_dict.get('managerId'),
                'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }

        self.target_task[manager_id] = TrainServer(train_dict)
        self.target_task[manager_id].start()
        print("TaskManager: start task ", manager_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    def _task_process(self, param_dict, task_type, task_id, is_stage_two=False):
        if task_id:
            manager_id = task_id
        else:
            manager_id = str(int(time.time()))
        print("TaskManager:", manager_id)
        self.task_type = task_type
        param_dict.update({"managerId": manager_id})

        if is_stage_two:
            print("TaskManager: Stage Two", manager_id)
            self.history[manager_id] = {
                "progress": 50,
                "state": TaskStatus.RUNNING.name,
                'task_id': manager_id,
                'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            self._create_anomaly(param_dict.get('anomalyDetectList'), manager_id)
        else:
            print("TaskManager: Stage One", manager_id)
            self._create_template(param_dict)

        self.history[manager_id].update({
            'type': task_type,
            'template_id': param_dict.get('templateId', param_dict.get('itemNo')),
            'param': param_dict
        })
        self.scheduler.add_job(self._running_status, 'interval', seconds=5, args=[
                                manager_id], id=manager_id)
        return True, manager_id

    # 筛选异常
    def create_anomaly_task(self, detect_dict, task_id=None):
        print("TaskManager: create anomaly detection task ", detect_dict, task_id)
        self.anomaly_dict.update(detect_dict)

        # if weights file exists, start stage Two
        is_stage_two = self.is_overleap
        if is_stage_two:
            weights_path_list = self.anomaly_dict.get('weightsPath', [])
            for weights_list in weights_path_list:
                for weights in weights_list:
                    if len(weights) >= 2 and not os.path.exists(weights[1]):
                        is_stage_two = False

        return self._task_process(self.anomaly_dict, TaskType.FILTER_ANOMALY.name, task_id, is_stage_two)

    # 生成模板
    def create_generate_template_task(self, train_dict, task_id=None):
        print("TaskManager: create generate template task ", train_dict, task_id)
        self.template_dict.update(train_dict)
        return self._task_process(self.template_dict, TaskType.GENERATE_TEMPLATE.name, task_id)

    # 停止任务
    def stop_manager_task(self, task_id):
        print("TaskManager: stop task ", task_id)
        task_list = self.scheduler.get_jobs()
        task_id_list = [task.id for task in task_list]
        task_process = False
        if task_id:
            if task_id in task_id_list:
                print("TaskManager: stop timer ", task_id)
                self.scheduler.remove_job(task_id)
            else:
                print("TaskManager: timer not found ", task_id)
            if self.target_task.get(task_id):
                # 关闭 task
                print("TaskManager: stop task ", task_id)
                self.target_task.get(task_id).close()
                if self.history[task_id]['state'] in [TaskStatus.RUNNING.name, TaskStatus.IDLE.name]:
                    self.history[task_id]['state'] = TaskStatus.ABORTED.name
                task_process = True
            else:
                print("TaskManager: task not found ", task_id)
        else:
            for ti in task_id_list:
                # 关闭定时器
                print("TaskManager: stop timer ", ti)
                self.scheduler.remove_job(ti)
                if self.target_task.get(ti):
                    # 关闭 task
                    print("TaskManager: stop task ", ti)
                    self.target_task.get(ti).close()
                    if self.history[ti]['state'] in [TaskStatus.RUNNING.name, TaskStatus.IDLE.name]:
                        self.history[ti]['state'] = TaskStatus.ABORTED.name
                task_process = True

        print("TaskManager: task process ", task_process)
        self._dump_history()
        return task_process

    # 获取任务状态
    def get_status(self, task_id):
        return self.history.get(task_id)

    # 获取历史任务状态
    def get_history(self):
        return list(self.history.values())

    # 设置config
    def set_config(self, config):
        self.config = config
