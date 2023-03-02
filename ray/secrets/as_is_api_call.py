import pandas as pd
from batch.batch_cn.util.dbConnect import exec_query, insert_data
import logging
from datetime import datetime, timedelta, date
import akshare as ak

import pandas as pd
from batch.batch_cn.util.dbConnect import exec_query, insert_data
import logging
from datetime import datetime, timedelta, date
import akshare as ak

logging.basicConfig(level=logging.INFO)

## stock_cd / isin / ticker /market 불러오기
sit = pd.DataFrame(exec_query(
    f"""
        select 
            a.*,
            (
                case
                    when b.market = 'SSEC' then 'sh'
                    when b.market = 'SZSE' then 'sz'
                    else 'no_market'
                end    
            ) as market
            from (
                select * from stock_cn.stock_isin_ticker_mapping
            ) as a 

            left join (
                select distinct(stock_cd), market from stock_cn.stock_daily_technical
            ) as b    
            on a.stock_cd=b.stock_cd    

            order by a.ticker
    """,
    cursor='dict')
)
sit['market'].value_counts()

sit = sit[sit['market'] != 'no_market'].reset_index(drop=True)
sit['akcode'] = sit['market'] + sit['ticker']


latest_date = exec_query('select max(date) from stock_cn.stock_daily_technical')
if latest_date[0][0] is not None:
    latest_date = datetime.strptime(str(latest_date[0][0]), '%Y%m%d').date()
else:
    latest_date = datetime.strptime('20090101', '%Y%m%d').date()

today = date.today()

update_list = [
    (latest_date + timedelta(days=delta)).strftime('%Y-%m-%d') for delta in range((today-latest_date).days+1)
]
del update_list[0]

start_date = update_list[0]
end_date = update_list[len(update_list)-1]

# (AS-IS) 멀티프로세서 쓰기 전
stock_list_to_scrape = sit['akcode'].tolist()
df_akshare = pd.DataFrame()
for stock in stock_list_to_scrape:
    try:
        df = ak.stock_zh_a_daily(symbol=stock, start_date=start_date, end_date=end_date)
        if not df.empty:
            df['market_cap'] = df['close'] * df['outstanding_share']
            df['akcode'] = stock
            df = df[['akcode', 'date', 'close', 'outstanding_share', 'market_cap']]
            # df.set_index('date', inplace=True)
            df_akshare = pd.concat([df_akshare, df], ignore_index=True)
            print(stock_list_to_scrape.tolist().index(stock), ' | ', len(stock_list_to_scrape), ' | ', df_akshare.shape)
            del df
        pass
        # time.sleep(0)
    except:
        # catch the error and continue to the next iteration
        continue