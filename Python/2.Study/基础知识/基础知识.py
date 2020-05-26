# 数据分析包
import pandas as pd 
# 数据绘图可视化操作
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif']=['SimHei']
# 设置正常显示字符
plt.rcParams['axes.unicode_minus']=False

# 设置绘画风格
plt.style.use('fivethirtyeight')

# 调取接口获取数据
current = pd.read_json('https://api.coinmarketcap.com/v1/ticker/')
print(current.head())
