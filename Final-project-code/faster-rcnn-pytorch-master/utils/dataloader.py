from random import shuffle
import numpy as np
import torch
import torch.nn as nn
import math
import cv2
import torch.nn.functional as F
from PIL import Image
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

class FRCNNDataset(Dataset):
    def __init__(self,train_lines,shape=[600,600],batch_size=1):
        self.train_lines = train_lines
        self.train_batches = len(train_lines)
        self.shape = shape
        self.batch_size = batch_size

    def __len__(self):
        return self.train_batches

    def rand(self, a=0, b=1):
        return np.random.rand() * (b - a) + a
        
    def get_random_data(self, annotation_line, jitter=.3, hue=.1, sat=1.5, val=1.5):
        '''r实时数据增强的随机预处理'''
        line = annotation_line.split()
        image = Image.open(line[0])
        iw, ih = image.size
        h,w = self.shape
                            #######################这里我改过############################
        box = np.array([np.array(list(map(int, list(map(float, box.split(',')))))) for box in line[1:]])
        # box = np.array([np.array(list(map(float,box.split(',')))) for box in line[1:]])

        # resize image
        new_ar = w/h * self.rand(1-jitter,1+jitter)/self.rand(1-jitter,1+jitter)
        scale = self.rand(.5, 1.5)
        if new_ar < 1:
            nh = int(scale*h)
            nw = int(nh*new_ar)
        else:
            nw = int(scale*w)
            nh = int(nw/new_ar)
        image = image.resize((nw,nh), Image.BICUBIC)

        # place image
        dx = int(self.rand(0, w-nw))
        dy = int(self.rand(0, h-nh))
        new_image = Image.new('RGB', (w,h), (128,128,128))
        new_image.paste(image, (dx, dy))
        image = new_image

        # flip image or not
        flip = self.rand()<.5
        if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # distort image
        hue = self.rand(-hue, hue)
        sat = self.rand(1, sat) if self.rand()<.5 else 1/self.rand(1, sat)
        val = self.rand(1, val) if self.rand()<.5 else 1/self.rand(1, val)
        x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
        x[..., 0] += hue*360
        x[..., 0][x[..., 0]>1] -= 1
        x[..., 0][x[..., 0]<0] += 1
        x[..., 1] *= sat
        x[..., 2] *= val
        x[x[:,:, 0]>360, 0] = 360
        x[:, :, 1:][x[:, :, 1:]>1] = 1
        x[x<0] = 0
        image_data = cv2.cvtColor(x, cv2.COLOR_HSV2RGB)*255 # numpy array, 0 to 1

        # correct boxes
        box_data = np.zeros((len(box),5))
        if len(box)>0:
            np.random.shuffle(box)
            box[:, [0,2]] = box[:, [0,2]]*nw/iw + dx
            box[:, [1,3]] = box[:, [1,3]]*nh/ih + dy
            if flip: box[:, [0,2]] = w - box[:, [2,0]]
            box[:, 0:2][box[:, 0:2]<0] = 0
            box[:, 2][box[:, 2]>w] = w
            box[:, 3][box[:, 3]>h] = h
            box_w = box[:, 2] - box[:, 0]
            box_h = box[:, 3] - box[:, 1]
            box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box
            box_data = np.zeros((len(box),5))
            box_data[:len(box)] = box
        if len(box) == 0:
            return image_data, []

        if (box_data[:,:4]>0).any():
            return image_data, box_data
        else:
            return image_data, []


    def __getitem__(self, index):
        if index == 0:
            shuffle(self.train_lines)
        lines = self.train_lines
        n = self.train_batches
        while True:
            img,y=self.get_random_data(lines[index])
            if len(y)==0:
                index = (index + 1) % n
                continue
            box = np.array(y[:,:4],dtype=np.float32)
            box[:,0] = y[:,0]
            box[:,1] = y[:,1]
            box[:,2] = y[:,2]
            box[:,3] = y[:,3]
            
            box_widths = box[:,2] - box[:,0]
            box_heights = box[:,3] - box[:,1]
            if (box_heights<=0).any() or (box_widths<=0).any():
                index = (index + 1) % n
                continue
            break
            
        label = y[:,-1]
        img = np.transpose(img / 255.0, [2,0,1])
        return img, box, label

# DataLoader中collate_fn使用
def frcnn_dataset_collate(batch):
    images = []
    bboxes = []
    labels = []
    for img, box, label in batch:
        images.append(img)
        bboxes.append(box)
        labels.append(label)
    images = np.array(images)
    bboxes = np.array(bboxes)
    labels = np.array(labels)
    return images, bboxes, labels

