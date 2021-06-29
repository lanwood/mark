import torch

print('GPU 是否可用', torch.cuda.is_available())
print('GPU 数量', torch.cuda.device_count())
print('GPU 名称', torch.cuda.get_device_name())


