#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly
warnings.filterwarnings('ignore')


# In[2]:


url = 'https://raw.githubusercontent.com/Zeynepelabiad/road-accidents/main/oecd_full.csv'
df = pd.read_csv(url)
url1='https://raw.githubusercontent.com/Zeynepelabiad/road-accidents/main/ITF_ROAD_ACCIDENTS_road-injury-crashes.csv'
df1 = pd.read_csv(url1)


# In[3]:


df=df[(df['SUBJECT'] == "DEATH") & (df["MEASURE"]=="1000000HAB")]


# In[4]:


df=df.loc[df['LOCATION'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA']) & (df['TIME']>=2010) & (df['TIME']<=2020)]


# In[5]:


df1=df1.loc[df1['COUNTRY'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA']) & (df1['Year']>=2010) & (df1['Year']<=2020)]


# In[6]:


df = df.drop(['INDICATOR','SUBJECT','MEASURE','FREQUENCY','Flag Codes'], axis=1)


# In[7]:


df.columns=['Code', 'Year','Death_rate']


# In[8]:


df1=df1.drop(['VARIABLE','Variable','YEAR','Unit Code','Unit','PowerCode Code','PowerCode','Reference Period Code',
            'PowerCode','Reference Period Code','Reference Period','Flag Codes','Flags'], axis=1)


# In[9]:


df1.columns=['Code','Country','Year','Death_injure']


# In[10]:


oecd_df=pd.merge(df, df1,how ='left', on =['Code','Year'])


# In[11]:


print(df.head(5))


# In[12]:


oecd_df.info()


# In[13]:


oecd_df


# In[14]:


import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode()
fig = px.line(oecd_df, x="Year", y="Death_rate", color='Country',symbol="Country")
plotly.offline.plot(fig, filename='death_rate1.html')
fig.show()


# In[15]:


import plotly.express as px
fig=px.scatter(oecd_df, x="Death_rate", y="Death_injure", animation_frame="Year", animation_group="Year",
           size="Death_rate", color="Country", hover_name="Country",size_max=55, range_x=[0,15], range_y=[0,3000000])
plotly.offline.plot(fig, filename='death_rate2.html')

#fig.update_traces(textposition='middle center')
fig.show()


# In[16]:


fig = px.choropleth(oecd_df,
                    locations="Code",
                    color ="Death_rate",
                    hover_name ="Death_rate", 
                    color_continuous_scale = px.colors.sequential.Viridis,
                    scope ="world",
                    animation_frame ="Year",width=950, height=600)
plotly.offline.plot(fig, filename='death_rate3.html')
fig.show()


# In[17]:


fig = px.scatter_geo(oecd_df, locations="Code", color="Death_rate",
                     hover_name="Year", size="Death_rate",
                     projection="natural earth",
                     animation_frame ="Year", width=950, height=600)
plotly.offline.plot(fig, filename='death_rate4.html')

fig.show()


# In[18]:


sns.set(rc = {'figure.figsize':(15,10)})

ax=sns.barplot(x='Code', y='Death_rate', data=oecd_df)
ax.bar_label(ax.containers[0])
plt.title('ROAD TRAFFIC ACCIDENTS DEATH RATE BY COUNTRY (OECD)')
plt.savefig('TRAFFIC_ACCIDENTS_DEATH_RATE.png')


# In[ ]:




