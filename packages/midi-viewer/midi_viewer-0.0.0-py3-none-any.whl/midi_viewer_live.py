from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import QRunnable
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QMainWindow, QAction, QMenu

from threading import Thread
from time import sleep
import math
import rtmidi
from enum import Enum


class MidiDeviceMenuParent(QMainWindow):
    def set_input_device(self, d_id):
        raise NotImplementedError()

    def get_input_devices(self) -> [str]:
        raise NotImplementedError()


class KeyboardDisplay(QWidget):

    class STATE(Enum):
        RELEASE = 0
        PRESS = 1
        SUSTAIN = 2

    def __init__(self, parent: QWidget, width=900):
        super().__init__(parent=parent)

        self.noctaves = 7
        self._startoctave = 1
        self.state = [self.STATE.RELEASE]*12*self.noctaves

        self.blackkeywidth = None
        self.whitekeywidth = None
        self.blackkeyheight = None
        self._x_offset = None

        self.setGeometry(QtCore.QRect(0, 0, width, 150))
        self._painter = QPainter(self)
        self._painter.setPen(QPen(QColor(0, 0, 0), 1))

        self._whitenote_colors = {self.STATE.PRESS: QColor(30, 200, 120),
                                  self.STATE.RELEASE: QColor(255, 255, 255),
                                  self.STATE.SUSTAIN: QColor(110, 223, 190)}

        self._blacknote_colors = {self.STATE.PRESS: QColor(30, 200, 120),
                                  self.STATE.RELEASE: QColor(0, 0, 0),
                                  self.STATE.SUSTAIN: QColor(15, 100, 60)}

        self._parent = parent

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50, 50, 50))
        self.setPalette(p)

        self._pedal_queue = []
        self._pedal_state = False

        self.show()

    def setGeometry(self, a0: QtCore.QRect) -> None:
        super().setGeometry(a0)
        octave_width = a0.width()/self.noctaves
        self.whitekeywidth = octave_width/7
        self.blackkeywidth = octave_width/12
        self.blackkeyheight = int(a0.height()*0.7)

    def _key_to_xlocs(self, note: int, isblacknote):
        if not isblacknote:
            octave = (note // 12)
            whiteindex = ((note % 12) + 1)//2
            x = (octave*7 + whiteindex) * self.whitekeywidth
            x1 =  math.floor(x)
            return x1, math.ceil(x + self.whitekeywidth) - x1
        else:
            x = int(note * self.blackkeywidth)
            return x, int(self.blackkeywidth)

    def handle_midi(self, msg: [int]):
        if msg[0] == 176:
            self._pedal_state = msg[2] > 0
            if not self._pedal_state:
                for i in self._pedal_queue:
                    self.set_key(i, self.STATE.RELEASE)
                self._pedal_queue.clear()
                self.update()
            return

        if msg[0] == 128:
            if self._pedal_state:
                self._pedal_queue.append(msg[1])
                self.set_key(msg[1], self.STATE.SUSTAIN)
            else:
                self.set_key(msg[1], self.STATE.RELEASE)
        elif msg[0] == 144:
            self.set_key(msg[1], self.STATE.PRESS)

        self.update()

    def set_key(self, key, state: STATE):
        keyofst = self._startoctave*12
        adjkey = key-keyofst
        if adjkey < 0 or adjkey >= len(self.state):
            return
        self.state[adjkey] = state


    def _draw_key(self, note: int, keystate: STATE):
        isblacknote = note % 12 in [1, 3, 6, 8, 10]
        x, w = self._key_to_xlocs(note, isblacknote=isblacknote)

        if isblacknote:
            self._painter.setBrush(self._blacknote_colors[keystate])
            self._painter.drawRect(x, 1, w, self.blackkeyheight)
        else:
            self._painter.setBrush(self._whitenote_colors[keystate])
            self._painter.drawRect(x, 1, w, self.height()-1)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)
        # Paint event triggered by resize
        self.setGeometry(QtCore.QRect(0, 0, self._parent.width(), self._parent.height()))

        self._painter.begin(self)
        for i in range(self.noctaves):
            for j in [0, 2, 4, 5, 7, 9, 11]:
                key = i * 12 + j
                self._draw_key(key, self.state[key])
        for i in range(self.noctaves):
            for j in [1, 3, 6, 8, 10]:
                key = i * 12 + j
                self._draw_key(key, self.state[key])

        self._painter.end()


class MidiViewerLive(MidiDeviceMenuParent):
    class MidiMonitor(Thread):
        def __init__(self, midi_in: rtmidi.MidiIn, device_id: int, callback):
            super().__init__()
            self._midi_in = midi_in
            self._device_id = device_id
            self._running = False
            self._callback = callback

        def stop(self, timeout=None):
            self._midi_in.close_port()
            self._running = False
            self.join(timeout=timeout)

        def run(self) -> None:
            self._running = True
            self._midi_in.open_port(self._device_id)
            while self._midi_in.is_port_open():
                msg = self._midi_in.get_message()
                if msg is None:
                    # 100Hz poll rate
                    sleep(0.01)
                    continue
                self._callback(msg[0])

    class MidiDeviceMenu(QMenu):
        def __init__(self, parent: MidiDeviceMenuParent):
            super().__init__('Input device: None', parent)
            self.mapping = QtCore.QSignalMapper(parent)
            self.mapping.mapped['int'].connect(parent.set_input_device)
            self.mapping.mapped['int'].connect(self._on_set_device)
            self._parent = parent
            self._current_device = -1

            if len(parent.get_input_devices()) > 0:
                self._on_set_device(0)
                parent.set_input_device(0)

        def _on_set_device(self, d_id):
            name = self._parent.get_input_devices()[d_id]
            self.setTitle('Input device: {}'.format(name))
            self._current_device = d_id

        def _refresh(self):
            self.clear()
            input_devices = self._parent.get_input_devices()
            if len(input_devices) == 0:
                a = QAction('No input devices detected!', self)
                a.setEnabled(False)
                self.addAction(a)
                return

            for i in range(len(input_devices)):
                name = input_devices[i]
                if i == self._current_device:
                    da = QAction(name + ' (active)', self)
                    da.setEnabled(False)
                else:
                    da = QAction(name, self)
                self.mapping.setMapping(da, i)
                da.triggered.connect(self.mapping.map)
                self.addAction(da)

        def showEvent(self, a0: QtGui.QShowEvent) -> None:
            self._refresh()
            super().showEvent(a0)

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 900, 150)
        self.setWindowTitle('MidiViewerLive')
        self._layout = QGridLayout()

        self._midiin = rtmidi.MidiIn()
        self._inputdevicesubmenu = None
        self._monitor = None
        self._midimenu = MidiViewerLive.MidiDeviceMenu(self)

        self._keyboard = KeyboardDisplay(self)

        self.menuBar().addMenu(self._midimenu)

        self._off_queue = []
        self._pedal_state = False

        self.show()

    def _on_midi(self, msg: [int]):
        self._keyboard.handle_midi(msg)

    def get_input_devices(self) -> [str]:
        return self._midiin.get_ports()

    def set_input_device(self, d_id):
        if self._monitor is not None:
            self._monitor.stop()
        self._monitor = MidiViewerLive.MidiMonitor(self._midiin, d_id, self._on_midi)
        self._monitor.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        if self._monitor is not None:
            self._monitor.stop()

def main(argv=None):
    app = QApplication([])
    mvl = MidiViewerLive()
    app.exec_()

if __name__ == '__main__':
    main()
