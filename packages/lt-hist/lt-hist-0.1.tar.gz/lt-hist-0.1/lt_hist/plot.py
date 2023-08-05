from datetime import date, timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import os


def plot_endpoint(endpoint, path, dates):
    p50, p75, p95, p99 = [], [], [], []

    for stats in endpoint:
        p50.append(stats['p50']['total'])
        p75.append(stats['p75']['total'])
        p95.append(stats['p95']['total'])
        p99.append(stats['p99']['total'])
    
    plt.plot(dates, p50, 'b-', label='p50')
    plt.plot(dates, p75, 'r-', label='p75')
    plt.plot(dates, p95, 'y-', label='p95')
    plt.plot(dates, p99, 'g-', label='p99')

    plt.legend(loc="upper left")
    plt.gcf().autofmt_xdate()
    plt.gcf().canvas.set_window_title(path)
    if not os.path.exists('plots'):
        os.mkdir('plots')
    filename = 'plots/{}.png'.format(path.replace('/', '_'))
    plt.savefig(filename)
    plt.clf()

def plot_data(endpoints: dict, dates: []):
    print('Ploting the graphs and saving them inside the ./plots dir')
    for path in endpoints.keys():
        plot_endpoint(endpoints[path], path, dates)
    print('Done')


def get_last_days(past_days:int) -> [datetime]:
    start = datetime.now() - timedelta(days=past_days)
    dates = []
    for i in range(past_days):
        day = start + timedelta(days=i+1)
        dates.append(day)

    return dates