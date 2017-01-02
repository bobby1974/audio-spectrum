# -*- coding: utf-8 -*-
# |----------------------------------------------------------------------| #
# | Copyright (C) Bobby, BH7PRM, 2016                                    | #
# |                                                                      | #
# | This program is free software: you can redistribute it and/or modify | #
# | it under the terms of the GNU General Public License as published by | #
# | the Free Software Foundation, either version 3 of the License, or    | #
# | any later version.                                                   | #
# |                                                                      | #
# | This program is distributed in the hope that it will be useful,      | #
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       | #
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        | #
# | GNU General Public License for more details.                         | #
# |                                                                      | #
# | You should have received a copy of the GNU General Public License    | #
# | along with this program.  If not, see <http://www.gnu.org/licenses/>.| #
# |----------------------------------------------------------------------| #

import numpy as np

import pylab as plt

fs = 64. #sampling frequency
t  = np.arange(0, 2.0, 1/fs) #2 seconds sampling data
FFT_SIZE = 16

fc = 4
unit = fs/FFT_SIZE

x = np.sin(2.*np.pi*fc*t)
x_sample = x[:FFT_SIZE]

y_fft = np.fft.fft(x_sample) / FFT_SIZE

freq  = np.fft.fftfreq(x_sample.shape[-1])*fs

fft_amp = np.abs(y_fft[:FFT_SIZE/2])
#fft_real = 20*np.log10(np.clip(np.abs(fft_real), 1e-20, 1e100))

freq = freq[:FFT_SIZE/2]
print freq
print fft_amp

plt.stem(freq, fft_amp, '-.')

#plt.plot(freq, fft_real, 'bo')
#plt.plot(freq, fft_real, label="$fft$",color="blue",linewidth=2)

plt.xlabel('Hz')
plt.ylabel('amplitude')
plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.grid()
plt.show()