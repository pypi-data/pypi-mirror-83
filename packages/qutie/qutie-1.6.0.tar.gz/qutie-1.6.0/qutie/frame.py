from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Frame']

class Frame(BaseWidget):

    QtClass = QtWidgets.QFrame

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
