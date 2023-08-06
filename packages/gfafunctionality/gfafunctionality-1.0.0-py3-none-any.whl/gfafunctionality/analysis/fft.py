import numpy as np
import matplotlib.pyplot as plt
import csv

class FileFFT(object):
    def __init__(self, csv_path, sampling_rate=100E6):
        self._csv_path = csv_path
        self._raw_data = None
        self.pixels = []
        self.sr = sampling_rate
        self._values = []
        self._values_ref = []
        self._values_sign = []
        self.n = 0
        self.sampling_interval = 0

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

        for row in self._raw_data:
            t_value, t_low, t_high = int(row[0]), int(row[1]), int(row[2])
            self._values.append(t_value)
            if t_high == 1:
                self._values_ref.append(t_value)
            if t_low == 1:
                self._values_sign.append(t_value)

        self.n = 2*int(len(self._values)/2)
        self.sampling_interval = self.n/self.sr
        print("Found {} Pixels".format(len(self._values)))

    def show_fft(self):

        k = np.arange(self.n)
        frq = k*self.sr/self.n
        frq = frq[range(int(self.n/2))]

        t = np.arange(0, self.n/self.sr, 1/self.sr)

        fft = np.fft.fft(self._values[:self.n])/self.n

        fig, ax = plt.subplots(2, 1)
        ax[0].plot(t, self._values)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Amplitude')

        ax[1].plot(frq, fft[range(int(self.n/2))])
        ax[1].set_xlabel('Freq (Hz)')
        ax[1].set_ylabel('|Y(freq)|')

        plt.show()


if __name__ == "__main__":
    import os
    print(os.path.abspath('.'))
    CSV_PATH = '/home/otger/development/desi/analysis/Imatge_otger/'
    CSV_FILES = ['IMG_57_0.csv', 'IMG_57_1.csv', 'IMG_57_2.csv', 'IMG_57_3.csv']

    anal = FileFFT(os.path.abspath(os.path.join(CSV_PATH, CSV_FILES[3])))
    anal.load_data()
    anal.parse_data()
    anal.show_fft()

