#library load
import pandas as pd
import numpy as np
import tarfile
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
########## Pre-processing ##########
path='/home/estudiante/data/lastfm-dataset-1K.tar.gz'
data_title={0:"userid",1:"timestamp",
            2:"musicbrainz-artist-id",3:"artist-name",
            4:"musicbrainz-track-id",5:"track-name"}

#decompressing tsv files using tarfile library
def extractData(path,pos):
    with tarfile.open(path, "r:*") as tar:
        csv_path = tar.getnames()[pos]
        df = pd.read_csv(tar.extractfile(csv_path), 
                         header=0, sep="\t",error_bad_lines=False)
    return df

#reference dataframe- clean process
ref = extractData(path,3)
ref = (((pd.DataFrame(np.vstack([ref.columns, ref])).rename(columns=data_title)
         [['userid','timestamp','artist-name','track-name']].
         drop_duplicates()[['userid','timestamp','track-name']].
         dropna().reset_index())))

#first criteria - song frecuency in data source
ref1 =(((ref[['userid','track-name','index']].
         groupby(['userid','track-name']).
         agg({'count'}))))
ref1.columns = ref1.columns.get_level_values(0)
ref1 = (((ref1.reset_index().
          set_index('userid').
          merge(pd.DataFrame(ref1.reset_index().
                             groupby('userid')['index'].max()),
                left_index=True,right_index=True,how='inner'))))
ref1['porc']=ref1.index_x/ref1.index_y
ref1['calif']=ref1['porc'].apply(lambda x: 1 if x<0.20 else 2 
                                 if x>=0.20 and x <0.40 else 3
                                 if x>=0.40 and x <0.60 else 4
                                 if x>=0.60 and x <0.80 else 5)

#second criteria - use frecuency by song and date
ref2 = ref[['userid','timestamp','track-name']]
ref2['time_use']=ref2.timestamp.str.slice(start=0, stop=10, step=1)
ref2 = (((ref2.groupby(['userid','track-name','time_use']).
            agg({'count'}).reset_index()
          [['userid','track-name','time_use']].
          groupby(['userid','track-name']).agg({'count'}).
          reset_index().set_index('userid','track-name'))))
ref2.columns = ref2.columns.get_level_values(0)
ref1= ref1[['track-name','index_x','calif']].set_index('track-name', append=True).merge(
    ref2.set_index('track-name', append=True), left_index=True, right_index=True, how='inner')
ref1['frec'] = ref1.index_x/ref1.time_use
ref2 = (((ref1.reset_index().groupby(['userid'])['frec'].agg({'max','min'}).
          rename(columns={'max':'max_value','min':'min_value'}))))
ref2['dif']=(ref2.max_value-ref2.min_value)
ref1 = (((ref1.reset_index().set_index('userid').
          merge(ref2,left_index=True,right_index=True,how='inner')
         [['track-name','calif','frec','min_value','dif']])))
ref1['calif_2']= ((ref1.frec-ref1.min_value)/ref1.dif).apply(lambda x: 1 if x<0.20 else 2 
                                                             if x>=0.20 and x <0.40 else 3
                                                             if x>=0.40 and x <0.60 else 4
                                                             if x>=0.60 and x <0.80 else 5)
ref1 = ref1[['track-name','calif','calif_2']]

#weighting average using the first and second criteria
ref1['rating'] = (((ref1.calif)*0.4)+((ref1.calif_2)*0.6)).round()
ref1 = (((ref1.reset_index().rename(columns={'track-name':'itemid'})
          [['userid','itemid','rating']])))

#split dataFrame- train and test dataset
train, test = train_test_split(ref1, test_size=0.2)
#export dataset
train.to_csv('/home/estudiante/output/train_dataset.csv', index=False)
test.to_csv('/home/estudiante/output/test_dataset.csv', index=False)