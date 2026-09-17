# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NPCA_v2.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
    QStatusBar, QTextBrowser, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(694, 741)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: yelow;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setStyleSheet(u"QFrame {\n"
"Background-color: Beige;\n"
"}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.title = QLabel(self.frame_4)
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


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.pushButton_3 = QPushButton(self.frame_4)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.textBrowser_2 = QTextBrowser(self.frame_4)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setMinimumSize(QSize(575, 140))
        self.textBrowser_2.setMaximumSize(QSize(16777215, 160))
        self.textBrowser_2.setStyleSheet(u"QTextBrowser {\n"
"\n"
"Background-color: white;\n"
"\n"
"}")

        self.verticalLayout_2.addWidget(self.textBrowser_2)

        self.frame = QFrame(self.frame_4)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.frame)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.checkBox_3 = QCheckBox(self.frame_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.frame_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.frame_3)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.frame_3)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBox_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.horizontalFrame_3 = QFrame(self.frame_4)
        self.horizontalFrame_3.setObjectName(u"horizontalFrame_3")
        self.horizontalFrame_3.setFrameShape(QFrame.StyledPanel)
        self.horizontalFrame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalFrame_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_2 = QPushButton(self.horizontalFrame_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setBold(True)
        self.pushButton_2.setFont(font2)

        self.horizontalLayout_4.addWidget(self.pushButton_2)

        self.label_4 = QLabel(self.horizontalFrame_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.scrollArea = QScrollArea(self.horizontalFrame_3)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMaximumSize(QSize(16777215, 25))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 389, 23))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_4.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.horizontalFrame_3)

        self.line = QFrame(self.frame_4)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.checkBox_7 = QCheckBox(self.frame_4)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.horizontalLayout_5.addWidget(self.checkBox_7)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.line_3 = QFrame(self.frame_4)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_4 = QPushButton(self.frame_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFont(font2)

        self.horizontalLayout_7.addWidget(self.pushButton_4)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setFont(font1)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.textEdit = QTextEdit(self.frame_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(0, 25))
        self.textEdit.setMaximumSize(QSize(16777215, 25))
        self.textEdit.setStyleSheet(u"QTextEdit {\n"
"\n"
"background-color: white;\n"
"\n"
"}")

        self.horizontalLayout_7.addWidget(self.textEdit)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setPointSize(16)
        self.label.setFont(font3)

        self.horizontalLayout_7.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        font4 = QFont()
        font4.setBold(True)
        font4.setItalic(False)
        self.pushButton.setFont(font4)
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

        self.verticalLayout_2.addWidget(self.pushButton)

        self.progressBar = QProgressBar(self.frame_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"    width: 20px;\n"
"}")
        self.progressBar.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.progressBar)


        self.verticalLayout.addWidget(self.frame_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 694, 30))
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
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"What is NPC?", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Instructions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Select the type of frequency data and the noun phrase structure stages you wish to analyze.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Choose the folder that contains the text files for analysis.</p>\n"
"<p style=\" "
                        "margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. To visualize the results, check the box to generate a bar graph. The image file &quot;npc_plot.png&quot; will be saved in your output folder.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Enter a name for your output CSV file, and select the folder where it should be saved.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. Click &quot;Start the analysis&quot; to begin processing. Please wait while the results are generated.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">** For detailed info on the noun phrase structures analyzed by this tool, click 'What is NPC'.</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Frequency data:", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Raw frequency", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Normalized frequency per 1,000 words", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Stages:", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Stage 2", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Stage 3", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"Stage 4", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"Stage 5", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Select input folder", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Input folder", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Plot the results", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"Yes, I want a bar graph.", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Select output folder", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output file name", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"<enter file name here>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u".csv", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start the analysis", None))
    # retranslateUi

