import tensorflow as tf
print('GPU 是否可用:', tf.test.is_gpu_available())
print('GPU Logcal(虚拟):', tf.config.list_logical_devices('GPU'))
print('GPU Physical(实体):', tf.config.list_physical_devices('GPU'))

## 单GPU 模拟 多GPU
#gpus = tf.config.list_physical_devices('GPU')
#tf.config.set_logical_device_configuration(
#    gpus[0],
#    [tf.config.LogicalDeviceConfiguration(memory_limit=2048),
#     tf.config.LogicalDeviceConfiguration(memory_limit=2048)])


#设置训练所需的GPU的memory随需求而增长
##tf.config.experimental.set_memory_growth(gpus[0],True)
##os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"


# 设置使用的GPU
##import os
##os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# command = "nvidia-smi -q -d Memory"
# nvidia_list = os.popen(command).readlines()
# memory_list = [(nvidia_list[i+1], nvidia_list[i+2], nvidia_list[i+3]) for i, j in enumerate(nvidia_list) if "FB" in j]
# process_list = list(map(lambda x: x.split(" "), memory_list[0]))
# value_list = [i[2] for i in [list(filter(lambda x: x, y)) for y in process_list]]
# print('>>> GPU Memory: Total %s MiB | Used %s MiB | Free %s MiB' % (value_list[0], value_list[1], value_list[2]))

# import tensorflow as tf
# # # 显存动态分配 tf2 version, experimental版本可能后期会调整
# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)
#     # tf.config.experimental.set_virtual_device_configuration(
#     #     gpu,
#     #     [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])

# 显存动态分配 tf1 version
## config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
## config.gpu_options.per_process_gpu_memory_fraction = 0.3
## config.gpu_options.allow_growth=True
## tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))