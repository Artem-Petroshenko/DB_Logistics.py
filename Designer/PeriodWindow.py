# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Designer\PeriodWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Period(object):
    def setupUi(self, Period):
        Period.setObjectName("Period")
        Period.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Period)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.FromDateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.FromDateEdit.setObjectName("FromDateEdit")
        self.gridLayout.addWidget(self.FromDateEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ToDateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.ToDateEdit.setObjectName("ToDateEdit")
        self.gridLayout.addWidget(self.ToDateEdit, 1, 1, 1, 1)
        self.ReportButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ReportButton.setObjectName("ReportButton")
        self.gridLayout.addWidget(self.ReportButton, 2, 0, 1, 2)

        self.retranslateUi(Period)
        QtCore.QMetaObject.connectSlotsByName(Period)

    def retranslateUi(self, Period):
        _translate = QtCore.QCoreApplication.translate
        Period.setWindowTitle(_translate("Period", "Form"))
        self.label.setText(_translate("Period", "Начало периода"))
        self.label_2.setText(_translate("Period", "Конец периода"))
        self.ReportButton.setText(_translate("Period", "Получить отчет"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Period = QtWidgets.QWidget()
    ui = Ui_Period()
    ui.setupUi(Period)
    Period.show()
    sys.exit(app.exec_())
