from PyQt6.QtWidgets import QGridLayout, QWidget, QPushButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
from PyQt5.QtCore import Qt, QTimer, QThread
import datetime

'''
Displays the video and two/one buttons to press depending on the selected scenario
When video starts, store the OS time as INFO["startTime] for later processing
Upon button press record the time, store time in INFO["output"]
'''
class ExperimentWindow(QWidget):
    def __init__(self, INFO):
        super().__init__()

        self.INFO = INFO
        self.timestamps = []
        self.timestampsLength = len(self.INFO["timestamps"])
        for i in range(self.timestampsLength):
            self.timestamps.append(int(float(self.INFO["timestamps"][i]) * 1000))
        
        self.currTimestamp = 1

        layout = QGridLayout()
        self.longEmergencyButton = QPushButton("Emergency")
        self.completeButton = QPushButton("Complete")
        
        self.player = QMediaPlayer()
        self.video = QVideoWidget()
        self.player.setVideoOutput(self.video)
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.video.show()

        layout.addWidget(self.video, 0, 0, 2, 4)
        layout.addWidget(self.longEmergencyButton, 2, 1, 1, 2)
        layout.addWidget(self.completeButton, 3, 1, 1, 2)
        layout.addWidget(QWidget(), 0, 3)
        layout.addWidget(QWidget(), 3, 0)
        self.setLayout(layout)

        self.videoTimer = QTimer()
        #self.promptTimer = QTimer()
        #self.promptTimer.setTimerType(Qt.PreciseTimer)
        #self.buttonTimer = QTimer()
        #self.buttonTimer.setInterval(5000)
        
        self.videoTimer.timeout.connect(self.videoEnded)
        #self.promptTimer.timeout.connect(self.promptReached)
        #self.buttonTimer.timeout.connect(self.buttonLimitReached)

        self.longEmergencyButton.clicked.connect(self.longEmergencyButtonClicked)

        self.thread = QThread()
        self.videoTimer.moveToThread(self.thread)
        self.thread.start()

    # render video on ready button click
    def renderVideo(self):
        self.player.setSource(QUrl.fromLocalFile(self.INFO["videoName"]))
        self.video.setHidden(False)
        self.completeButton.setHidden(True)
        self.longEmergencyButton.setHidden(True)
        self.videoTimer.start(self.player.duration())

    # start video on ready button click
    def startVideo(self):
        self.player.play()
        self.INFO["startTime"] = datetime.datetime.now()
        #self.promptTimer.start(self.timestamps[0])

    def setCompleteButton(self, parentFunc):
        self.completeButton.clicked.connect(parentFunc)
    
    def longEmergencyButtonClicked(self):
        self.INFO["output"].append(datetime.datetime.now())
        #self.buttonTimer.stop()
        self.longEmergencyButton.setHidden(True)

    def videoEnded(self):
        self.player.stop()
        self.video.setHidden(True)
        self.longEmergencyButton.setHidden(True)
        self.videoTimer.stop()
        #self.promptTimer.stop()
        #self.buttonTimer.stop()
        self.completeButton.setHidden(False)
        self.currTimestamp = 1

    def promptReached(self):
        self.longEmergencyButton.setHidden(False)
        #self.buttonTimer.start()
        #if (self.currTimestamp < self.timestampsLength):
        #    self.promptTimer.start(self.timestamps[self.currTimestamp])
        #    self.currTimestamp += 1
        #else:
        #    self.promptTimer.stop()
    
    def buttonLimitReached(self):
        self.INFO["output"].append(datetime.datetime.now())
        #self.buttonTimer.stop()
        self.longEmergencyButton.setHidden(True)