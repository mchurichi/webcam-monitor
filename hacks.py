# -*- coding: utf-8 *-*
from PyQt4.QtCore import QObject, pyqtSignal, QEvent


def clickable(widget):
    '''
    Hace clickeable cualquier widget
    '''
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    self.clicked.emit()
                    return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
