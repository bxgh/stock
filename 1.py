from apscheduler.schedulers.blocking import BlockingScheduler
import baseFunction,stockFunction
import time 
# 将要被定时执行的任务
def task_kdayClose():  #日线收盘任务，s:收盘日期
    
    # mskday.kday_close(s)
    mskday.test()

def tick() :
    t = time.localtime(time.time())               
    StrIMSt = time.strftime("%H:%M:%S", t) 
    print(StrIMSt)
 
if __name__ == '__main__':
    # 初始化调度器      
    scheduler = BlockingScheduler()

    t = time.localtime(time.time())  
    StrYMDt = time.strftime("%Y-%m-%d", t)         
    StrIMSt = time.strftime("%H:%M:%S", t) 
    today=time.strftime("%Y%m%d", t)

    mskday = stockFunction.MSSQL(host="192.168.151.213", user="toshare1", pwd="toshare1", db="kday_qfq",myOrms="mysql") 
 
    # 添加任务作业，args()中最后一个参数后面要有一个逗号，本任务设置在每天凌晨1:00:00执行
    # scheduler.add_job(task_kdayClose, 'cron', hour='10', minute='10', second='30', args=(today,))
    scheduler.add_job(task_kdayClose, 'interval', minutes=1, start_date='2019-01-15 11:00:01' , end_date='2019-01-15 14:00:10')


    # scheduler.add_job(tick, 'interval', seconds=3)
    # scheduler.add_job(task, 'cron', args=(today,))
 
    # 启动调度器，到点task就会被执行啦
    scheduler.start()
 
    print("world")  # 此处world将不会被打印出来，因为被阻塞了
