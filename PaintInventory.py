from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType
from time import sleep
import sys, os
from os import path
import sqlite3

# For executable
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

FORM_CLASS,_=loadUiType(resource_path("main.ui"))

# Globals for tracking current row for Edit Inventory tab
x = 0
idx = 0

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.Handle_Buttons()
    
    def Handle_Buttons(self):
        # All Pages
        self.refresh_btn.clicked.connect(self.GET_DATA)

        # Details Page
        self.search_btn.clicked.connect(self.SEARCH)

        # Statistics Page
        self.check_btn.clicked.connect(self.LEVEL)
        self.check_btn_2.clicked.connect(self.LEVEL2)

        # Edit Page
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
        self.next_btn.clicked.connect(self.NEXT)
        self.previous_btn.clicked.connect(self.PREVIOUS)
        self.last_btn.clicked.connect(self.LAST)
        self.first_btn.clicked.connect(self.FIRST)

    
    def GET_DATA(self):
        # Connect to SQlite database and fill GUI table with data
        db = sqlite3.connect(resource_path("paint.db"))
        cursor = db.cursor()

        command = ''' SELECT * from paint_table '''
        result = cursor.execute(command)
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Display total paints number and total gallons number in statistics tab
        cursor2 = db.cursor()
        cursor3 = db.cursor()

        paint_nbr = ''' SELECT COUNT (Name) FROM paint_table ''' 
        gallons_nbr = ''' SELECT SUM (Gallons) FROM paint_table ''' 

        result_paint_nbr = cursor2.execute(paint_nbr)
        result_gallons_nbr = cursor3.execute(gallons_nbr)

        self.lbl_paint_nbr.setText(str(result_paint_nbr.fetchone()[0]))
        self.lbl_gallons_nbr.setText(str(result_gallons_nbr.fetchone()[0]))

        # Initialize Edit Inventor page info
        self.FIRST()
        self.NAVIGATE()


    def SEARCH(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())
        command = ''' SELECT * from paint_table WHERE Gallons<=?'''
        result = cursor.execute(command, [nbr])
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # Display Highest 3 volume paints
    def LEVEL(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        command = ''' SELECT Name, Location, Gallons from paint_table order by Gallons desc LIMIT 3 '''
        result = cursor.execute(command)
        self.table2.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        
    # Display lowest 3 volume paints    
    def LEVEL2(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        command = ''' SELECT Name, Location, Gallons from paint_table order by Gallons asc LIMIT 3 '''
        result = cursor.execute(command)
        self.table3.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table3.setItem(row_number, column_number, QTableWidgetItem(str(data)))



    def NAVIGATE(self):
        global idx
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        command = ''' SELECT * from paint_table WHERE ID = ? '''

        result = cursor.execute(command, [idx])
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.paint_name.setText(str(val[1]))
        self.sheen.setText(str(val[2]))
        self.location.setText(str(val[3]))
        self.gallons.setValue(val[4])

    def NEXT(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        
        tot = len(val)
        global x
        global idx
        x = x + 1

        if x < tot:
            idx = val[x][0]
            self.NAVIGATE()
        else:
            x = tot - 1
    
    def PREVIOUS(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        
        tot = len(val)
        global x
        global idx
        x = x - 1

        if x > -1:
            idx = val[x][0]
            self.NAVIGATE()
        else:
            x = 0
    
    def LAST(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        
        tot = len(val)
        global x
        global idx
        x = tot - 1

        if x < tot:
            idx = val[x][0]
            self.NAVIGATE()
        else:
            x = tot - 1
    
    def FIRST(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        val = result.fetchall()
        
        tot = len(val)
        global x
        global idx
        x = 0

        if x > -1:
            idx = val[x][0]
            self.NAVIGATE()
        else:
            x = 0

    def UPDATE(self):
        db = sqlite3.connect("paint.db")
        cursor=db.cursor()
        
        id_= int(self.id.text())
        paint_name_ = self.name.text()
        sheen_ = self.sheen.text()
        location_ = self.location.text()
        gallons_= str(self.gallons.value())
        
        row = (paint_name_,sheen_,location_,gallons_,id_)
        command = ''' UPDATE paint_table SET Name=?,Sheen=?,Location=?,Gallons=?, WHERE ID=?'''  
        cursor.execute(command,row)
        db.commit()
    
    def DELETE(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        d = self.id.text()
        command = ''' DELETE FROM paint_table WHERE ID=? '''
        cursor.execute(command, d)
        db.commit()

    def ADD(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        paint_name_ = self.paint_name.text()
        sheen_ = self.sheen.text()
        location_ = self.location.text()
        gallons_ = str(self.gallons.value())
        
        row = (paint_name_,sheen_,location_,gallons_)
        command = ''' INSERT INTO paint_table (Name,Sheen,Location,Gallons) VALUES (?, ?, ?, ?)''' 
        cursor.execute(command,row)
        db.commit()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()

if __name__== '__main__':
    main()