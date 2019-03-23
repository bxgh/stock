import easyquotation
import pandas as pd
import os

quotation = easyquotation.use('qq')
# data=quotation.stocks(['sh000001', 'sz000001'], prefix=True) 
data=quotation.get_stock_data
print(data)

# df=pd.DataFrame.from_dict(data,orient='index')

# # print(df)
# filename = 'c:\\ontimeKday\\realhq.hd5'        
# h5 = pd.HDFStore(filename,'w', complevel=4, complib='blosc')
# h5['data'] = df      
# h5.close()     