import concurrent.futures
import pandas as pd
import matplotlib
from pathlib import Path
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st



def get_data(url):
    res = requests.get(url, headers=header)
    return pd.read_html(res.text, header=0, encoding='euc-kr')[0]

st.multiselect(’choose a name’,[name])

name = '휴켐스'
url = get_url(name, df_code)  # url 가져오기
df_price_item = pd.DataFrame()

def fetch_data(page):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    return get_data(pg_url)

# 멀티스레딩을 사용하여 데이터 가져오기
with concurrent.futures.ThreadPoolExecutor() as executor:
    pages = range(59, 85)
    results = executor.map(fetch_data, pages)

# 가져온 데이터 병합
for result in results:
    df_price_item = pd.concat([df_price_item, result], ignore_index=True)

# 이후 작업을 계속 진행
df_price_item = df_price_item.dropna()


pd.set_option('display.max_rows',500)


for i in range(1, 31):
    df_price_item.drop(df_price_item[df_price_item['날짜'] == "2019.12.{0:0>2}".format(i)].index, inplace=True)
for i in range(5, 31):
    df_price_item.drop(df_price_item[df_price_item['날짜'] == '2021.01.{0:0>2}'.format(i)].index, inplace=True)
df_price_item = df_price_item.sort_index(ascending=False) #sort
df_price_item = df_price_item.reset_index(drop=True) # 초기화
print(df_price_item)


font_location = 'NanumBarunGothicLight.ttf'
font_name = fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)

df_2021 = pd.read_csv('2021.csv')
df_2020 = pd.read_csv('2020.csv')

#normalization
df_kospi_price['체결가_normalization'] = df_kospi_price['체결가']/abs(df_kospi_price['체결가'].max())
df_price_item['종가_normalization'] = df_price_item['종가']/abs(df_price_item['종가'].max())

#graph
plt.figure(figsize=(10,4))
plt.plot(df_kospi_price['날짜'], df_kospi_price['체결가_normalization'],color='dodgerblue')
plt.xlabel('날짜')
plt.ylabel('종가')
plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=False,
    labelbottom=False)

plt.plot(df_price_item['날짜'], df_price_item['종가_normalization'],color='orange')
plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=False,
    labelbottom=False)

variable_x = mpatches.Patch(color='dodgerblue',label='KOSPI')
variable_y = mpatches.Patch(color='orange',label=name)
plt.legend(handles=[variable_x, variable_y],loc='lower left')

plt.show()
