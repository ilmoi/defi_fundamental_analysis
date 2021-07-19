import csv
import datetime
from typing import Dict, List


def calc_avg_over_period(days_ago_start, days_ago_end, series):
    time_start = (datetime.datetime.now() - datetime.timedelta(days=days_ago_start)).timestamp()
    time_end = (datetime.datetime.now() - datetime.timedelta(days=days_ago_end)).timestamp()

    relevant_list = filter(lambda x: time_start <= int(x['date']) <= time_end, series)
    relevant_list = list(map(lambda x: x['totalLiquidityUSD'], relevant_list))
    if len(relevant_list) > 0:
        return sum(relevant_list) / len(relevant_list)
    else:
        return 0


def merge_two_lists_of_dicts(list1: List[Dict], list2: List[Dict]):
    merged_list = []
    for l1 in list1:
        for l2 in list2:
            if l1['id'] == l2['id']:
                merged_list.append({**l1, **l2})
    return merged_list


def save_data(results, fieldnames):
    with open('output/defi_data.csv', mode='w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()

        for result in results:
            filtered_res = {}

            for (k, v) in result.items():
                if k in fieldnames:
                    if k == 'ytd':
                        filtered_res[k] = v['price_change']
                    else:
                        filtered_res[k] = v

            csv_writer.writerow(filtered_res)
