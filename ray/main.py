import ray
import datetime
import time
import akshare as ak
import threading

def upload_stock():
    my_list = []
    with open("./secrets/china_stock_list.txt", "r") as f:
        my_list = f.read().splitlines()

    return my_list

if __name__ == '__main__':
    print(ray.__version__)
    to_update_stock = upload_stock()

    start_date = end_date = "20230301"

    cnt = 0

    ## return 값이 dataframe 임.
    # date open high low close volume outstanding_share turnover
    # result = ak.stock_zh_a_daily(symbol="sz000006", start_date=start_date, end_date=end_date)
    # print(result)

    for stock in to_update_stock:
        try:
            response = ak.stock_zh_a_daily(symbol=stock, start_date=start_date, end_date=end_date)
            cnt+=1
            current_thread_name = threading.current_thread().name
            current_timestmap = time.mktime(date_time.timetuple()))
            result = f"{stock} {response['open']} {response['low']} {current_thread_name}"
            if cnt%100==0:
                print(f"{cnt} has done!")
        except Exception as e:
            print(f"{stock} has {e}")


