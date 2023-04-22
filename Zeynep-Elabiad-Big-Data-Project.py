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
d_rate = pd.read_csv(url)


# In[3]:


url1='https://raw.githubusercontent.com/Zeynepelabiad/road-accidents/main/ITF_ROAD_ACCIDENTS_road-injury-crashes.csv'
d_injure = pd.read_csv(url1)


# In[4]:


url2='https://raw.githubusercontent.com/Zeynepelabiad/road-accidents/main/alcohol_consumption.csv'
alcohol=pd.read_csv(url2)


# In[5]:


url3='https://raw.githubusercontent.com/Zeynepelabiad/road-accidents/main/hdi_full.csv'
hdi=pd.read_csv(url3)


# In[6]:


d_rate=d_rate[(d_rate['SUBJECT'] == "DEATH") & (d_rate["MEASURE"]=="1000000HAB")]


# In[7]:


d_ratef=d_rate.loc[d_rate['LOCATION'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA']) & (d_rate['TIME']>=2010) & (d_rate['TIME']<=2020)]


# In[8]:


d_rate = d_rate.drop(['INDICATOR','SUBJECT','MEASURE','FREQUENCY','Flag Codes'], axis=1)


# In[9]:


d_rate.columns=['Code', 'Year','Death_rate']


# In[10]:


d_injure=d_injure.loc[d_injure['COUNTRY'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA']) & (d_injure['Year']>=2010) & (d_injure['Year']<=2020)]


# In[11]:


d_injure=d_injure.drop(['VARIABLE','Variable','YEAR','Unit Code','Unit','PowerCode Code','PowerCode','Reference Period Code',
            'PowerCode','Reference Period Code','Reference Period','Flag Codes','Flags'], axis=1)


# In[12]:


d_injure.columns=['Code','Country','Year','Death_injure']


# In[13]:


alcohol=alcohol.loc[alcohol['LOCATION'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA']) & (alcohol['TIME']>=2010) & (alcohol['TIME']<=2020)]


# In[14]:


alcohol = alcohol.drop(['INDICATOR','SUBJECT','MEASURE','FREQUENCY','Flag Codes'], axis=1)


# In[15]:


alcohol.columns=['Code', 'Year','Alcohol_cons']


# In[16]:


alcohol.to_csv('alcohol.csv',index=False)


# In[17]:


hdi=hdi.loc[hdi['iso3'].isin(['AUT','BEL','CAN','CHE','CZE','DEU','DNK','EST','FIN','FRA','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LVA','MEX','NOR','NZL','POR','PRT','SVK','SVN','SWE','TUR','USA'])]


# In[18]:


hdi=hdi[['iso3','country','hdi_2010','hdi_2011','hdi_2012','hdi_2013','hdi_2014','hdi_2015','hdi_2016','hdi_2017','hdi_2018','hdi_2019','hdi_2020']]


# In[19]:


hdi.columns = ['Code','Country', '2010', '2011', '2012', '2013','2014', '2015', '2016', '2017','2018', '2019','2020']


# In[20]:


hdi=hdi.drop(['Country'], axis=1)
hdi=hdi.set_index(['Code']).stack().reset_index()
hdi.columns=['Code', 'Year','Hdi']
hdi.Year = hdi['Year'].astype('int')


# In[21]:


hdi.head()


# In[22]:


d_injure.head()


# In[23]:


d_rate.head()


# In[24]:


alcohol.head()


# In[25]:


hdi.info()


# In[26]:


oecd_df1=pd.merge(d_injure, d_rate,how ='left', on =['Code','Year'])


# In[27]:


oecd_df1


# In[28]:


oecd_df2=pd.merge(oecd_df1, alcohol,how ='left', on =['Code','Year'])


# In[29]:


oecd_df2


# In[30]:


oecd_df=pd.merge(oecd_df2, hdi,how ='left', on =['Code','Year'])


# In[31]:


oecd_df.info()


# In[32]:


oecd_df


# import plotly.express as px
# import plotly.offline as pyo
# import plotly.graph_objs as go
# pyo.init_notebook_mode()
# fig = px.line(oecd_df, x="Year", y="Death_rate", color='Country',symbol="Country")
# plotly.offline.plot(fig, filename='death_rate1.html')
# fig.show()
# 

# import plotly.express as px
# fig=px.scatter(oecd_df, x="Death_rate", y="Death_injure", animation_frame="Year", animation_group="Year",
#            size="Death_rate", color="Country", hover_name="Country",size_max=55, range_x=[0,15], range_y=[0,3000000])
# plotly.offline.plot(fig, filename='death_rate2.html')
# 
# #fig.update_traces(textposition='middle center')
# fig.show()
# 

# fig = px.choropleth(oecd_df,
#                     locations="Code",
#                     color ="Death_rate",
#                     hover_name ="Death_rate", 
#                     color_continuous_scale = px.colors.sequential.Viridis,
#                     scope ="world",
#                     animation_frame ="Year",width=950, height=600)
# plotly.offline.plot(fig, filename='death_rate3.html')
# fig.show()

# fig = px.scatter_geo(oecd_df, locations="Code", color="Death_rate",
#                      hover_name="Year", size="Death_rate",
#                      projection="natural earth",
#                      animation_frame ="Year", width=950, height=600)
# plotly.offline.plot(fig, filename='death_rate4.html')
# 
# fig.show()

# In[33]:


sns.set(rc = {'figure.figsize':(15,10)})

ax=sns.barplot(x='Code', y='Death_rate', data=oecd_df)
#ax.bar_label(ax.containers[0])
plt.title('ROAD TRAFFIC ACCIDENTS DEATH RATE BY COUNTRY (OECD)')
plt.savefig('TRAFFIC_ACCIDENTS_DEATH_RATE.png')


# In[34]:


oecd_df.to_csv('oecd_df.csv',index=False)


# In[ ]:




