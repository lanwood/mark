from torchvision.models import resnet18
from torchvision import transforms
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    print("begin")
    
    img = cv2.imread('sample.jpg')

    transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])

    img = transforms(img)

    print("origin img:", img.shape)
    img = img.unsqueeze(0)
    print("unsqueeze img:", img.shape)

    resnet = resnet18(pretrained=True)
    with torch.no_grad():
        output = resnet(img)

    print("resnet img:", output.shape)

    conv_model = [m for _, m in resnet.named_modules() if isinstance(m, torch.nn.Conv2d)]

    first_layer = conv_model[0]
    f_output = first_layer(img)


    print("first layer:", f_output.shape)

    width = 8
    flg, ax = plt.subplots(f_output[0].shape[0] // width, width, figsize=(20, 20))

    for i in range(f_output[0].shape[0]):
        ix = np.unravel_index(i, ax.shape)
        plt.sca(ax[ix])
        ax[ix].title.set_text('filter-{}'.format(i))
        plt.imshow(f_output.detach()[0][i])

    # plt.imshow(f_output.detach()[0][0])
    plt.show()