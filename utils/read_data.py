__author__ = 'Victoria'

# 2018-09-26

import os
import json
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_signals(file_date, part, file_dir='../../Smart City/data/hf_signals/'):
    '''
    Get the signal data from one file named "%s/hf_%s/part-%s" % (data_dir, file_date, part)
    :param file_date: (str) yyyymmdd
    :param part: (str) e.g: 00000
    :param file_dir:
    :return:
    '''
    # filename = file_dir + 'hf_' + str(file_date) + '/part-' + part
    filename = os.path.join(file_dir, 'hf_' + str(file_date), 'part-' + part)
    f = open(filename)
    dates, cell_id, user_id, service_type, web = [], [], [], [], []

    for line in f.readlines():
        line_tmp = line.strip('()\n').split(',')
        dates.append(get_date_type(line_tmp[0]))
        cell_id.append(line_tmp[1])
        user_id.append(line_tmp[2])
        service_type.append(line_tmp[3])
        web.append(line_tmp[4])
    f.close()
    return pd.DataFrame({'dates': dates, 'cell_id': cell_id, 'user_id': user_id,
                         'service_type': service_type, 'web': web})


def get_datetime(t):
    '''Transfer a string time to datetime format.'''
    print(t)
    if '/' in t:
        pattern = '%Y/%m/%d %H:%M:%S'
    elif '-' in t:
        pattern = '%Y-%m-%d %H:%M:%S'
    else:
        pattern = '%Y%m%d%H%M%S'

    return datetime.datetime.strptime(t, pattern)


def get_date_type(date0):
    '''
    :param date0: yyyy/mm/dd HH:MM:SS.xxx
    :return A datetime date
    Transfer a string time to datetime format.
    Specifically for signal data reading.
    '''
    day, time = date0.split(' ')
    day = day.split('/')
    time = time.split(':')
    return datetime.datetime(int(day[0]), int(day[1]), int(day[2]),
                             int(time[0]), int(time[1]), int(float(time[2])), int(float(time[2]) % 1))


def unique_users(signal_dir):
    not_found = []
    days = [d for d in os.listdir(signal_dir) if 'hf_' in d]
    for d in days:
        files = [f for f in os.listdir(os.path.join(signal_dir, d))  if 'part' in f]
        for f in files:
            not_found.append(os.path.join(d, f))

    user_dir = os.path.join(signal_dir, 'users')
    if os.path.exists(os.path.join(user_dir, 'users.json')):
        with open(os.path.join(user_dir, 'users.json')) as f:
            users = json.load(f)
            found = users['found']
            users = users['users']
    else:
        found = []
        users = {}

    # TODO:


def user_based_singal_data():
    '''Prepare user based signal data'''
    # TODO:
    pass


def check_dir(dir_name):
    '''
    Check if the directory exists. If not exists, it will be create.
    :param dir_name: directory name [String]
    :return: No return
    '''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def time_based_signal_data(signal_dir, file_date):
    '''
    Prepare time based signal data
    :param signal_dir: (str) e.g: "~/hf_signals"
    :param file_date: (str) e.g: "20170607"
    :return:
    '''
    check_dir(os.path.join(signal_dir, 'time_based_signals'))
    parts = [f.split('-')[1] for f in os.listdir(os.path.join(signal_dir, 'hf_'+file_date)) if 'part' in f]
    df = None
    t0 = time.time()

    for i, part in enumerate(parts):
        tmp = get_signals(file_date, part, signal_dir)
        if df is None:
            df = tmp
        else:
            df = pd.concat([df, tmp])

        if i % 30 == 0:
            df['time_minute'] = ['%s%.2d' % (t.strftime('%Y%m%d-%H'), (t.minute//5)*5) for t in df.dates]
            unique_minute = np.unique(df.time_minute)
            for t_min in unique_minute:
                out_f = os.path.join(signal_dir, 'time_based_signals', t_min+'.csv')
                df_min = df[df.time_minute == t_min]
                df_min = df_min.drop(['time_minute'], axis=1)
                if os.path.exists(out_f):
                    df_min.to_csv(out_f, index=False, mode='a', header=False)
                else:
                    df_min.to_csv(out_f, index=False)
            df = None

        if i % 10 == 0:
            print('%d parts is finished. Cost %.2f s.' % (i, time.time() - t0))
            t0 = time.time()

    pass


class _Test:
    def __init__(self):
        return

    def test_fun(self):
        df = get_signals('20170607', '00000')
        print(df.head())

    def test_unique_users(self):
        signal_dir = '/Users/Viki/Documents/yhliu/Smart City/data/hf_signals'
        unique_users(signal_dir)

    def test_time_based_signal_data(self):
        signal_dir = '/Users/Viki/Documents/yhliu/Smart City/data/hf_signals'
        file_date = '20170607'
        time_based_signal_data(signal_dir, file_date)


if __name__ == '__main__':
    test = _Test()
    # test.test_fun()
    # test.test_unique_users()
    test.test_time_based_signal_data()

    pass