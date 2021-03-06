# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Designer\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(857, 635)
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 801, 571))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ActivityLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.ActivityLabel.setFont(font)
        self.ActivityLabel.setAutoFillBackground(True)
        self.ActivityLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ActivityLabel.setLineWidth(3)
        self.ActivityLabel.setMidLineWidth(10)
        self.ActivityLabel.setTextFormat(QtCore.Qt.PlainText)
        self.ActivityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ActivityLabel.setObjectName("ActivityLabel")
        self.gridLayout.addWidget(self.ActivityLabel, 2, 0, 1, 2)
        self.MileageButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.MileageButton.setObjectName("MileageButton")
        self.gridLayout.addWidget(self.MileageButton, 8, 0, 1, 1)
        self.DowntimeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.DowntimeButton.setObjectName("DowntimeButton")
        self.gridLayout.addWidget(self.DowntimeButton, 8, 1, 1, 1)
        self.CityActivityButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.CityActivityButton.setObjectName("CityActivityButton")
        self.gridLayout.addWidget(self.CityActivityButton, 9, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 11, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 2)
        self.SellButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.SellButton.setObjectName("SellButton")
        self.gridLayout.addWidget(self.SellButton, 3, 1, 1, 1)
        self.BuyButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.BuyButton.setObjectName("BuyButton")
        self.gridLayout.addWidget(self.BuyButton, 3, 0, 1, 1)
        self.FinancialReportButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.FinancialReportButton.setObjectName("FinancialReportButton")
        self.gridLayout.addWidget(self.FinancialReportButton, 10, 0, 1, 2)
        self.OrderButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.OrderButton.setObjectName("OrderButton")
        self.gridLayout.addWidget(self.OrderButton, 5, 0, 1, 2)
        self.ReportLable = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ReportLable.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.ReportLable.setFont(font)
        self.ReportLable.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ReportLable.setAutoFillBackground(True)
        self.ReportLable.setLineWidth(3)
        self.ReportLable.setMidLineWidth(10)
        self.ReportLable.setTextFormat(QtCore.Qt.PlainText)
        self.ReportLable.setAlignment(QtCore.Qt.AlignCenter)
        self.ReportLable.setWordWrap(False)
        self.ReportLable.setObjectName("ReportLable")
        self.gridLayout.addWidget(self.ReportLable, 7, 0, 1, 2)
        self.CargoPopularityButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.CargoPopularityButton.setObjectName("CargoPopularityButton")
        self.gridLayout.addWidget(self.CargoPopularityButton, 9, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
        self.ActivityLabel.setText(_translate("MainWindow", "??????????????"))
        self.MileageButton.setText(_translate("MainWindow", "?????????????????????? ???????????????????????? ??????????????"))
        self.DowntimeButton.setText(_translate("MainWindow", "?????????????????????? ??????????????"))
        self.CityActivityButton.setText(_translate("MainWindow", "???????????????????? ??????????????"))
        self.SellButton.setText(_translate("MainWindow", "?????????????? ????????????????"))
        self.BuyButton.setText(_translate("MainWindow", "???????????? ????????????????"))
        self.FinancialReportButton.setText(_translate("MainWindow", "???????????????????? ??????????"))
        self.OrderButton.setText(_translate("MainWindow", "???????????????? ??????????"))
        self.ReportLable.setText(_translate("MainWindow", "???????????????????? ???? ????????????"))
        self.CargoPopularityButton.setText(_translate("MainWindow", "???????????????????? ??????????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
