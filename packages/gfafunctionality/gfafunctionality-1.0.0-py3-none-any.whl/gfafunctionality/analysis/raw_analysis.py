import numpy as np
from scipy import stats
import csv

class Analysis(object):
    def __init__(self, csv_path):
        self._csv_path = csv_path
        self._raw_data = None
        self.pixels = []

    def load_data(self):
        self._raw_data = []
        with open(self._csv_path) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0].startswith('#'):
                    print('skipped line: {}'.format(row))
                    continue
                self._raw_data.append(row)

    def parse_data(self):
        self.pixels.append(Pixel())
        high = 0
        for row in self._raw_data:
            t_value, t_low, t_high = int(row[0]), int(row[1]), int(row[2])
            if high:
                if t_high == 0:
                    self.pixels.append(Pixel())
            if t_high or t_low:
                self.pixels[-1].add_point(t_value, t_low, t_high)
            high = t_high

        print("Found {} Pixels".format(len(self.pixels)))


class Pixel(object):
    def __init__(self):
        self.high_values = []
        self.low_values = []
        self.trim = 0.3

    def add_point(self, value, low=False, high=False):
        if high:
            self.high_values.append(value)
        if low:
            self.low_values.append(value)

    @property
    def average(self):
        return self.high_average - self.low_average

    @property
    def high_average(self):
        return np.average(self.high_values)

    @property
    def low_average(self):
        return np.average(self.low_values)

    @property
    def median(self):
        return self.high_median - self.low_median

    @property
    def high_median(self):
        return np.median(self.high_values)

    @property
    def low_median(self):
        return np.median(self.low_values)

    @property
    def high_trim_mean(self):
        return stats.trim_mean(self.high_values, self.trim)

    @property
    def low_trim_mean(self):
        return stats.trim_mean(self.low_values, self.trim)

    @property
    def trim_mean(self):
        return self.high_trim_mean - self.low_trim_mean

    @property
    def samples(self):
        return len(self.high_values), len(self.low_values)

    @property
    def diff(self):
        return self.average - self.median


if __name__ == '__main__':
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt


    import os
    print(os.path.abspath('.'))
    CSV_PATH = '/home/otger/development/desi/analysis/Imatge_otger/'
    CSV_FILES = ['IMG_57_0.csv', 'IMG_57_1.csv', 'IMG_57_2.csv', 'IMG_57_3.csv']
    anals = []
    for fn in CSV_FILES:
        anal = Analysis(os.path.abspath(os.path.join(CSV_PATH, fn)))
        anal.load_data()
        # print(anal._raw_data)
        anal.parse_data()
        anals.append(anal)

    # p30 = anal.pixels[30]


    # the histogram of the data
    # plt.figure(1)
    # plt.subplot()
    # n, bins, patches = plt.hist(p30.high_values, 20, density=1, facecolor='green', alpha=0.75)
    # avg = plt.axvline(x=p30.high_average, color='black', label='average')
    # med = plt.axvline(x=p30.high_median, color='green', label='median')
    # trim = plt.axvline(x=p30.high_trim_mean, color='blue', label='trim_mean 30%')
    # plt.legend(handles=[avg, med, trim])
    # plt.figure(2)
    # n, bins, patches = plt.hist(p30.low_values, 20, density=1, facecolor='red', alpha=0.75)
    # avg = plt.axvline(x=p30.low_average, color='black', label='average')
    # med = plt.axvline(x=p30.low_median, color='green', label='median')
    # trim = plt.axvline(x=p30.low_trim_mean, color='blue', label='trim_mean 30%')
    # plt.legend(handles=[avg, med, trim])

    for ix, anal in enumerate(anals):
        plt.figure(ix)
        plt.subplot(3, 1, 1)
        averages = [el.average for el in anal.pixels[15:46]]
        xs = np.arange(15, 46)
        stdev = np.std(averages)
        avg = np.average(averages)
        print(type(avg))
        h, = plt.plot(xs, averages, color='blue', label='pixel value - chanel {}'.format(ix))
        s = plt.axhline(avg, label='average: {:.3f} - std: {:.3f}'.format(avg, stdev), color='red')
        plt.title('Using average')
        plt.legend(handles=[h, s])

        plt.subplot(3, 1, 2)
        median = [el.median for el in anal.pixels[15:46]]
        stdev = np.std(median)
        avg = np.average(median)
        print(type(avg))
        h, = plt.plot(xs, median, color='blue', label='pixel value - chanel {}'.format(ix))
        s = plt.axhline(avg, label='average: {:.3f} - std: {:.3f}'.format(avg, stdev), color='red')
        plt.title('Using median')
        plt.legend(handles=[h, s])

        plt.subplot(3, 1, 3)
        trim_mean = [el.trim_mean for el in anal.pixels[15:46]]
        stdev = np.std(trim_mean)
        avg = np.average(trim_mean)
        print(type(avg))
        h, = plt.plot(xs, trim_mean, color='blue', label='pixel value - chanel {}'.format(ix))
        s = plt.axhline(avg, label='average: {:.3f} - std: {:.3f}'.format(avg, stdev), color='red')
        plt.title('Using trim_mean 30%')
        plt.legend(handles=[h, s])

    plt.show()

