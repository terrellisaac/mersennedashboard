import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QDialog, QVBoxLayout
from ProgramStarter import StartButton  # See ProgramStarter.py for more details
from FactoringWorkHandler import FactoringWork  # See FactoringWorkHandler.py for more details


dashboard = QApplication([])  # The fundamental PyQt object. We build it iteratively
p95Button = StartButton("prime95", "./prime95/prime95.exe")  # The user will be told to put prime95 here
p95Button.buttonObject.clicked.connect(p95Button.ClickedMe)  # Link a PyQt button to a function definition
mfaktcButton = StartButton("mfaktc", "./mfaktc/mfaktc.exe")
mfaktcButton.buttonObject.clicked.connect(mfaktcButton.ClickedMe)
MainDash = QWidget()  # The main application window
MainDash.setWindowTitle("Mersenne Dashboard")


# This block of code builds and displays the application's welcome popup
startPopup = QDialog(parent=MainDash)  # This window will return control to the main dashboard when closed
startupLayout = QVBoxLayout()  # Vertical box layout. Widgets stack on top of one another
startupText = "You must already have prime95 and mfaktc installed for this dashboard to work!"
p95LinkText = "prime95 can be downloaded <a href=https://www.mersenne.org/download>here</a>"  # PyQt parses HTML
mfaktcLinkText = "mfaktc can be downloaded <a href=https://download.mersenne.ca/mfaktc/mfaktc-0.21>here</a>"
dirWarning = 'Your prime95 and mfaktc folders should be in the same directory as this dashboard, and should be named "prime95" and "mfaktc"'
pgmNameWarning = 'Your prime95 and mfaktc executables themselves should also be named "prime95" and "mfaktc"'
startupProceed = "Close this dialog to continue"
p95Link = QLabel(p95LinkText)
mfaktcLink = QLabel(mfaktcLinkText)
p95Link.setOpenExternalLinks(True)
# PyQt can open hyperlinks in the browser, but this must be enabled manually for EACH label with a link in it
mfaktcLink.setOpenExternalLinks(True)
startupLayout.addWidget(QLabel(startupText))
startupLayout.addWidget(p95Link)  # With QVBoxLayout, new widgets are automatically added under older ones
startupLayout.addWidget(mfaktcLink)
startupLayout.addWidget(QLabel(dirWarning))
startupLayout.addWidget(QLabel(pgmNameWarning))
startupLayout.addWidget(QLabel(startupProceed))
startPopup.setLayout(startupLayout)  # Load the QDialog object with the layout we've been building
startPopup.setWindowTitle("Welcome")
startPopup.exec()
# When a QDialog window is called with exec, closing it returns control to the parent window automatically


# Creates a FactoringWork instance to call our work management methods with, and stores some buttons we need in it
loadWorkButton = QPushButton("Load new work")
workReporter = QPushButton("Collect completed work")
mainDashGetWork = QPushButton("Get factoring work")
mainDashReportWork = QPushButton("Report factoring results")
workHandlerInstance = FactoringWork(loadWorkButton, workReporter, mainDashGetWork, mainDashReportWork)
# I couldn't get PyQt's connect() method to work with button objects instantiated in the same file.
# Storing the buttons I need in the FactoringWork object instead is a slightly hacky workaround
workHandlerInstance.GetButton.clicked.connect(workHandlerInstance.loadWork)
workHandlerInstance.ReportButton.clicked.connect(workHandlerInstance.grabResults)


# This code block builds the dialog that pops up when the user clicks "get work" in the main dashboard.
# See the comments in the code for the startup dialog for more details
getFactoringPopup = QDialog(parent=MainDash)
getFactoringPopup.setWindowTitle("Get work for mfaktc")
workLoaderLayout = QVBoxLayout()
getWorkText = "Get some factoring work for mfaktc. A mersenne.org account is required."
workInstructionsText1 = "Click <a href=https://www.mersenne.org/manual_gpu_assignment>here</a> to go to the factoring work page."
workInstructionsText2 = "Complete the form, then copy the work lines to your clipboard (Ctrl+C) and return to this program."
workInstructionsText3 = "Click the button below to load your new assignments into mfaktc's work file."
workInstructionsText4 = "When you are finished loading work, close this window to return to the main dashboard."
workLoaderLayout.addWidget(QLabel(getWorkText))
workPageLink = QLabel(workInstructionsText1)
workPageLink.setOpenExternalLinks(True)
workLoaderLayout.addWidget(workPageLink)
workLoaderLayout.addWidget(QLabel(workInstructionsText2))
workLoaderLayout.addWidget(QLabel(workInstructionsText3))
workLoaderLayout.addWidget(workHandlerInstance.GetButton)
workLoaderLayout.addWidget(QLabel(workInstructionsText4))
getFactoringPopup.setLayout(workLoaderLayout)


# This code block builds the pop-up dialog for reporting completed work.
# See the comments in the code for the startup dialog for more details
reportFactoringPopup = QDialog(parent=MainDash)
reportFactoringPopup.setWindowTitle("Submit completed mfaktc work")
workReporterLayout = QVBoxLayout()
returnResultsText = "Return factoring work you completed to mersenne.org."
resultInstructions1 = "Click the button below to clear mfaktc's results file and copy the current unreported results into your clipboard."
resultInstructions2 = "Click <a href=https://www.mersenne.org/manual_result>here</a> to go to the work submission page."
resultInstructions3 = 'Paste your mfaktc results into the text box (Ctrl+V), then click the "Submit" button.'
exitResultsInstruction = "Close this dialog when done to return to the main dashboard."
workReporterLayout.addWidget(QLabel(returnResultsText))
workReporterLayout.addWidget(QLabel(resultInstructions1))
workReporterLayout.addWidget(workHandlerInstance.ReportButton)
ReportWorkLink = QLabel(resultInstructions2)
ReportWorkLink.setOpenExternalLinks(True)
workReporterLayout.addWidget(ReportWorkLink)
workReporterLayout.addWidget(QLabel(resultInstructions3))
workReporterLayout.addWidget(QLabel(exitResultsInstruction))
reportFactoringPopup.setLayout(workReporterLayout)


# These functions pop up the work get and work report dialogs when the corresponding buttons are pressed from the main dash
def startWorkGet():
    workHandlerInstance.GetButton.setText("Load new work")
    # In the work handler class, this button's label changes to indicate a success.
    # We need to set it back when the dialog is opened again
    getFactoringPopup.exec()

def startWorkReport():
    workHandlerInstance.ReportButton.setText("Collect completed work")
    reportFactoringPopup.exec()
    # Again, calling exec() automatically returns control when the dialog box is closed

workHandlerInstance.MainDashGet.clicked.connect(startWorkGet)
# Hook up the work management buttons in the main dashboard
workHandlerInstance.MainDashRep.clicked.connect(startWorkReport)


# After taking care of all popup window definitions, we're ready to build the main window
layout = QGridLayout()
# Configurable grid layout. Widgets are passed with coordinates
mfaktcWorkWarning1 = "mfaktc will quit out immediately if you try to start it without any work in the file."
mfaktcWorkWarning2 = 'Remember to click the "Get factoring work" button and fetch some work for mfaktc to do.'
layout.addWidget(mfaktcButton.buttonObject, 0, 0)
layout.addWidget(mfaktcButton.statusObject, 0, 1)
layout.addWidget(p95Button.buttonObject, 3, 0)
layout.addWidget(p95Button.statusObject, 3, 1)
layout.addWidget(workHandlerInstance.MainDashGet, 4, 0)
layout.addWidget(workHandlerInstance.MainDashRep, 5, 0)
layout.addWidget(QLabel(mfaktcWorkWarning1), 1, 0)
layout.addWidget(QLabel(mfaktcWorkWarning2), 2, 0)
# Load the main window layout and display it
MainDash.setLayout(layout)
MainDash.show()


sys.exit(dashboard.exec())
# The outer call to sys.exit kills the Python application when the user closes the main window
