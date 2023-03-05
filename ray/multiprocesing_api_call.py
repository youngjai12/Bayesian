import threading
import time
import akshare as ak
import multiprocessing
import psutil

def upload_stock():
    my_list = []
    with open("./secrets/china_stock_list.txt", "r") as f:
        my_list = f.read().splitlines()

    return my_list


def scrape_stock_data(stock):
    start_date = "20230301"
    current_thread_name = threading.current_thread().name
    current_timestmap = time.time()

    process = multiprocessing.current_process()
    process_id = process.pid
    process_info = psutil.Process(process_id)

    process_cpu_affinity = "don't know"

    #    cpu_id = utils.get_system_memory().get("node:0/cpu:0", {}).get("cpu_affinity", None)

    try:
        response = ak.stock_zh_a_daily(symbol=stock, start_date=start_date, end_date=start_date)

        result = f"{stock} {response['open']} {response['low']} cpu-core({process_cpu_affinity}) thread({current_thread_name}) {current_timestmap}"

    except Exception as e:
        result = f"{stock} ERROR ERROR-low cpu-core({process_cpu_affinity}) thread({current_thread_name}_ {current_timestmap}"
        print(f"{stock} has {e}")
    return result

if __name__ == '__main__':
    to_update_stock = upload_stock()[0:100]
    pool = multiprocessing.Pool(processes=4)
    results = pool.map(scrape_stock_data, to_update_stock)

    with open("./secrets/multiprocessing_cpu_call.txt", "w") as f:
        for record in results:
            f.write(f"{record}\n")