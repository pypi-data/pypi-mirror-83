from .qutie import QtGui
from .qutie import QtWidgets

from .object import Object
from .icon import Icon

__all__ = ['Action']

class Action(Object):

    QtClass = QtWidgets.QAction

    def __init__(self, text=None, *, checkable=None, checked=False, tool_tip=None,
                 status_tip=None, shortcut=None, icon=None, separator=None,
                 triggered=None, toggled=None, **kwargs):
        super().__init__(**kwargs)
        # Create separator from text
        if isinstance(text, str) and text.startswith("---"):
            text = None
            separator = True
        if text is not None:
            self.text = text
        if checkable is not None:
            self.checkable = checkable
        self.checked = checked
        if tool_tip is not None:
            self.tool_tip = tool_tip
        if status_tip is not None:
            self.status_tip = status_tip
        if shortcut is not None:
            self.shortcut = shortcut
        if icon is not None:
            self.icon = icon
        if separator is not None:
            self.separator = separator
        self.triggered = triggered
        self.toggled = toggled
        # Connect signals
        self.qt.triggered.connect(self.__handle_triggered)
        self.qt.toggled.connect(self.__handle_toggled)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

    @property
    def checked(self):
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value):
        self.qt.setChecked(value)

    @property
    def checkable(self):
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value):
        self.qt.setCheckable(value)

    @property
    def tool_tip(self):
        return self.qt.toolTip()

    @tool_tip.setter
    def tool_tip(self, value):
        self.qt.setToolTip(value)

    @property
    def status_tip(self):
        return self.qt.statusTip()

    @status_tip.setter
    def status_tip(self, value):
        self.qt.setStatusTip(value)

    @property
    def shortcut(self):
        return self.qt.shortcut().toString() or None

    @shortcut.setter
    def shortcut(self, value):
        if value is None:
            self.qt.setShortcut(QtGui.QKeySequence())
        else:
            self.qt.setShortcut(QtGui.QKeySequence(value))

    @property
    def icon(self):
        icon = self.qt.icon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setIcon(value.qt)

    @property
    def separator(self):
        return self.qt.isSeparator()

    @separator.setter
    def separator(self, value):
        self.qt.setSeparator(value)

    @property
    def triggered(self):
        return self.__triggered

    @triggered.setter
    def triggered(self, value):
        self.__triggered = value

    def __handle_triggered(self):
        if callable(self.triggered):
            self.triggered()

    @property
    def toggled(self):
        return self.__toggled

    @toggled.setter
    def toggled(self, value):
        self.__toggled = value

    def __handle_toggled(self, checked):
        if callable(self.toggled):
            self.toggled(checked)

    def trigger(self):
        self.qt.trigger()

    def toggle(self):
        self.qt.toggle()
