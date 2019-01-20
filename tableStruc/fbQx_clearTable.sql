create procedure [dbo].[clearTable]  
 as
begin
    declare @tableName char(16)
	declare @ts_code char(9)	
	declare @CreateSQL nvarchar(MAX);
    DECLARE kday_Cursor CURSOR FOR	
	-- select ts_code from allKday_closed where trade_date=@closeDate
	 select name as ts_code from sysobjects where   xtype='U'
	OPEN kday_Cursor
	FETCH NEXT FROM kday_Cursor into @ts_code

	WHILE @@FETCH_STATUS = 0
		BEGIN	
		set @tableName=@ts_code		
		set @CreateSQL='truncate table  ' +@tableName 
		exec(@CreateSQL)
		--print @CreateSQL
		FETCH NEXT FROM kday_Cursor into @ts_code
		END
	CLOSE kday_Cursor
	DEALLOCATE kday_Cursor
end
