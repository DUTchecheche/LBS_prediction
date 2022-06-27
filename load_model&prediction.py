import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F
import numpy as np
import pandas as pd

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.l1 = torch.nn.Linear(33, 128)
        self.l2 = torch.nn.Linear(128, 64)
        self.l3 = torch.nn.Linear(64, 32)
        self.l4 = torch.nn.Linear(32, 2)

    def forward(self, x):
        x = x.view(-1,33)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        return self.l4(x)
# Redeclare the network structure corresponding to the model parameters to be loaded

class dockingDataset(Dataset):
    def __init__(self, filepath):
        readrow=np.arange(2,35)
        x = np.loadtxt(filepath, delimiter=',', usecols=readrow,skiprows=1,dtype=np.float32)
        self.len = x.shape[0]
        global mean
        global std
        if filepath == 'training_set.csv':
            mean=np.mean(x[:, :],0)
            x[:, :]-=mean
            std=np.std(x[:, :],0)
            x[:, :] /=std
        else:
            x[:, :] -= mean
            x[:, :] /= std
        self.x_data = torch.from_numpy(x[:,:])
    def __getitem__(self, index):
        return self.x_data[index]
    def __len__(self):
        return self.len
# define how to load dataset and standardize dataset

def test():
    list_probability=[]
    with torch.no_grad():
        for data in test_loader:
            output = model(data)
            tensor_probability=F.softmax(output.data,dim=1)
            probability=tensor_probability.data[:,-1]
            list_probability.extend(list(probability.numpy()))
        return list_probability
# obtain the model output for the test set

train_dataset = dockingDataset('training_set.csv')
train_loader = DataLoader(dataset=train_dataset, batch_size=512, shuffle=False)
test_dataset_path=input('Please enter the path and name of the input file (.csv):')
test_dataset = dockingDataset(test_dataset_path)
test_loader =DataLoader(dataset=test_dataset, batch_size=9,shuffle=False)
model=torch.load('ANN_model.pkl')
# load dataset and the ANN model, the training set is used to generate standardized parameters

df=pd.read_csv(test_dataset_path,usecols=[0])
df.insert(1,'probability',test())
df.to_csv('output_LBSprediction_results.csv',index=False)
# export the prediction results to a csv file

print('done')