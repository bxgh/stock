/****** Object:  StoredProcedure [dbo].[createTableFb]    Script Date: 2019-01-19 17:35:48 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create  procedure [dbo].[createTableFbQx]   
(@tableKind  char(10) ,@tsCode char(10)) 
 as
begin
	declare @tableName char(25)
	set @tableName=ltrim(rtrim(@tsCode)) 
	

	if not exists (select * from sysobjects where name=@tableName)
	begin
        declare @CreateSQL nvarchar(MAX);
        set @CreateSQL = 
        'Create table [dbo].['+ltrim(rtrim(@tableName))+'](  		
		[ts_code] [char](8) NOT NULL,
		[Time] [datetime] NOT NULL,
		[Price] [decimal](8, 2) NULL,
		[Volume] [decimal](8, 2) NULL,
		[Tradeid] [int] NULL,
		[Direction] [char](1) null,
		[SaleOrderId] [int] NULL,
		[BuyOrderId] [int] NULL,
	    ) ON [PRIMARY]
	    '        
        EXEC(@CreateSQL)		
    end
end



