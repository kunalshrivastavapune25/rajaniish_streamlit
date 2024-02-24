drop table IF EXISTS N100_OHLC_1H;
create table N100_OHLC_1H AS
SELECT 
    strftime('%Y-%m-%d %H:00:00', Datetime) AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM N100_OHLC
GROUP BY strftime('%Y-%m-%d %H:00:00', Datetime), ticker;

drop table IF EXISTS N100_OHLC_1D;
create table N100_OHLC_1D AS
SELECT 
    strftime('%Y-%m-%d 00:00:00', Datetime) AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM N100_OHLC
GROUP BY strftime('%Y-%m-%d 00:00:00', Datetime), ticker;

 
drop table IF EXISTS N100_OHLC_15M; 
create table N100_OHLC_15M AS
SELECT 
    substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00' AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM N100_OHLC
GROUP BY substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00', ticker;


drop table IF EXISTS NINDEX_OHLC_1H;
create table NINDEX_OHLC_1H AS
SELECT 
    strftime('%Y-%m-%d %H:00:00', Datetime) AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM NINDEX_OHLC
GROUP BY strftime('%Y-%m-%d %H:00:00', Datetime), ticker;

drop table IF EXISTS NINDEX_OHLC_1D;
create table NINDEX_OHLC_1D AS
SELECT 
    strftime('%Y-%m-%d 00:00:00', Datetime) AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM NINDEX_OHLC
GROUP BY strftime('%Y-%m-%d 00:00:00', Datetime), ticker;

 
drop table IF EXISTS NINDEX_OHLC_15M; 
create table NINDEX_OHLC_15M AS
SELECT 
    substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00' AS Datetime,
    ticker,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume
FROM NINDEX_OHLC
GROUP BY substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00', ticker;


drop table IF EXISTS nniftyoptions_ohlc_1H;
create table nniftyoptions_ohlc_1H AS
SELECT 
    strftime('%Y-%m-%d %H:00:00', Datetime) AS Datetime,
    stock_code,expiry_date,right,strike_price,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume,
	LAST_VALUE(open_interest) OVER (ORDER BY  Datetime) AS open_interest
FROM nniftyoptions_ohlc
GROUP BY strftime('%Y-%m-%d %H:00:00', Datetime), stock_code,expiry_date,right,strike_price;

drop table IF EXISTS nniftyoptions_ohlc_1D;
create table nniftyoptions_ohlc_1D AS
SELECT 
    strftime('%Y-%m-%d 00:00:00', Datetime) AS Datetime,
    stock_code,expiry_date,right,strike_price,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume,
	LAST_VALUE(open_interest) OVER (ORDER BY  Datetime) AS open_interest
FROM nniftyoptions_ohlc
GROUP BY strftime('%Y-%m-%d 00:00:00', Datetime), stock_code,expiry_date,right,strike_price;

 
drop table IF EXISTS nniftyoptions_ohlc_15M; 
create table nniftyoptions_ohlc_15M AS
SELECT 
    substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00' AS Datetime,
    stock_code,expiry_date,right,strike_price,
    FIRST_VALUE(Open) OVER (ORDER BY  Datetime) AS Open,
    MAX(High) AS High,
    MIN(Low) AS Low,
    LAST_VALUE(Close) OVER (ORDER BY  Datetime) AS Close,
    SUM(Volume) AS Volume,
	LAST_VALUE(open_interest) OVER (ORDER BY  Datetime) AS open_interest
FROM nniftyoptions_ohlc
GROUP BY substr(Datetime,1,14) ||
substr(replace(cast(15* (cast(substr(Datetime,15,2) as integer)/15 ) as text),'0','00'),1,2) 
|| ':00', stock_code,expiry_date,right,strike_price;


drop table tab_summary;
create table tab_summary as
select 'Nifty100-15min' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from N100_OHLC_15M
UNION
select 'NiftyINDEX-15min' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from NINDEX_OHLC_15M
UNION
select 'Nifty100-1H' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from N100_OHLC_1H
UNION
select 'NiftyINDEX-1H' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from NINDEX_OHLC_1H
UNION
select 'Nifty100-1D' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from N100_OHLC_1D
UNION
select 'NiftyINDEX-1D' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from NINDEX_OHLC_1D
union
select 'nniftyoptions-1H' as DATA, count(distinct strike_price) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from nniftyoptions_OHLC_1H
UNION
select 'nniftyoptions-1D' as DATA, count(distinct strike_price) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from nniftyoptions_OHLC_1D
UNION
select 'nniftyoptions-15min' as DATA, count(distinct strike_price) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
from nniftyoptions_OHLC_15M
order by 1