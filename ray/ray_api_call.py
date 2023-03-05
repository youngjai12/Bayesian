import ray
import akshare as ak
import threading
import time
from ray._private import utils

def upload_stock():
    my_list = []
    with open("./secrets/china_stock_list.txt", "r") as f:
        my_list = f.read().splitlines()

    return my_list


@ray.remote
def scrape_stock_data(stock, start_date):
    current_thread_name = threading.current_thread().name
    current_timestmap = time.time()

    try:
        response = ak.stock_zh_a_daily(symbol=stock, start_date=start_date, end_date=start_date)

        result = f"{stock} {response['open']} {response['low']} cpu-core(none)) thread({current_thread_name}) {current_timestmap}"

    except Exception as e:
        result = f"{stock} ERROR ERROR-low cpu-core(none) thread({current_thread_name}_ {current_timestmap}"
        print(f"{stock} has {e}")
    return result


if __name__ == '__main__':
    print(ray.__version__)
    to_update_stock = upload_stock()[0:300]
    # ray.init(object_store_memory=4 * 1024 * 1024 * 1024) The configured object store size (4.0GiB) exceeds the optimal size on Mac (2.0GiB). This will harm performanc
    ray.init()
    start_time = time.time()
    start_date = end_date = "20230301"

    final_result_list = []
    futures = [scrape_stock_data.remote(stock, start_date) for stock in to_update_stock]
    for i, future in enumerate(ray.get(futures)):
        if future is not None:
            final_result_list.append(future)
    end_time = time.time()

    with open("./secrets/ray_call_result_cpu_0.3k.txt", "w") as f:
        for record in final_result_list:
            f.write(f"{record}\n")
        f.write(f"tot elapsed : {end_time - start_time}")