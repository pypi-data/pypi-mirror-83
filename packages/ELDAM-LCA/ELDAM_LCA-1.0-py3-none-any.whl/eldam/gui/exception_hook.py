""" Adapted from http://timlehr.com/python-exception-hooks-with-qt-message-box/ """

import sys
import traceback
from PyQt5 import QtCore, QtWidgets

from eldam.gui.dialogs import ResizableMessageBox

from eldam.utils.gui import remove_path_from_error_message

from eldam.settings import DEBUG


def show_exception_box(error):
    if QtWidgets.QApplication.instance() is not None:
        error_message, detailed_message = error
        errorbox = ResizableMessageBox()
        errorbox.setText("An unexpected error occurred:\n\n" + error_message)
        errorbox.setDetailedText(detailed_message)
        errorbox.setWindowTitle("Error")
        errorbox.exec()


class UncaughtHook(QtCore.QObject):
    _exception_caught = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            error_message = '{0}: {1}'.format(exc_type.__name__, exc_value)
            detailed_message = '\n'.join([''.join(traceback.format_tb(exc_traceback)), error_message])

            # Removing path from message
            detailed_message = remove_path_from_error_message(detailed_message)

            # trigger message box show
            self._exception_caught.emit((error_message, detailed_message))


# create a global instance of our class to register the hook
if not DEBUG:  # If DEBUG is True, the exception will be raised in the standard output and the program will crash
    qt_exception_hook = UncaughtHook()
