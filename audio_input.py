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

import threading
import pyaudio
import sys
import numpy as np
import pyqtgraph as pg
import configure as cfg
import pylab as plt
import signal_lib as signal_lib

from pyqtgraph.Qt import QtGui, QtCore


class SlotCommunicate(QtCore.QObject):
    drawSlot = QtCore.pyqtSignal(object)

class DisplaySignal():
    def __init__(self):
        self.window = pg.GraphicsWindow(title="Basic plotting examples")
        self.window.resize(1000, 600)
        self.window.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.scope_plot = self.window.addPlot(title="Time domain Analysis")
        self.scope_curve = self.scope_plot.plot(pen='y')
        # data = np.random.normal(size=(10,1000))
        self.scope_plot.setXRange(0, 1024)
        self.scope_plot.setYRange(-1500, 1500)
        self.scope_plot.showGrid(x=True, y=True)

        self.window.nextRow()

        self.low_freq  = 0
        self.high_freq = cfg.SOUND_CARD_RATE/2.

        self.spectrum_plot = self.window.addPlot(title="Spectrum domain Analysis")
        self.spectrum_curve = self.spectrum_plot.plot(pen='y')
        # data = np.random.normal(size=(10,1000))
        self.spectrum_plot.setXRange(self.low_freq, self.high_freq)
        self.spectrum_plot.setYRange(0, -80)
        self.spectrum_plot.showGrid(x=True, y=True)

        self.audio_capture = AudioCapture(self)
        self.audio_capture.start()

        self.fft_data = np.zeros(cfg.SOUND_CARD_CHUNK)
        self.hanning_window = np.hanning(cfg.FFT_SIZE)

        "communication between capture and display."
        self.audio_capture.c.drawSlot.connect(self.update)

        ############################
        self.cosine = signal_lib.CosineCarrier()
    #__init__()

    def calculate_n_FFT(self, iqDataInput, fft_length, fft_counter, hanning_window, fft_type):
        i = 0
        fft_temp = 0
        power = 0

        for i in range(fft_counter):
            "对I/Q复数数据做FFT变换,numpy.fft.fft(a, n=None, axis=-1)[source]"
            "The values in the result follow so-called “standard” order: If A = fft(a, n), then A[0] contains"
            "the zero-frequency term (the mean of the signal), which is always purely real for real inputs. "
            "Then A[1:n/2] contains the positive-frequency terms, and A[n/2+1:] contains the negative-frequency "
            "terms, in order of decreasingly negative frequency. For an even number of input points, A[n/2] represents"
            " both positive and negative Nyquist frequency, and is also purely real for real input. For an odd number "
            "of input points, A[(n-1)/2] contains the largest positive frequency, while A[(n+1)/2] contains the largest"
            "negative frequency. The routine np.fft.fftshift(A) shifts transforms and their frequencies to put the "
            "zero-frequency components in the middle, and np.fft.ifftshift(A) undoes that shift."
            iqDataCmplx = iqDataInput[i * fft_length:(i + 1) * fft_length]

            "apply hanning window for FFT"
            power = np.multiply(iqDataCmplx, hanning_window)

            if fft_type == cfg.FFT_COMPLEX_TYPE:
                power = np.fft.fft(power)

                power = np.fft.fftshift(power)
            elif fft_type == cfg.FFT_REAL_TYPE:
                power = np.fft.rfft(power)

            power = np.abs(power)

            "average calculate for FFT to get better result."
            fft_temp = np.add(fft_temp, power)

        "每次读入的buffer个数据，使用FFT_AVERAGE个数据计算FFT"
        fft_temp = fft_temp / fft_counter

        "When the input a is a time-domain signal and A = fft(a), np.abs(A) is its amplitude spectrum and np.abs(A)**2"
        "is its power spectrum. The phase spectrum is obtained by np.angle(A)."

        "after average, it can be calculate for power spectrum"
        power_spectrum = (fft_temp * 1.0) / fft_length

        power_spectrum = 20 * np.log10(power_spectrum)

        return power_spectrum
    #calculate_n_FFT()

    def update(self, data):
        global ptr

        self.scope_curve.setData(data*1.5)

        self.fft_data = self.calculate_n_FFT(data, cfg.FFT_SIZE, 1,
                                              self.hanning_window, cfg.FFT_REAL_TYPE)
        self.fft_data -= 30

        self.fft_data = np.clip(self.fft_data, -80, 0)

        fftBinSeq = np.fft.rfftfreq(cfg.FFT_SIZE)

        x = self.low_freq + fftBinSeq * (self.high_freq - self.low_freq) * 2  # must multiply by two for it is fs

        self.spectrum_curve.setData(x, self.fft_data)

        if ptr == 0:

            self.spectrum_plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        ptr += 1
        # timer = QtCore.QTimer()
        # timer.timeout.connect(update)
        # timer.start(50)
#DisplaySignal()

class AudioCapture(threading.Thread):
    def __init__(self, displaySignal):
        threading.Thread.__init__(self)

        """pyaudio open the sound card"""
        self.p = pyaudio.PyAudio()

        print pyaudio.get_portaudio_version_text()

        print "(portaduio version:", pyaudio.get_portaudio_version(), ")"

        self.audio_data = 0
        self.displaySignal = displaySignal
        self.c = SlotCommunicate()

        try:
            self.in_stream = self.p.open(format=cfg.PYAUDIO_FORMAT_INT16,
                channels = cfg.SOUND_CARD_CHANNELS,
                rate = cfg.SOUND_CARD_RATE,
                input= True,
                frames_per_buffer = cfg.SOUND_CARD_CHUNK)

            self.out_stream = self.p.open(format = cfg.PYAUDIO_FORMAT_INT16, channels = cfg.SOUND_CARD_CHANNELS,
                                         rate = cfg.SOUND_CARD_RATE,
                                         output = True)

            print "open sound card succ. Sound card rate is: ", cfg.SOUND_CARD_RATE
        except:
            print "open sound card failure!"

    def run(self):
        #for i in range(0, int(SOUND_CARD_RATE / CHUNK * RECORD_SECONDS)):
        while True:
            self.audio_data = self.in_stream.read(cfg.SOUND_CARD_CHUNK)

            self.audio_data = np.fromstring(self.audio_data, dtype = np.int16)

            self.c.drawSlot.emit(self.audio_data)

            #self.displaySignal.update(self.audio_data)

            #self.outStream = self.out_stream.write(sound_card_data)

            #sound_card_data = np.ndarray.tostring(sound_card_data)

        self.in_stream.stop_stream()
        self.in_stream.close()

        self.out_stream.stop_stream()
        self.out_stream.close()

        self.p.terminate()

if __name__ == '__main__':

    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.resize(800,800)

    ptr = 0

    spectrum_plot = DisplaySignal()

    if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()




