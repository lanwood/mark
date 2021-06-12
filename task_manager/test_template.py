from task_manager import TaskManager as tm
import time

template_config = {
    'task_list_path': 'task_list.json'
}


task_config = {
    "type": 1,
    "frontBack": 2,
    "itemNo": "new002",
    "colorNo": "newno112",
    "colorArea": "black",
    "imageList": [r"/workspace/addp_workspace/dataset/train/images", r"/workspace/addp_workspace/dataset/train/images"],
    "labelList": [r"/workspace/addp_workspace/dataset/train/labels", r"/workspace/addp_workspace/dataset/train/labels"],
    "taskIdList": ["", ""],
    # "taskIdList": [r"1623227051820", r"1623227051391"],
    "weightsPath": [
        [
            [0, r"/workspace/addp_workspace/train_server/od_v100_c0.engine"],
            [3, r"/workspace/addp_workspace/train_server/od_2080ti_c0.engine"],
        ],
        [
            [0, r"/workspace/addp_workspace/train_server/od_v100_c1.engine"],
            [3, r"/workspace/addp_workspace/train_server/od_2080ti_c1.engine"],
        ]
    ]
}

if __name__ == '__main__':
    print("labelImg: TaskManager init")
    task = tm(template_config)
    task.start()


    print("labelImg: create generate template task")
    task.create_generate_template_task(task_config)


    print("labelImg: start status polling")
    while True:
        status = task.get_status() # 获取当前任务状态
        print("labelImg: current ", status)
        history = task.get_history() # 获取任务列表状态
        print("labelImg: history ", history)
        if status.get('state') == 'FINISHED':
            break
        time.sleep(12)
