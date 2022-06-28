from PyQt6.QtWidgets import QGridLayout, QWidget, QPushButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
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

        self.longEmergencyButton.clicked.connect(self.longEmergencyButtonClicked)
        self.completeButton.clicked.connect(self.stopVideo)

    # render video on ready button click
    def renderVideo(self):
        self.player.setSource(QUrl.fromLocalFile(self.INFO["videoName"]))

    # start video on ready button click
    def startVideo(self):
        self.player.play()
        self.INFO["startTime"] = datetime.datetime.now()

    # eventually get rid of this
    def stopVideo(self):
        self.player.stop()

    def setCompleteButton(self, parentFunc):
        self.completeButton.clicked.connect(parentFunc)
    
    def longEmergencyButtonClicked(self):
        self.INFO["output"].append(datetime.datetime.now())