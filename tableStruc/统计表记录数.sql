select   a.name as ����,max(b.rows) as ��¼����   from  
 sysobjects   a   ,sysindexes   b     
  where   a.id=b.id   and   a.xtype='U'   
group   by   a.name   
order by max(b.rows) desc

