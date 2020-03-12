#Processing dataset
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
from surprise import AlgoBase
train_path = '/home/estudiante/output/train_dataset.csv'
test_path = '/home/estudiante/output/test_dataset.csv'
#Read data sources
trains = pd.read_csv(train_path,header=0, sep=",",error_bad_lines=False)
tests = pd.read_csv(test_path,header=0, sep=",",error_bad_lines=False).sort_values(by=['userid'])[0:10]


reader = Reader( rating_scale = ( 1, 5 ))
#Create surprise dataset
train_dataset = Dataset.load_from_df(trains[ [ 'userid', 'itemid', 'rating' ] ], reader )
train_set, test_set=  train_test_split(train_dataset, test_size=.2)
def model(user_based,types,type_cal):
    # knn model implementation using cosine
    sim_options = {'name': types,
               'user_based': user_based}
    algo = KNNBasic(k=2, min_k=2, sim_options=sim_options)
    algo.fit(trainset=train_set)
    data = pd.DataFrame(tests.apply(lambda x: algo.predict(x[0],x[1]),axis=1))
    return data[0].apply(lambda x: str(x).split(","))
    #Se le pasa la matriz de utilidad al algoritmo 
    #test_predictions=(((pd.DataFrame(algo.predict(154,302)[0:10]).
    #                      rename(columns = {'uid': 'userid','r_ui':'rating','igid':'recommendation'})
    #                      [['userid','rating','recommendation']])))
    #test_predictions["recommendationtype"]=types
    #test_predictions["flag"] = user_based
    #test_predictions["model"] = type_cal
    #return data['userid'] #test_predictions#[['userid','rating','recommendationtype','model']]
    
#Modelos basado en usuarios
print(model(True,'cosine','user-user'))
#model(True,'pearson','user-user')

#Modelos basado en items
#model(False,'cosine')
#model(False,'pearson')
#model(False,'msd')