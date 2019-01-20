select   a.name as 表名,max(b.rows) as 记录条数   from  
 sysobjects   a   ,sysindexes   b     
  where   a.id=b.id   and   a.xtype='U'   
group   by   a.name   
order by max(b.rows) desc

