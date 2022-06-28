from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from experiment_window import ExperimentWindow
from info_window import InfoWindow
from final_window import FinalWindow
import csv
import datetime

# create a separate Qwidget class to house all windows
class WindowManager(QWidget):
    def __init__(self):
        super().__init__()

        self.INFO = {
            "output": [],
            "startTime": datetime.datetime.now(),
            "outputName": "",
            "videoName": "",
            "timestamps": []
        }
        self.initializeINFO()

        layout = QGridLayout()

        # add all windows as class variables to use the window variables
        self.InfoWindow = InfoWindow(self.INFO)
        self.ExperimentWindow = ExperimentWindow(self.INFO)
        self.FinalWindow = FinalWindow(self.INFO)

        layout.addWidget(self.InfoWindow)
        layout.addWidget(self.ExperimentWindow)
        layout.addWidget(self.FinalWindow)
        self.ExperimentWindow.setHidden(True)
        self.FinalWindow.setHidden(True)
        self.setLayout(layout)

        # connect transition buttons to functions in WindowManager
        self.InfoWindow.setReadyButton(self.readyButtonClicked)
        self.InfoWindow.setReadyButton(self.ExperimentWindow.renderVideo)
        self.InfoWindow.setReadyButton(self.ExperimentWindow.startVideo)
        self.ExperimentWindow.setCompleteButton(self.completeButtonClicked)
        self.ExperimentWindow.setCompleteButton(self.FinalWindow.flushToCSV)
        self.FinalWindow.setReturnToStartButton(self.returnToStartButtonClicked)

    def initializeINFO(self):
        with open("fileNames.csv", newline='') as fileName:
            reader = csv.reader(fileName)
            for row in reader:
                self.INFO["videoName"] = row[0]
                self.INFO["outputName"] = row[1]
                with open(row[2], newline='') as controlTimes:
                    reader = csv.reader(controlTimes)
                    for i in reader:
                        self.INFO["timestamps"] = i

    def readyButtonClicked(self):
        self.InfoWindow.setHidden(True)
        self.ExperimentWindow.setHidden(False)
    
    def completeButtonClicked(self):
        self.ExperimentWindow.setHidden(True)
        self.FinalWindow.setHidden(False)

    def returnToStartButtonClicked(self):
        self.FinalWindow.setHidden(True)
        self.InfoWindow.setHidden(False)
        self.INFO["output"].clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Autonomous Driving Experiment")
        
        self.WindowManager = WindowManager()
        self.setCentralWidget(self.WindowManager)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()