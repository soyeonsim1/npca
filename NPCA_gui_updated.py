# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NPCA.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTextBrowser, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(648, 600)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: beige;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(30, 0, 571, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.title = QLabel(self.horizontalLayoutWidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setFamilies([u"Georgia"])
        font.setPointSize(18)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setFrameShape(QFrame.NoFrame)
        self.title.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.title)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(0, -10, 661, 571))
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setStyleSheet(u"QFrame {\n"
"Background-color: Beige;\n"
"}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.progressBar = QProgressBar(self.frame_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(140, 520, 341, 20))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"    width: 20px;\n"
"}")
        self.progressBar.setValue(24)
        self.frame = QFrame(self.frame_4)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(50, 170, 551, 50))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget_2 = QWidget(self.frame)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 10, 531, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.checkBox = QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(50, 220, 551, 41))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 10, 61, 16))
        self.label_6.setFont(font1)
        self.checkBox_3 = QCheckBox(self.frame_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(80, 10, 87, 20))
        self.checkBox_3.setChecked(True)
        self.checkBox_4 = QCheckBox(self.frame_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setGeometry(QRect(180, 10, 87, 20))
        self.checkBox_4.setChecked(True)
        self.checkBox_5 = QCheckBox(self.frame_3)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setGeometry(QRect(290, 10, 87, 20))
        self.checkBox_5.setChecked(True)
        self.checkBox_6 = QCheckBox(self.frame_3)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setGeometry(QRect(390, 10, 87, 20))
        self.checkBox_6.setChecked(True)
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 430, 141, 31))
        self.label_5.setFont(font1)
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(220, 470, 186, 41))
        font2 = QFont()
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(219, 246, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(7, 64, 128);\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"stop: 0.5 #e7e7e7, stop: 1.0 #fafafa); border-color: rgb(7, 64, 128);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(43, 32, 255);\n"
"    border-style: inset;\n"
"}")
        self.textBrowser_2 = QTextBrowser(self.frame_4)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(40, 50, 581, 121))
        self.textBrowser_2.setStyleSheet(u"QTextBrowser {\n"
"\n"
"Background-color: white;\n"
"\n"
"}")
        self.pushButton_3 = QPushButton(self.frame_4)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(530, 10, 113, 32))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(180, 420, 431, 41))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.textEdit = QTextEdit(self.frame_5)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 10, 251, 31))
        self.textEdit.setStyleSheet(u"QTextEdit {\n"
"\n"
"background-color: white;\n"
"\n"
"}")
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(270, 20, 41, 16))
        font3 = QFont()
        font3.setPointSize(16)
        self.label.setFont(font3)
        self.pushButton_4 = QPushButton(self.frame_5)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(310, 10, 113, 32))
        font4 = QFont()
        font4.setBold(True)
        self.pushButton_4.setFont(font4)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 380, 111, 21))
        self.label_3.setFont(font1)
        self.pushButton_2 = QPushButton(self.frame_4)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(100, 320, 108, 32))
        self.pushButton_2.setFont(font4)
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(100, 280, 101, 21))
        self.label_4.setFont(font1)
        self.scrollArea = QScrollArea(self.frame_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(220, 270, 381, 89))
        self.scrollArea.setMinimumSize(QSize(0, 89))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 379, 87))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.checkBox_7 = QCheckBox(self.frame_4)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setGeometry(QRect(230, 380, 181, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.frame_4.raise_()
        self.horizontalLayoutWidget.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 648, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Noun Phrase Complexity Analyzer", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Frequency data", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Raw frequency", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Normalized frequency per 1,000 words", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Stages", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Stage 2", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Stage 3", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"Stage 4", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"Stage 5", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output file name", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start the analysis", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Instructions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Select the frequency data value you would like to see as results. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Select the stages of noun phrase structures you would like to see the results of.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -"
                        "qt-block-indent:0; text-indent:0px;\">3. Select the folder that contains the texts you would like to analyze.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Write the output file name for your results csv file, and choose the folder for your file.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. When you're ready, click on &quot;Start the analysis&quot; and wait for the results.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">** For detailed info on the noun phrase structures analyzed in this tool, click 'What is NPC'.</p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"What is NPC?", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u".csv", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Find folder", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Plot the results", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Find folder", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Input folder", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"Yes, I want a bar graph.", None))
    # retranslateUi

