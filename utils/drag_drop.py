from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QWidget

class DraggableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.objectName())
        drag.setMimeData(mime_data)
        
        drag.exec_(Qt.MoveAction)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        event.acceptProposedAction()

