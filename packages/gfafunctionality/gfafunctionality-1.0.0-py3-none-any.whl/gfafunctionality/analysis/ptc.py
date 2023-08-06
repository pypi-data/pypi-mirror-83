# GFAvariance3.py
# M.Lampton March 2018
# level shifting flats to make their averages equal
# Uppers are all dark; plotting only Lowers

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

"""
folder 20180326_140009.tgz
PTC_000 and 001.fits: lower, 0 sec flat
PTC_002 and 003.fits: upper, 0 sec dark
PTC_004 and 005.fits: lower, 2 sec flat: bright half is ~ 17K adu/pix
PTC_006 and 007.fits: upper, 2 sec dark
PTC_008 and 009.fits: lower, 4 sec flat: bright part is ~ 30K adu/pix
PTC_010 and 011.fits: upper, 4 sec dark
PTC_012 and 013.fits: lower, 6 sec flat: bright part is 43K adu/pix
PTC_014 and 015.fits: upper, 6 sec dark
PTC_016 and 017.fits: lower, 8 sec nearly overloaded: 50K adu/pix
PTC_018 and 019.fits: upper, 8 sec dark
PTC_020 and 021.fits: lower, 10 sec flat: overloaded
PTC_022 and 023.fits: upper, 10 sec dark
PTC_024 and 025.fits: lower, 12 sec flat: overloaded
PTC_026 and 027.fits: upper, 12 sec dark
PTC_028 and 029.fits: lower, 14 sec flat: overloaded
PTC_030 and 031.fits: upper, 14 sec dark
"""


def cleanup(ydata):
    mean = np.average(ydata)
    rms = np.std(ydata)
    ymin = mean - 3.0 * rms
    ymax = mean + 3.0 * rms
    for i in range(1, len(ydata)):
        if ydata[i] < ymin or ydata[i] > ymax:
            ydata[i] = ydata[i - 1]
    return ydata


quadlist = (1, 2, 3, 4)  # amplifiers E, F, G, H

filepairs = (('PTC_000.fits', 'PTC_001.fits', '0'),
             #     ('PTC_002.fits', 'PTC_003.fits', '0'),
             ('PTC_004.fits', 'PTC_005.fits', '2'),
             #     ('PTC_006.fits', 'PTC_007.fits', '2'),
             ('PTC_008.fits', 'PTC_009.fits', '4'),
             #     ('PTC_010.fits', 'PTC_011.fits', '4'),
             ('PTC_012.fits', 'PTC_013.fits', '6'),
             #     ('PTC_014.fits', 'PTC_015.fits', '6'),
             ('PTC_016.fits', 'PTC_017.fits', '8'))
#       ('PTC_018.fits', 'PTC_019.fits', '8'))

# Define two regions of interest: upper and lower
leftcol = 200
rightcol = 900
uppertop = 200
upperbot = 300
lowertop = 700
lowerbot = 800

for filepair in filepairs:

    for quadrant in quadlist:
        file0 = filepair[0]
        try:
            hdu0 = fits.open(file0)
        except IOError:
            print
            'File cannot be found: ' + file0
            quit()
        data0 = hdu0[quadrant].data
        hdu0.close()

        file1 = filepair[1]
        try:
            hdu1 = fits.open(file1)
        except IOError:
            print
            'File cannot be found: ' + file1
        data1 = hdu1[quadrant].data
        hdu1.close()

        uppersumlist = list()
        lowersumlist = list()
        upperdifflist = list()
        lowerdifflist = list()

        for col in range(leftcol, rightcol):
            for row in range(uppertop, upperbot):  # define upper upper region
                upperdifflist.append(data1[row, col] - data0[row, col])
                uppersumlist.append(data1[row, col] + data0[row, col])
                # data1[row, col] = 10000
            for row in range(lowertop, lowerbot):  # define lower lower region
                lowerdifflist.append(data1[row, col] - data0[row, col])
                lowersumlist.append(data1[row, col] + data0[row, col])
                # data1[row, col] = 25000

        usums = np.array(uppersumlist)
        udiffs = np.array(upperdifflist)
        lsums = np.array(lowersumlist)
        ldiffs = np.array(lowerdifflist)

        usums = cleanup(usums)
        udiffs = cleanup(udiffs)
        lsums = cleanup(lsums)
        ldiffs = cleanup(ldiffs)

        uavesum = 0.5 * np.average(usums)  # to get adu per pixel
        uavediff = np.average(udiffs)
        udiffs -= int(uavediff)  # adjust to zero mean
        uavediff = np.average(udiffs)  # verify zero
        urms = np.std(udiffs)
        uvar = 0.5 * urms ** 2  # to get adu**2 per pixel

        lavesum = 0.5 * np.average(lsums)  # to get adu per pixel
        lavediff = np.average(ldiffs)
        ldiffs -= int(lavediff)  # adjust to zero mean
        lavediff = np.average(ldiffs)  # verify zero
        lrms = np.std(ldiffs)
        lvar = 0.5 * lrms ** 2  # to get adu**2 per pixel

        plt.plot((uavesum, lavesum), (uvar, lvar), 'o-')
        print
        filepair[0] + '  ' + filepair[1] + '  Quad=' + str(quadrant) + '  Texp=' + filepair[2]
        print
        'uavesum, uavediff, upperrms, uppervar = {:8.0f}{:8.0f}{:8.0f}{:8.0f}'.format(uavesum, uavediff, urms, uvar)
        print
        'lavesum, lavediff, lowerrms, lowervar = {:8.0f}{:8.0f}{:8.0f}{:8.0f}'.format(lavesum, lavediff, lrms, lvar)

plt.ylabel('variance, ADU^2/pixel')
plt.xlabel('mean, ADU/pixel')
plt.title('Flats from folder 20180326_140009.tgz  Texp=0,2,4,6,8sec')
plt.show()
