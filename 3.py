import fenbiFunction

# ExcFunc=fenbiFunction.FenBi() 

# url = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sh601388&p=16'      
# content = ExcFunc.getQQFbContent(url)  #获取腾讯股票实时分笔接口数据，单页数据每页70条   
# df=ExcFunc.dealQQFbContent(content) #处理腾讯股票实时分笔接口数据，转换为dataframe格式
# df["id"] = df["id"].astype("int")
# print(df)
# df=df[df['id']>1180]
# print(df)

# ExcFunc.testOntime()

for x in range(5):
    print(x)