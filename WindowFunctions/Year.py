import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.EnterYear import Ui_Year
from Reports import financial_report

class EnterYear(QtWidgets.QWidget):
    def YearSpinBox_slot(self, value):
        self.YearSpinBoxValue = value
    def ReportButton_slot(self):
        financial_report(self.connection, 'financial_report.csv', self.YearSpinBoxValue)
    def __init__(self, connection):
        super(EnterYear, self).__init__()
        self.ui = Ui_Year()
        self.ui.setupUi(self)
        self.connection = connection
        self.YearSpinBoxValue = self.ui.YearSpinBox.minimum()
        self.ui.YearSpinBox.valueChanged.connect(self.YearSpinBox_slot)
        self.ui.ReportButton.clicked.connect(self.ReportButton_slot)
