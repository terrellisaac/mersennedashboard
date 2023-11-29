from pyperclip import copy, paste
# External library for working directly with the operating system clipboard

class FactoringWork:
    def __init__(self, getWorkButton, reportWorkButton, getWorkMainDash, repWorkMainDash):
        # First two buttons passed are in the work management dialogs
        # Last two buttons passed are in the main dashboard
        self.GetButton = getWorkButton
        self.MainDashGet = getWorkMainDash
        self.MainDashRep = repWorkMainDash
        self.ReportButton = reportWorkButton

    def grabResults(self):
        resultsFile = open("./mfaktc/results.txt", "r")  # "Reading" mode to get the work results out
        completedWork = resultsFile.read()
        resultsFile.close()  # Can't write and read at the same time
        resultsFile = open("./mfaktc/results.txt", "w")  # "Writing" mode to blank the file
        resultsFile.close()  # Closing a file that was opened in writing mode without writing anything blanks it
        copy(completedWork)  # Pyperclip: Load what we read out into the clipboard
        self.ReportButton.setText("Current results copied to clipboard!")

    def loadWork(self):
        workFile = open("./mfaktc/worktodo.txt", "a")  # Open in "append" mode
        workFile.write("\n")
        workFile.write(paste())  # Call pyperclip's paste
        workFile.close()
        self.GetButton.setText("Work loaded!")