import threading
import pyaudio
import sys
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pylab as plt

CHUNK = 1024
PYAUDIO_FORMAT_INT16 = pyaudio.paInt16
CHANNELS = 1
SOUND_CARD_RATE = 8000
RECORD_SECONDS = 5

class SlotCommunicate(QtCore.QObject):
    drawSlot = QtCore.pyqtSignal(object)

class DisplaySignal():
    def __init__(self):
        self.window = pg.GraphicsWindow(title="Basic plotting examples")
        self.window.resize(1000, 600)
        self.window.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.spectrum_plot = self.window.addPlot(title="Updating plot")
        self.spectrum_curve = self.spectrum_plot.plot(pen='y')
        # data = np.random.normal(size=(10,1000))
        self.spectrum_plot.showGrid(x=True, y=True)

        self.spectrum_plot.setXRange(0, 1024)
        self.spectrum_plot.setYRange(-1500, 1500)

        self.window.nextRow()

        self.audio_capture = AudioCapture(self)
        self.audio_capture.start()

        "communication between capture and display."
        self.audio_capture.c.drawSlot.connect(self.update)

    def update(self, data):
        global ptr

        self.spectrum_curve.setData(data*5)

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
            self.in_stream = self.p.open(format=PYAUDIO_FORMAT_INT16,
                channels=CHANNELS,
                rate=SOUND_CARD_RATE,
                input=True,
                frames_per_buffer=CHUNK)

            self.out_stream = self.p.open(format=PYAUDIO_FORMAT_INT16, channels=CHANNELS,
                                         rate=SOUND_CARD_RATE,
                                         output=True)

            print "open sound card succ. Sound card rate is: ", SOUND_CARD_RATE
        except:
            print "open sound card failure!"

        print SOUND_CARD_RATE / CHUNK * RECORD_SECONDS


    def run(self):
        #for i in range(0, int(SOUND_CARD_RATE / CHUNK * RECORD_SECONDS)):
        while True:
            self.audio_data = self.in_stream.read(CHUNK)
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




