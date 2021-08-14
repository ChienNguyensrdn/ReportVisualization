import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
hr = pd.read_csv("Data/aug_train.csv")
hr.isna().sum()/len(hr)
hr_train = hr.fillna(0)
hr_train['relevent_experience'].unique()
hr_train['relevent_experience'] = hr_train['relevent_experience'].replace('Has relevent experience',1)
hr_train['relevent_experience'] = hr_train['relevent_experience'].replace('No relevent experience',0)
from sklearn.preprocessing import OrdinalEncoder
hr_train.company_size.unique()

edu_lv = [0,'Primary School','High School','Graduate','Masters','Phd']
uni = [0,'no_enrollment', 'Part time course', 'Full time course']
comp_size = [0,'<10','10/49','50-99','100-500','500-999','1000-4999','5000-9999','10000+']
enc = OrdinalEncoder(categories=[uni])
ordi1 = pd.DataFrame(enc.fit_transform(hr_train[["enrolled_university"]]))
#rename column for easy understanding
ordi1 = ordi1.rename(columns={0:"University"})
#Repeat ordinal encoding for education level and company_size
enc = OrdinalEncoder(categories=[edu_lv])
ordi2 = pd.DataFrame(enc.fit_transform(hr_train[["education_level"]]))
ordi2 = ordi2.rename(columns={0:"Education level"})
enc = OrdinalEncoder(categories=[comp_size])
ordi3 = pd.DataFrame(enc.fit_transform(hr_train[["company_size"]]))
ordi3 = ordi3.rename(columns={0:"Company size"})
hr_train= pd.get_dummies(hr_train, columns=['gender', 'major_discipline', 'company_type'])
#check any string in the columns
from pandas.api.types import is_numeric_dtype
is_numeric_dtype(hr_train['city_development_index'])
is_numeric_dtype(hr_train['training_hours'])
hr_train.experience.unique()
#Simply transform >20 to 21, of course it may be underestimated
#Simply transform <1 to 0.5 as the mean
hr_train['experience'] = hr_train['experience'].replace('>20',21)
hr_train['experience'] = hr_train['experience'].replace('<1',0.5)
hr_train.last_new_job.unique()
hr_train['last_new_job'] = hr_train['last_new_job'].replace('>4',5)
hr_train['last_new_job'] = hr_train['last_new_job'].replace('never',0)
len(hr_train.city.unique())
from sklearn.preprocessing import LabelEncoder
hr_train['city'] = LabelEncoder().fit_transform(hr_train['city'])
hr_train = hr_train.drop(columns=['enrollee_id',
                       'enrolled_university',
                       'education_level',
                       'company_size',
                      'target'])
# print(hr_train)
#concat all features
X = pd.concat([hr_train, ordi1, ordi2, ordi3], axis=1)
from sklearn.manifold import TSNE
#Dimension of the embedded space
X_embedded = TSNE(n_components=2).fit_transform(X)
df = pd.DataFrame()
df["y"] = hr['target']
df["dim-1"] = X_embedded[:,0]
df["dim-2"] = X_embedded[:,1]
sns.scatterplot(x="dim-1", y="dim-2", hue=df.y.tolist(),
                data=df).set(title="T-SNE projection") 