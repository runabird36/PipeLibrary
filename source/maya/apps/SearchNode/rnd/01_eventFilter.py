from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QObject, QEvent

class EventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            print("Mouse button pressed")
        elif event.type() == QEvent.KeyPress:
            print("Key pressed")
        
        # Let the event pass through to the object
        return False

# Create a custom widget
class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Install the event filter on the widget
        self.event_filter = EventFilter()
        self.installEventFilter(self.event_filter)

# Create the application
# app = QApplication([])
widget = CustomWidget()
widget.show()
# app.exec_()