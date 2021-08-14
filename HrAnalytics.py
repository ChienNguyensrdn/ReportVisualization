import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
hr = pd.read_csv("Data/aug_train.csv")
hr.head(5)
print(hr.head(5))

#=======================================================
# Features
# enrollee_id : Unique ID for enrollee
# city: City code
# citydevelopmentindex: Developement index of the city (scaled)
# gender: Gender of enrolee
# relevent_experience: Relevent experience of enrolee
# enrolled_university: Type of University course enrolled if any
# education_level: Education level of enrolee
# major_discipline :Education major discipline of enrolee
# experience: Employee total experience in years
# company_size: No of employees in current employer's company
# company_type : Type of current employer
# lastnewjob: Difference in years between previous job and current job
# training_hours: training hours completed
# target: 0 – Not looking for job change, 1 – Looking for a job change
#=======================================================
# How many candidate seeking a job change?
# 0 – Not looking for job change,
# 1 – Looking for a job change
target_count = hr['target'].value_counts()
sns.barplot(target_count.index , target_count.values)
plt.ylabel('Number of candidate')
plt.xlabel('target')
#Summary: No of not seeking a job change is far more than those seeking a job change, nearly 3 times.
# Male more likely to leave?
# Firstly, let's find the ratio of male and female.
#  Most job-seekers appear to be male in terms of absolute no.
# However, if look at the pivot table, the mean value (ie ratio of job-seeker) of 
# target between male and female is similar.
# This is because there are far more male data scientist 
# than female and of course more male job seeker will be observed, 
# giving us a illusion that male employee tend to leave.
sns.countplot(x="gender", hue="target", data=hr)
plt.ylabel('Number of candidate')

hrPivot=hr.pivot_table(index=['gender'], values='target',aggfunc=['mean', 'count'])
print(hrPivot)
# How the environment shape their tendency?

sns.kdeplot(hr.loc[(hr["target"]==0), "city_development_index"], label="Non-Job Seeker")
sns.kdeplot(hr.loc[(hr["target"]==1), "city_development_index"], label="Job Seeker")

# Relationship between experience and training hours
x=hr['experience'].str.strip('><').fillna(0).astype(int)
y=hr['training_hours']
plt.scatter(x, y, marker='o')
plt.ylabel('Training hours')
plt.xlabel('Experience (years)')
# Employee with more training hours more likely to leave?
sns.boxenplot(y='training_hours', x='target', data=hr)

import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(6,3))
gs = fig.add_gridspec(1, 2)

ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[0,1])

type_major_0 = hr.loc[hr['target']==0].pivot_table(index='company_type', columns='major_discipline', values='target', aggfunc='count')
type_major_1 = hr.loc[hr['target']==1].pivot_table(index='company_type', columns='major_discipline', values='target', aggfunc='count')


heat_0 = sns.heatmap(ax=ax0, data=type_major_0, cmap="OrRd", cbar=False)
ax0.text(0,-0.5,"Non-job seeker",fontsize=20,fontweight='bold')
heat_1 = sns.heatmap(ax=ax1, data=type_major_1,  yticklabels=False, cmap="OrRd", cbar=False)
ax1.text(1,-0.5,"Job seeker",fontsize=20,fontweight='bold')
ax1.set_ylabel('')  

# No of changing company before
# It's obvious that employee who haven't changed company or only once have high likelihood to seek a new job currently.
total = hr.groupby(['target'])['enrollee_id'].count().reset_index(drop=True)

not_seek = hr.loc[hr['target']==0].groupby(['target','last_new_job'])['enrollee_id'].count().reset_index()
seek = hr.loc[hr['target']==1].groupby(['target','last_new_job'])['enrollee_id'].count().reset_index()

not_seek['percentage'] = not_seek['enrollee_id'].div(total.iloc[0])*100
seek['percentage'] = seek['enrollee_id'].div(total.iloc[1])*100

ax = plt.barh(not_seek.last_new_job, not_seek.percentage, label='Non-job seeker')
ax = plt.barh(seek.last_new_job, seek.percentage, height=0.3, label='Job seeker')

plt.legend()
