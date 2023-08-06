from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

__all__ = ['Qutie']

def handle_event(event):
    def handle_event(*args, **kwargs):
        if callable(event):
            event(*args, **kwargs)
    return handle_event

def to_brush(method):
    def to_brush(self, value):
        if value is None:
            brush = QtGui.QBrush()
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        return method(self, brush)
    return to_brush

def from_brush(method):
    def from_brush(self):
        value = method(self)
        if value is not None:
            return QtGui.QBrush(value).color().name()
        return None
    return from_brush

class QutieStub:

    QtClass = NotImplemented

    def __init__(self, qt=None):
        class QtClassWrapper(self.QtClass):

            def reflection(self):
                return self._reflection

            def setReflection(self, value):
                self._reflection = value

        if qt is None: qt = []
        if not isinstance(qt, (tuple, list)):
            qt=[qt]
        self.__qt = QtClassWrapper(*qt)
        self.qt.setReflection(self)

    @property
    def qt(self):
        return self.__qt

class Qutie:

    QtClass = NotImplemented

    def __init__(self, qt=None):
        class QtClassWrapper(self.QtClass):

            handleEvent = QtCore.pyqtSignal(object)

            def reflection(self):
                return self.property('__qutie_property')

            def setReflection(self, value):
                self.setProperty('__qutie_property', value)

        if qt is None: qt = []
        if not isinstance(qt, (tuple, list)):
            qt=[qt]
        self.__qt = QtClassWrapper(*qt)
        self.qt.setReflection(self)

    @property
    def qt(self):
        return self.__qt
