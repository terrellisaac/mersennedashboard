from PyQt6.QtWidgets import QPushButton, QLabel
import subprocess
import signal

class StartButton:
    def __init__(self, pgmName, programDir):
        self.program = pgmName  # Name of the program this button will start
        self.directory = programDir  # String with the file path of the exe we want this button to run
        lbl = ("Start " + pgmName)  # What the button label will say
        statusLbl = (pgmName + " is not running")
        self.buttonObject = QPushButton(lbl)  # Create the PyQt button object
        self.statusObject = QLabel(statusLbl)  # A complementary Qt widget for displaying the status
        self.pgmRunning = False
        self.processID = None  # subprocess's Popen function returns a PID

    def ClickedMe(self):
        if not self.pgmRunning:
            self.processID = subprocess.Popen(self.directory)  # Run the exe at the file path that was captured in the init
            self.buttonObject.setText("Stop " + self.program)
            self.statusObject.setText(self.program + " is running")  # Change the button's label and the program status
            self.pgmRunning = True
        else:
            self.processID.send_signal(signal.SIGTERM)  # A "soft" terminate signal that allows the program to clean up
            self.buttonObject.setText("Start " + self.program)
            self.statusObject.setText(self.program + " is not running")
            self.pgmRunning = False
