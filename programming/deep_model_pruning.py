from torchvision.models import resnet18
from torchvision import transforms
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np


class PruningModel(torch.nn.Module):
    r"""深度学习模型剪枝优化原理：
    目标： 减少需要拟合的参数个数，从而在特定的数据量下，提高模型表现

    无用的权重大多分布比较平均，或权重数值很小，所以可以使用std检测和percentile来决定训练时是否保留这些权重

    当获取这些无需训练的权重，设置这些参数权重为0，权重更新时，这些值的梯度也设置为0，从而达到该权重不更新的目的

    """
    def prune_by_std(self, s=1e-1):
        pass

    def prune_by_percentile(self, q=5.0, **kwargs):
        pass


def visualize_model(model, input, f_output):
    width = 8
    flg, ax = plt.subplots(f_output[0].shape[0] // width, width, figsize=(20, 20))

    for i in range(f_output[0].shape[0]):
        ix = np.unravel_index(i, ax.shape)
        plt.sca(ax[ix])
        ax[ix].title.set_text('filter-{}'.format(i))
        plt.imshow(f_output.detach()[0][i])
    # plt.imshow(f_output.detach()[0][0])
    plt.show()


if __name__ == '__main__':
    print("begin")

    img = cv2.imread('sample.jpg')

    transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    img = transforms(img)

    print("origin img:", img.shape)
    img = img.unsqueeze(0)
    print("unsqueeze img:", img.shape)

    resnet = resnet18(pretrained=True)

    conv_model = [m for _, m in resnet.named_modules() if isinstance(m, torch.nn.Conv2d)]
    for conv in conv_model:
        conv.register_forward_hook(visualize_model)

    first_layer = conv_model[0]
    f_output = first_layer(img)

    print("first layer:", f_output.shape)

    # visualize_model(f_output)

    with torch.no_grad():
        output = resnet(img)

    print("resnet img:", output.shape)
