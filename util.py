import matplotlib.pyplot as plt
from torchvision.utils import make_grid
from baseline import BaselineNet
from cvae_model import CVAE
from mnist import *


def imshow(inp, title=None):
    inp = inp.numpy().transpose((1, 2, 0))
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


def visualize():
    model = BaselineNet(500, 500)
    model.load_state_dict(torch.load('../data/models/baseline_net_q1.pth'))
    model.eval()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    datasets, dataloaders, dataset_sizes = get_data(
        num_quadrant_inputs=1,
        batch_size=32
    )
    num_images = 10
    batch = next(iter(dataloaders['val']))
    inputs = batch['input'].to(device)
    outputs = batch['output'].to(device)
    originals = batch['original'].to(device)

    with torch.no_grad():
        preds = model(inputs).view(outputs.shape)

    # Predictions are only made in the pixels not masked. This completes
    # the input quadrant with the prediction for the missing quadrants, for
    # visualization purpose
    preds[outputs == -1] = inputs[outputs == -1]

    originals_slice = originals[:num_images]
    preds_slice = preds.unsqueeze(1)[:num_images]
    grid_tensor = torch.cat([originals_slice, preds_slice], dim=0)
    grid_tensor = make_grid(grid_tensor, nrow=num_images, padding=0)

    for i in range(num_images - 1):
        grid_tensor[:, :, (i + 1) * 28] = 0.2
    grid_tensor[:, 28, :] = 0.2

    imshow(grid_tensor)


if __name__ == '__main__':
    visualize()
    # pre_trained_baseline_net = BaselineNet(500, 500)
    # pre_trained_baseline_net.load_state_dict(
    #     torch.load('../data/models/baseline_net_q1.pth'))
    # pre_trained_baseline_net.eval()
    #
    # model = CVAE(200, 500, 500, pre_trained_baseline_net)
    # model.load('../data/models/cvae_net_q1')
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # datasets, dataloaders, dataset_sizes = get_data(
    #     num_quadrant_inputs=1,
    #     batch_size=32
    # )
    #
    # batch = next(iter(dataloaders['val']))
    # inputs = batch['input'].to(device)
    # outputs = batch['output'].to(device)
    # originals = batch['original'].to(device)
    #
    # preds = model.predict(inputs, num_samples=10)
    # print(preds)










