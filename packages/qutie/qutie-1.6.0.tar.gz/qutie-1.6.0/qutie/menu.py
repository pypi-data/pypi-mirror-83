from .qutie import QtWidgets

from .action import Action
from .widget import BaseWidget

__all__ = ['Menu']

class Menu(BaseWidget):

    QtClass = QtWidgets.QMenu

    def __init__(self, *items, text=None, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)
        if text is not None:
            self.text = text

    @property
    def text(self):
        return self.qt.title()

    @text.setter
    def text(self, value):
        self.qt.setTitle(value)

    def append(self, item):
        if isinstance(item, str):
            item = Action(item)
        if isinstance(item, Action):
            self.qt.addAction(item.qt)
        elif isinstance(item, Menu):
            self.qt.addMenu(item.qt)
        else:
            raise ValueError(item)
        return item

    def insert(self, index, item):
        if index < 0:
            index = max(0, len(self) + index)
        if isinstance(item, str):
            item = Action(item)
        before = self[index].qt if len(self) else None
        if isinstance(item, Action):
            self.qt.insertAction(before, item.qt)
        elif isinstance(item, Menu):
            self.qt.insertMenu(before, item.qt)
        else:
            raise ValueError(item)
        return item

    def index(self, item):
        return self.qt.actions().index(item.qt)

    def _get_action_or_menu(self, action):
        if hasattr(action, 'reflection'):
            return action.reflection()
        return action.menu().reflection()

    def __getitem__(self, index):
        action = self.qt.actions()[index]
        return self._get_action_or_menu(action)

    def __iter__(self):
        return iter(self._get_action_or_menu(action) for action in self.qt.actions())

    def __len__(self):
        return len(self.qt.actions())
