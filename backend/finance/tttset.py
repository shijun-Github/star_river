import akshare as ak
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 获取股票日线行情数据
stock_data = ak.stock_zh_a_daily(symbol="sz000001", start_date="2024-01-01", end_date="2025-02-11")
print(stock_data)
# 选择用于预测的特征（以日期为基础进行编码）
stock_data["date"] = pd.to_datetime(stock_data["date"])
stock_data["day_of_year"] = stock_data["date"].dt.dayofyear
X = stock_data[["day_of_year"]].values
y = stock_data["close"].values

# 训练线性回归模型
model = LinearRegression()
model.fit(X, y)

# 预测未来30天的股价
future_dates = pd.date_range(start="2025-02-11", periods=28)
print(future_dates)
# future_dates = pd.date_range(start="2025-01-11", periods=30, closed="right")
future_day_of_year = future_dates.dayofyear.values.reshape(-1, 1)
future_predictions = model.predict(future_day_of_year)

# 绘制股价预测图
plt.figure(figsize=(12, 6))
plt.plot(stock_data["date"], stock_data["close"], label="历史股价")
plt.plot(future_dates, future_predictions, label="预测股价", linestyle = "--")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title("Stock Price Prediction")
plt.legend()
plt.show()