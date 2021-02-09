# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:28:26 2021

@author: victor-h-flores
"""

# Timestamp indicates prof needs sleep

# Script to run mean-variance optimization for portfolio in bt.py

# Import the bt package so we can use the backtesting functions
import bt

# Intead of using a date to get the data in every call, I set up a variable here
# It is usually better to use variables so you can change things later in ONE place
# rather than many places. 
beginning = '2017-01-01'
endate = '2019-12-31'
# Import data
equity_list = ['MCD','BKNG','LVS','GRMN','AZO','DPZ','HLT','HAS','NKE','ETSY','LEG','TJX','APTV','GPS','PVH','CMG','EXPE','BBY','TPR','DG','AAP','VFC','CHIQ']
data = bt.get(equity_list, start=beginning, end=endate)
data.head()
benchmark = ['RCD']
data2 = bt.get(benchmark, start=beginning, end=endate)
# We will need the risk-free rate to get correct Sharpe Ratios 
riskfree =  bt.get('^IRX', start=beginning)
# Take the average of the risk free rate over entire time period
riskfree_rate = float(riskfree.mean()) / 100
# Print out the risk free rate to make sure it looks good
print(riskfree_rate)

s_mark = bt.Strategy('Bounce Portfolio', 
                       [bt.algos.RunEveryNPeriods(9, 3),
                       bt.algos.SelectAll(),
                       bt.algos.WeighMeanVar(),
                       bt.algos.Rebalance()])

#Benchmark ETF Invesco Consumer Discretionary

#'Invesco S&P500 Equal Weighted Consumer Discretionary ETF',
s_mark2 = bt.Strategy('Invesco S&P500 Equal Weighted Consumer Discretionary ETF',
                       [bt.algos.RunEveryNPeriods(9, 3),
                       bt.algos.SelectAll(),
                       bt.algos.WeighMeanVar(),
                       bt.algos.Rebalance()])


b_mark = bt.Backtest(s_mark, data)
b_mark2 = bt.Backtest(s_mark2, data2)


result = bt.run(b_mark,b_mark2)
#result = bt.run(b_mark, b_inv, b_random, b_best, b_sp500)
result.set_riskfree_rate(riskfree_rate)
result.plot()

# Show some performance metrics
result.display()