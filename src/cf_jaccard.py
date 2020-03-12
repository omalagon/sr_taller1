# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
from surprise import AlgoBase
import random
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
from sklearn.metrics.pairwise import pairwise_distances

#Para garantizar reproducibilidad en resultados
seed = 10
random.seed(seed)
np.random.seed(seed)

#test_set=pd.read_csv('/content/drive/My Drive/Colab Notebooks/test_dataset.csv', sep = ',')
#train_set=pd.read_csv('/content/drive/My Drive/Colab Notebooks/train_dataset.csv', sep = ',')
test_set=pd.read_csv('/home/estudiante/output/test_dataset.csv', sep = ',')
train_set=pd.read_csv('/home/estudiante/output/train_dataset.csv', sep = ',')

def simi(df,user,significance=None):
  df = df.pivot(index='itemid',columns='userid',values='rating')
  list_append = []
  for column in df.columns:
    list_df = df[user].tolist()
    intersect = len(list(filter(lambda x: x is True,map(lambda x,y: x==y,list_df,df[column].tolist()))))
    len_list_df = len(df.loc[df[user].notna()])
    weight = intersect / len_list_df
    if significance is None:
      significance = 0
      if weight >= significance:
        len_j_f_list = len(df.loc[df[column].notna()]) 
        jaccard_sim = intersect / (len_list_df+len_j_f_list-intersect)
        list_append.append([jaccard_sim,column])
      else:
        pass
    else:
      if weight >= significance:
        len_j_f_list = len(df.loc[df[column].notna()]) 
        jaccard_sim = intersect / (len_list_df+len_j_f_list-intersect)
        list_append.append([jaccard_sim,column])
      else:
        pass
  df_returned = pd.DataFrame(list_append, columns=['sim','column']).sort_values(by='sim', ascending=False)
  return df_returned
  

def pred(df,simdf,user,k):
  df = df.pivot(index='itemid',columns='userid',values='rating')
  pred=[]
  num=[]
  denom=[]
  mean_r = df[user].mean()
  df = df.drop([user],axis=1)
  simdf_temp = simdf[1:k+1] 
  for x in range(0,len(simdf_temp)):
    index = simdf_temp.index[x]
    simili = simdf_temp['sim'][index]
    user_local = simdf_temp['column'][index]
    reducing = df[user_local]-df[user_local].mean()
    reducing = reducing.fillna(mean_r - df[user_local].mean()) 
    num.append(simili * (reducing))
    denom.append(simili)
  pred = mean_r + sum(num)/sum(denom)
  pred_df = pd.DataFrame(pred.values.round(0),columns=['pred'],index=pred.index)
  return pred_df

def rmse(df_train,df_pred,user):
  df_train=df_train.loc[df_train['itemid'].isin(df_pred.index.tolist()) & (df_train['userid'].isin([user]))]
  df_pred['itemid'] = df_pred.index 
  df_pred = df_pred.reset_index(drop=True)
  merged = pd.merge(df_train,df_pred,on='itemid',how='inner')
  return np.sqrt(((merged['pred'] - merged['rating']) ** 2).mean())

sim = simi(train_set,'user_000609')
predict = pred(test_set,sim,'user_000609',5)
rmse(train_set,predict,'user_000609')