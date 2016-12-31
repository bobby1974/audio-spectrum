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
import scipy.signal as signal
from scipy      import fftpack
import configure as cfg

class CosineCarrier(object):
    def __init__(self):
        self.n = 0

    def set_phase(self, phase):
        self.n = phase

    def cosine_carrier(self, fc, fs, fft_size, amplitude):
        "fc:carrier freq, fs:sample rate"
        cosineResult = np.arange(0, fft_size, 1.0)
        n = self.n

        for i in range(fft_size):
            angle = 2. * np.pi * fc * n / fs

            if angle >= 2. * np.pi * fc:
                n = 0

            cosineData = amplitude*np.cos(angle)

            n += 1

            cosineResult[i] = cosineData

            self.n = n

        return cosineResult


class SineCarrier(object):
    def __init__(self):
        self.n = 0

    def sine_carrier(self, fc, fs, fft_size, amplitude):
        sineResult = np.arange(0, fft_size, 1.0)

        n = self.n

        for i in range(fft_size):
            angle = 2. * np.pi * fc * n / fs

            if angle >= 2. * np.pi * fc:
                n = 0

            sineData = amplitude * np.sin(angle)

            n += 1

            sineResult[i] = sineData

        self.n = n

        return sineResult


class ExpCarrier(object):
    def __init__(self):
        self.n = 0

    "flag:-j or j"

    def exp_carrier(self, fc, fs, fft_size, amplitude):
        expResult = np.arange(0, fft_size, 1.0, dtype=np.complex64)

        n = self.n

        for i in range(fft_size):
            angle = -1.0j * 2. * np.pi * fc * n / fs

            expData = amplitude * np.exp(angle)

            n += 1

            expResult[i] = expData

        self.n = n

        return expResult
        # expCarrier()

# class expCarrier()
