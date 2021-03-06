
GO
/****** Object:  StoredProcedure [dbo].[createTable]    Script Date: 2018-12-30 19:31:48 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
alter  procedure [dbo].[createTableFb]
(@tableKind  char(10) ,@tsCode char(10)) 
 as
begin
	declare @tableName char(25)
	set @tableName=ltrim(rtrim(@tableKind))+ltrim(rtrim(@tsCode)) 
	

	if not exists (select * from sysobjects where name=@tableName)
	begin
        declare @CreateSQL nvarchar(MAX);
        set @CreateSQL = 
        'Create table [dbo].['+ltrim(rtrim(@tableName))+'](  
		[id] [int] NOT NULL,
		[ts_code] [char](8) NOT NULL,
		[trade_time] [datetime] NOT NULL,
		[price] [decimal](8, 2) NULL,
		[updown] [decimal](8, 2) NULL,
		[vol] [decimal](15, 2) NULL,
		[amount] [decimal](20, 2) NULL,
		[bs] [char](10) NULL,
	 CONSTRAINT [PK_fenbi_'+ltrim(rtrim(@tableName))+'] PRIMARY KEY CLUSTERED 
	(
		[id] ASC,
		[ts_code] ASC,
		[trade_time] ASC
	)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
	) ON [PRIMARY]
	 '        
        EXEC(@CreateSQL)		
    end
end
