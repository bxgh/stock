import pandas as pd

# def getPreClose(closeday,kdaydf):

df=kdaydf[kdaydf['trade_date'<=closeday]]

