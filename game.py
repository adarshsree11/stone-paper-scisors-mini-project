# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
#2104196
#27784901
#31929231
#31993041
#1793624
from PyQt5 import QtCore, QtGui, QtWidgets

from keras.models import load_model
import cv2
import numpy as npy
from random import choice
import time
from playsound import playsound
from threading import *
import time
import pygame

from ai import *

class Ui_MainWindow(object):

    webcam = False
    #move = ""

    mapper = {
        0: "rock",
        1: "paper",
        2: "scissors",
        3: "none"
    }

    user_move_name = ""

    CompMove_points = []

    model = load_model("rock-paper-scissors-model.h5")

    cap = cv2.VideoCapture(0)


    cap.set(3,1280)
    cap.set(4,720)


    def displayUserScreen(self):

        count = 0
        self.sound()
        while self.webcam:
            print(count)
            count = count+1
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame,1)
            # rectangle for user to play
            cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "Your Move Here: ",
                        (90, 90), font, 1.5, (255, 255, 255), 4, cv2.LINE_AA)
            self.displayImage(frame,1)
            if count == 35:
                self.predict()
                self.sound()
                count = 0
                #time.sleep(1)
            k = cv2.waitKey()

        #self.cap.release()
        #cv2.destroyAllWindows()


    def displayImage(self,img,window = 1):
        qformat = QtGui.QImage.Format_Indexed8
        print("test display image")
        if img.shape[2] ==3:
            if img.shape[2] ==4:
                qformat = QtGui.QImage.Format_RGBA888
            else:
                qformat = QtGui.QImage.Format_RGB888

        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.lblImage.setPixmap(QtGui.QPixmap.fromImage(img))
        self.lblImage.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
    def toggleEvent(self):
        if self.webcam :
            self.webcam = False
            self.btnToggle.setStyleSheet("border: 3px solid  #009900;""background-color:#152c02;""border-radius: 10px;""color: #009900;")
            _translate = QtCore.QCoreApplication.translate
            self.btnToggle.setText(_translate("MainWindow", "Start"))
        else:
            self.webcam = True
            self.btnToggle.setStyleSheet("border: 3px solid  #a40000;""background-color:#390404;""border-radius: 10px;""color:  #a40000;")
            _translate = QtCore.QCoreApplication.translate
            self.btnToggle.setText(_translate("MainWindow", "Stop"))
            self.displayUserScreen()
    
    def predict(self):
        logic = True
        print("test predict")
        while logic:

            print("test predict while")

            #playsound('audio_stone_paper_scissors.mp3')

            ret, frame = self.cap.read()
            if not ret:
                continue

            print("in predict-----------------")
            frame = cv2.flip(frame,1)

            # rectangle for user to play
            cv2.rectangle(frame, (100, 100), (200, 600), (255, 255, 255), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "Your Move Here: ",
                    (90, 90), font, 1.5, (255, 255, 255), 4, cv2.LINE_AA)

            roi = frame[100:500, 100:500]
            img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (227, 227))

            # predict the move made
            pred = self.model.predict(npy.array([img]))
            
            move_code = npy.argmax(pred[0])
            
            print(move_code)
            #return move_code
            self.user_move_name = self.mapper[move_code]
            print("predicted....{}".format(self.user_move_name))
            logic = False
            #self.displayImage(frame,1)

            if move_code != 3:
                self.displayResult(self.user_move_name)
                self.getCompMove(move_code)
                self.displayCompMove()
                self.displayPoints()
            else:
                self.displayResult(self.user_move_name)
                self.lblCompOutput.setText("Couldn't\nrecognise\nyour Move..\nPlay again..")
            #time.sleep(.3)

    def displayResult(self, msg):
        self.lblUserChoice.setText(msg)

    def displaytimer(self):
        for n in range(1,4):
            n = str(n)
            print(n)
            self.lblUserChoice.setText(n)
            time.sleep(2)

    def sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("audio_stone_paper_scissors.mp3")
        pygame.mixer.music.play()
    
    def getCompMove(self, user_move):
        if self.rbAi.isChecked():
            self.label.setStyleSheet("background-color: #121212;""color: #fcba03")
            self.CompMove_points = compMoveAi(user_move)
            print(self.CompMove_points)
        else:
            self.label.setStyleSheet("background-color: #121212;""color: #75d3ff")
            self.CompMove_points = compMoveRandom(user_move)
            print(self.CompMove_points)

    def displayCompMove(self):
        if self.CompMove_points[0] == 0:
            self.lblCompOutput.setPixmap(QtGui.QPixmap(":/newPrefix/images/rock.png"))
        elif self.CompMove_points[0] == 1:
            self.lblCompOutput.setPixmap(QtGui.QPixmap(":/newPrefix/images/paper.png"))
        elif self.CompMove_points[0] == 2:
            self.lblCompOutput.setPixmap(QtGui.QPixmap(":/newPrefix/images/scissors.png"))

    def displayPoints(self):
        self.lblCompScore.setText(str(self.CompMove_points[1][0]))
        self.lblUserScore.setText(str(self.CompMove_points[1][1]))
        self.label_2.setText(str(self.CompMove_points[1][3]))
        self.lblWinner.setText("Winner\n\n" + self.CompMove_points[2])
        self.checkGameOver()

    def reset_display(self):
        reset_points()
        self.lblCompScore.setText("0")
        self.lblUserScore.setText("0")
        self.label_2.setText("00")

    def checkGameOver(self):
        if self.CompMove_points[1][0] == 10:
            self.lblFinal.setText("Winner : Computer")
            self.lblCompFinal.setText(str(self.CompMove_points[1][0]))
            self.lblUserFinal.setText(str(self.CompMove_points[1][1]))
            self.webcam = False
            self.showCelebration()
        elif self.CompMove_points[1][1] == 10:
            self.lblFinal.setText("Winner : User")
            self.lblCompFinal.setText(str(self.CompMove_points[1][0]))
            self.lblUserFinal.setText(str(self.CompMove_points[1][1]))
            self.webcam = False
            self.showCelebration()

    def showCelebration(self):
        self.lblCelebration.setGeometry(QtCore.QRect(0, 0, 1920, 1015))
        self.btnNewgame.setGeometry(QtCore.QRect(710, 700, 491, 111))
        self.lblFinal.setGeometry(QtCore.QRect(480, 530, 961, 131))
        self.lblCompFinal.setGeometry(QtCore.QRect(1100, 320, 201, 171))
        self.lblUserFinal.setGeometry(QtCore.QRect(590, 320, 201, 171))

    def playAgain(self):
        self.reset_display()
        self.btnToggle.setStyleSheet("border: 3px solid  #009900;""background-color:#152c02;""border-radius: 10px;""color: #009900;")
        _translate = QtCore.QCoreApplication.translate
        self.btnToggle.setText(_translate("MainWindow", "Start"))
        self.lblCelebration.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.btnNewgame.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.lblFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.lblCompFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.lblUserFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1057)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rbAi = QtWidgets.QRadioButton(self.centralwidget)
        self.rbAi.setGeometry(QtCore.QRect(1710, 130, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.rbAi.setFont(font)
        self.rbAi.setStyleSheet("transform : scale(10);")
        self.rbAi.setText("")
        self.rbAi.setObjectName("rbAi")
        self.lblUserScore = QtWidgets.QLabel(self.centralwidget)
        self.lblUserScore.setGeometry(QtCore.QRect(810, 410, 121, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.lblUserScore.setFont(font)
        self.lblUserScore.setStyleSheet("color: rgb(255, 217, 0);")
        self.lblUserScore.setAlignment(QtCore.Qt.AlignCenter)
        self.lblUserScore.setObjectName("lblUserScore")
        self.lblCompScore = QtWidgets.QLabel(self.centralwidget)
        self.lblCompScore.setGeometry(QtCore.QRect(940, 700, 131, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.lblCompScore.setFont(font)
        self.lblCompScore.setStyleSheet("color: rgb(255, 217, 0);")
        self.lblCompScore.setAlignment(QtCore.Qt.AlignCenter)
        self.lblCompScore.setObjectName("lblCompScore")
        self.btnToggle = QtWidgets.QPushButton(self.centralwidget)
        self.btnToggle.setGeometry(QtCore.QRect(80, 350, 161, 161))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(34)
        font.setBold(True)
        font.setWeight(75)
        self.btnToggle.setFont(font)
        self.btnToggle.setAutoFillBackground(False)
        self.btnToggle.setStyleSheet("border: 3px solid  #009900; \n"
"background-color: #152c02;\n"
"border-radius: 10px;\n"
"color: #009900;\n"
"opacity: 8;")
        self.btnToggle.setFlat(True)
        self.btnToggle.setObjectName("btnToggle")
        self.lblbackground = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(72)
        self.lblbackground = QtWidgets.QLabel(self.centralwidget)
        self.lblbackground.setGeometry(QtCore.QRect(0, 0, 1920, 1015))
        self.lblbackground.setText("")
        self.lblbackground.setScaledContents(True)
        self.lblbackground.setObjectName("lblbackground")
        movie = QtGui.QMovie("background.gif")
        self.lblbackground.setMovie(movie)
        movie.start()
        self.lblImage = QtWidgets.QLabel(self.centralwidget)
        self.lblImage.setGeometry(QtCore.QRect(324, 375, 421, 491))
        self.lblImage.setText("")
        self.lblImage.setScaledContents(True)
        self.lblImage.setObjectName("lblImage")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1664, 725, 141, 131))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(84, 218, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lblUserChoice = QtWidgets.QLabel(self.centralwidget)
        self.lblUserChoice.setGeometry(QtCore.QRect(490, 720, 321, 61))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.lblUserChoice.setFont(font)
        self.lblUserChoice.setStyleSheet("color: rgb(203, 251, 255);")
        self.lblUserChoice.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblUserChoice.setObjectName("lblUserChoice")
        self.lblCompOutput = QtWidgets.QLabel(self.centralwidget)
        self.lblCompOutput.setGeometry(QtCore.QRect(1140, 360, 421, 511))
        self.lblCompOutput.setStyleSheet("color: #75d3ff;")
        font.setPointSize(24)
        self.lblCompOutput.setFont(font)
        self.lblCompOutput.setText("")
        #self.lblCompOutput.setPixmap(QtGui.QPixmap(":/newPrefix/images/paper.png"))
        self.lblCompOutput.setScaledContents(True)
        self.lblCompOutput.setObjectName("lblCompOutput")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1580, 60, 131, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: #121212;\n"
"border-radius: 10px;\n"
"color: #75d3ff;\n"
"opacity: 8;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btnReset = QtWidgets.QPushButton(self.centralwidget)
        self.btnReset.setGeometry(QtCore.QRect(80, 531, 161, 161))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.btnReset.setFont(font)
        self.btnReset.setAutoFillBackground(False)
        self.btnReset.setStyleSheet("border: 3px solid #75d3ff;\n"
"background-color: #072363;\n"
"border-radius: 10px;\n"
"transform: rotate(90);\n"
"color: #75d3ff;\n"
"opacity: 8;")
        self.btnReset.setFlat(True)
        self.btnReset.setObjectName("btnReset")
        self.lblWinner = QtWidgets.QLabel(self.centralwidget)
        self.lblWinner.setGeometry(QtCore.QRect(1640, 270, 151, 151))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblWinner.setFont(font)
        self.lblWinner.setStyleSheet("border: 3px solid  rgb(243, 224, 13); \n"
"background-color: #000;\n"
"border-radius: 10px;\n"
"transform: rotate(90);\n"
"color: rgb(243, 224, 13);\n"
"opacity: 8;")
        self.lblWinner.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblWinner.setObjectName("lblWinner")
        self.lblCelebration = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(72)
        self.lblCelebration = QtWidgets.QLabel(self.centralwidget)
        self.lblCelebration.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.lblCelebration.setText("")
        self.lblCelebration.setScaledContents(True)
        self.lblCelebration.setObjectName("lblCelebration")
        movie = QtGui.QMovie("celebration.gif")
        self.lblCelebration.setMovie(movie)
        movie.start()
        self.btnNewgame = QtWidgets.QPushButton(self.centralwidget)
        self.btnNewgame.setGeometry(QtCore.QRect(0, 0, 0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(44)
        font.setBold(True)
        font.setWeight(75)
        self.btnNewgame.setFont(font)
        self.btnNewgame.setStyleSheet("border: 6px solid #072363;\n"
"background-color: #75d3ff;\n"
"border-radius: 55px;\n"
"transform: rotate(90);\n"
"color: #072363;\n"
"opacity: 8;")
        self.btnNewgame.setObjectName("btnNewgame")
        self.lblFinal = QtWidgets.QLabel(self.centralwidget)
        self.lblFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.lblFinal.setFont(font)
        self.lblFinal.setStyleSheet("border: 3px solid  rgb(243, 224, 13); \n"
"background-color: #000;\n"
"border-radius: 10px;\n"
"transform: rotate(90);\n"
"color: rgb(243, 224, 13);\n"
"opacity: 8;")
        self.lblFinal.setObjectName("lblFinal")
        self.lblCompFinal = QtWidgets.QLabel(self.centralwidget)
        self.lblCompFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(90)
        font.setBold(True)
        font.setWeight(75)
        self.lblCompFinal.setFont(font)
        self.lblCompFinal.setStyleSheet("color: #75d3ff;\n"
"background-color: rgb(5, 44, 103);\n"
"border-radius: 20px;")
        self.lblCompFinal.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblCompFinal.setObjectName("lblCompFinal")
        self.lblUserFinal = QtWidgets.QLabel(self.centralwidget)
        self.lblUserFinal.setGeometry(QtCore.QRect(0, 0, 0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(90)
        font.setBold(True)
        font.setWeight(75)
        self.lblUserFinal.setFont(font)
        self.lblUserFinal.setStyleSheet("color: #75d3ff;\n"
"background-color: rgb(5, 44, 103);\n"
"border-radius: 20px;")
        self.lblUserFinal.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblUserFinal.setObjectName("lblUserFinal")
        self.lblbackground.raise_()
        self.rbAi.raise_()
        self.lblUserScore.raise_()
        self.lblCompScore.raise_()
        self.btnToggle.raise_()
        self.lblImage.raise_()
        self.label_2.raise_()
        self.lblUserChoice.raise_()
        self.lblCompOutput.raise_()
        self.label.raise_()
        self.btnReset.raise_()
        self.lblWinner.raise_()
        self.lblCelebration.raise_()
        self.btnNewgame.raise_()
        self.lblFinal.raise_()
        self.lblCompFinal.raise_()
        self.lblUserFinal.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.lblUserChoice.setText(self.user_move)
        self.btnToggle.clicked.connect(self.toggleEvent)
        self.btnReset.clicked.connect(self.reset_display)
        self.btnNewgame.clicked.connect(self.playAgain)
        #self.aboutToQuit.connect(self.closeEvent)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rock Paper Scissors 1.0"))
        self.lblUserScore.setText(_translate("MainWindow", "0"))
        self.lblCompScore.setText(_translate("MainWindow", "0"))
        self.btnToggle.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow", "00"))
        self.lblUserChoice.setText(_translate("MainWindow", "none"))
        self.label.setText(_translate("MainWindow", "Ai"))
        self.btnReset.setText(_translate("MainWindow", "Reset"))
        self.lblWinner.setText(_translate("MainWindow", "Winner"))
        self.btnNewgame.setText(_translate("MainWindow", "Play Again"))
        self.lblFinal.setText(_translate("MainWindow", "Winner : Computer"))
        self.lblCompFinal.setText(_translate("MainWindow", "00"))
        self.lblUserFinal.setText(_translate("MainWindow", "00"))

import comp_choice_rc
import newbg_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(1920,1080)
    MainWindow.showMaximized()
    #app.aboutToQuit.connect(ui.closeEvent)
    #time.sleep(10)
    sys.exit(app.exec_())
