--Filtered data for Broadcaster

SELECT *
INTO #TEMP_BROADCASTER
FROM [dbo].[TBL_BROADCASTER]
WHERE [Code] NOT IN ('ADM', 'DWL', 'KBS')


DROP TABLE #TEMP_BROADCASTER


--Cleaned data without Alpha numeric characters in 'CirafZones'

SELECT Freq, 
		[Start],
		[Stop], 
		[CirafZones], 
		CASE WHEN TRY_CAST([CirafZones] AS DECIMAL) IS NULL THEN 0 ELSE 1 END AS 'Criteria',
		[Powr], 
		[AziMuth], 
		[Slew], 
		[Days], 
		[Sdate], 
		[Edate], 
		[Mod], 
		[Afrq], 
		[FmoCode], 
		[BroadcasterCode], 
		bro.[Broadcaster], 
		[AdminCode], 
		[AdminName], 
		[LanguageCode], 
		[Language], 
		[AntCode], 
		[Ant] as 'Antenna Type', 
		[LocCode], 
		[Site] as 'Transmitter',
		[Adm],
		[Lat],
		[Long]
FROM
[dbo].[TBL_HF_SCHEDULE] sc
JOIN #TEMP_BROADCASTER bro ON sc.BroadcasterCode = bro.Code
JOIN [dbo].[TBL_ADMIN] adm ON sc.AdminCode = adm.Code
JOIN [dbo].[TBL_LANGUAGE] lan ON sc.LanguageCode = lan.Code
JOIN [dbo].[TBL_ANT] ant ON sc.AntCode = ant.Code
JOIN [dbo].[TBL_LOCATION] loc on sc.LocCode = loc.Code
WHERE (sc.Freq = '5890'
	OR sc.Freq = '6040'
	OR sc.Freq = '7220'
	OR sc.Freq = '9490'
	OR sc.Freq = '9510')
	AND (CASE WHEN TRY_CAST([CirafZones] AS DECIMAL) IS NULL THEN 0 ELSE 1 END) = 1
