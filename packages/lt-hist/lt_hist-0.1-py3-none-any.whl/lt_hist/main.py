from datetime import datetime, timedelta
from collections import defaultdict
import sys
from lt_hist import plot
import tarfile
import json
import os
import glob
import shutil
import boto3
import boto3


def do(lt_name, past_days):
    bucket = 'nv-production-loadtest'
 
    get_files(bucket, lt_name, past_days)
    copy_stats_files(lt_name)
    delete_dirs(lt_name)
    data = consolidate()
    # data = _read()
    endpoints, dates = doit(data, past_days)
    plot.plot_data(endpoints, dates)


def doit(data: dict, past_days: int):
    endpoints = defaultdict(list)
    dates = []
    sorted_keys_date = list(data.keys())
    sorted_keys_date.sort()

    for report_date in sorted_keys_date:
        day = data[report_date]
        report_date = '{}/{}/{}'.format(report_date[6:8], report_date[4:6], report_date[:4])
        dates.append(report_date)
        for endpoint in day['contents'].values():
            endpoint_path = endpoint['path']
            stats = endpoint['stats']
            item = {
                'max_response_time': stats['maxResponseTime'],
                'min_response_time': stats['minResponseTime'],
                'total_requests': stats['numberOfRequests'],
                'p50': stats['percentiles1'],
                'p75': stats['percentiles2'],
                'p95': stats['percentiles3'],
                'p99': stats['percentiles4'],
            }
            endpoints[endpoint_path].append(item)
    
    return endpoints, dates


def copy_stats_files(lt_name: str):
    dirs = glob.glob('{}*'.format(lt_name))

    print("Copying the files from the gatling report")
    for d in dirs:
        stat_file = '{}/js/stats.json'.format(d)
        to = 'stats{}.json'.format(d.split(lt_name)[1])
        shutil.copy(stat_file, to)


def delete_dirs(lt_name:str): 
    dirs = glob.glob('{}*'.format(lt_name))

    print('Deleting the leftovers')
    for d in dirs:
        shutil.rmtree(d)


def get_files(bucket: str, lt_name: str, past_days: int):

    prefix = '{}/gatling-report/'.format(lt_name)

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)
    objects = my_bucket.objects.filter(Prefix=prefix)
    objects = [obj for obj in objects.all()]
    objects.sort(key=lambda x: x.key, reverse=True)

    objects_from_past_days = objects[:past_days*2]
    filtered = []
    for obj in objects_from_past_days:
        if 'logs' in obj.key:
            continue
        filtered.append(obj)

    print('Fetching, downloading and extracting the last {} reports'.format(past_days))
    for obj in filtered:
        path, filename = os.path.split(obj.key)

        if 'logs' in obj.key: # get only the reports
            continue

        my_bucket.download_file(obj.key, filename)
        tar = tarfile.open(filename, 'r:gz')
        tar.extractall()
        tar.close()
        os.remove(filename)


def _read():
    files_data = {}
    with open('consolidated.json', 'r') as f:
        files_data = json.loads(f.read())
    return files_data


def consolidate() -> dict:
    stats_files = glob.glob('stats-*.json')

    files_data = {}
    for f in stats_files:
        with open(f) as json_f:
            f_name = f.replace('.json', '').replace('stats-', '')
            files_data[f_name] = json.load(json_f)
        os.remove(f)

    print('Consolidating all the info into one file')
    with open('consolidated.json', 'w') as outfile:
        json.dump(files_data, outfile)

    return files_data


if __name__ == "__main__":
    do(sys.argv[1], int(sys.argv[2]))
    # os.environ['AWS_PROFILE'] = 'prod-legacy'
    # main('lt-account', 10)