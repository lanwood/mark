from task_manager import TaskManager as tm
import time

template_config = {
    'workspace': 'task_history.json'
}


task_config = {
    "anomalyDetectList": [
        {
            'rawImage': "/workspace/huayan_nfs/localhost/YS50083-10_BD/ad_rawimages/part1_C0_test/",
            'anomalyImage': "/workspace/backbone_check/dfr_od/tmp/test/anomaly_py/",
            'gpuInfos': [{"id": 1, "engine": "/workspace/backbone_check/dfr_od/anomaly_detect/build/AutoEncoder_fp16_b16_20210609.engine", "batch_size": 8},
                         {"id": 2, "engine": "/workspace/backbone_check/dfr_od/anomaly_detect/build/AutoEncoder_fp16_b16_20210609.engine", "batch_size": 8}]
        },
        # {
        #     'rawImage': "D:/data/YS56070-8_L_2/images/raw/C1",
        #     'anomalyImage': "D:/data/YS56070-8_L_2/images/anomaly/C1",
        #     'gpuInfos': [{"id": 2, "engine": "engine2", "batch_size": 4},
        #                  {"id": 3, "engine": "engine2", "batch_size": 4}]
        # }
    ],


    "type": 0,
    "frontBack": 2,
    "itemNo": "new002",
    "colorNo": "newno112",
    "colorArea": "black",
    "imageList": [r"/workspace/addp_workspace/dataset/train/images", r"/workspace/addp_workspace/dataset/train/images"],
    "labelList": [r"/workspace/addp_workspace/dataset/train/labels", r"/workspace/addp_workspace/dataset/train/labels"],

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

task_config_od = {
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

    print("labelImg: create anomaly task")
    task.create_anomaly_task(task_config)

    print("labelImg: start status polling")
    while True:
        status_ae = task.get_status() # 获取当前任务状态
        print("labelImg: current ae", status_ae)
        # history = task.get_history() # 获取任务列表状态
        # print("labelImg: history ", history)
        if status_ae.get('state') == 'FINISHED':
            print("labelImg: anomaly task success")
            break
        time.sleep(12)

    # # 生成 od 模板
    # task.create_generate_template_task(task_config_od)
    # print("labelImg: start od status polling")
    # while True:
    #     status_od = task.get_status() # 获取当前任务状态
    #     print("labelImg: current od", status_od)
    #     # history = task.get_history() # 获取任务列表状态
    #     # print("labelImg: history ", history)
    #     if status_od.get('state') == 'FINISHED':
    #         print("labelImg: generate_od_template task success")
    #         break
    #     time.sleep(12)
