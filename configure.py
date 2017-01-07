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

import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

FFT_SIZE             = 2048
FFT_COMPLEX_TYPE     = 0
FFT_REAL_TYPE        = 1

SOUND_CARD_CHUNK     = FFT_SIZE
PYAUDIO_FORMAT_INT16 = pyaudio.paInt16
SOUND_CARD_CHANNELS  = 1
SOUND_CARD_RATE      = 16000
RECORD_SECONDS       = 5

