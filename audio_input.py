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

        self.scope_plot = self.window.addPlot(title="Updating plot")
        self.scope_curve = self.scope_plot.plot(pen='y')
        # data = np.random.normal(size=(10,1000))
        self.scope_plot.setXRange(0, 1024)
        self.scope_plot.setYRange(-1500, 1500)
        self.scope_plot.showGrid(x=True, y=True)

        self.window.nextRow()

        self.spectrum_plot = self.window.addPlot(title="Updating plot")
        self.spectrum_curve = self.spectrum_plot.plot(pen='y')
        # data = np.random.normal(size=(10,1000))
        self.spectrum_plot.showGrid(x=True, y=True)

        self.audio_capture = AudioCapture(self)
        self.audio_capture.start()

        "communication between capture and display."
        self.audio_capture.c.drawSlot.connect(self.update)

        ############################
        self.cosine = signal_lib.CosineCarrier()

    def update(self, data):
        global ptr

        self.spectrum_curve.setData(data)

        if ptr == 0:

            self.spectrum_plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        ptr += 1
        # timer = QtCore.QTimer()
        # timer.timeout.connect(update)
        # timer.start(50)

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




