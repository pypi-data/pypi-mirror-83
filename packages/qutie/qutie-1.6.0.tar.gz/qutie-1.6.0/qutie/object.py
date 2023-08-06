from .qutie import QtCore
from .qutie import Qutie

__all__ = ['Object']

class Object(Qutie):

    QtClass = QtCore.QObject

    def __init__(self, *, object_name=None, parent=None, destroyed=None,
                 object_name_changed=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setReflection(self)
        # Properties
        if object_name is not None:
            self.object_name = object_name
        if parent is not None:
            self.parent = parent
        self.destroyed = destroyed
        self.object_name_changed = object_name_changed
        # Connect signals
        self.qt.destroyed.connect(self.__handle_destroyed)
        self.qt.objectNameChanged.connect(self.__handle_object_name_changed)
        self.qt.handleEvent.connect(lambda event: event())

    @property
    def object_name(self) -> str:
        return self.qt.objectName()

    @object_name.setter
    def object_name(self, value: str):
        self.qt.setObjectName(value)

    @property
    def parent(self):
        parent = self.qt.parent()
        if hasattr(parent, 'reflection'):
            return parent.reflection()

    @parent.setter
    def parent(self, value):
        assert isinstance(value, Object), "Parent must inherit from Object"
        self.qt.setParent(value.qt)

    @property
    def destroyed(self) -> object:
        return self.__destroyed

    @destroyed.setter
    def destroyed(self, value: object):
        self.__destroyed = value

    def __handle_destroyed(self, obj: object):
        if callable(self.destroyed):
            self.destroyed()

    @property
    def object_name_changed(self) -> object:
        return self.__object_name_changed

    @object_name_changed.setter
    def object_name_changed(self, value: object):
        self.__object_name_changed = value

    def __handle_object_name_changed(self):
        if callable(self.object_name_changed):
            self.object_name_changed(self.object_name)

    def emit(self, *args, **kwargs):
        """Emit an event.

        >>> o.event = lambda value: print(value) # assign event callback
        >>> o.emit('event', 42)
        """
        if not args:
            raise ValueError("Missing event argument.")
        event = args[0]
        if isinstance(event, str):
            if hasattr(self, event):
                event = getattr(self, event)
        if callable(event):
            self.qt.handleEvent.emit(lambda: event(*args[1:], **kwargs))
