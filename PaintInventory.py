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

FORM_CLASS,_ = loadUiType(resource_path("main.ui"))

# Globals for tracking current row for Edit Inventory tab
id_row = 0
curr_id = 0

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setFixedWidth(560)
        self.setFixedHeight(928)
        self.setupUi(self)
        self.Handle_Buttons()
    
    def Handle_Buttons(self):
        # All Pages
        self.refresh_btn.clicked.connect(self.load_data)

        # Details Page
        self.search_btn.clicked.connect(self.search)

        # Statistics Page
        self.check_btn.clicked.connect(self.highest_3)
        self.check_btn_2.clicked.connect(self.lowest_3)

        # Edit Page
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.add_btn.clicked.connect(self.add)
        self.next_btn.clicked.connect(self.next)
        self.previous_btn.clicked.connect(self.previous)
        self.last_btn.clicked.connect(self.last)
        self.first_btn.clicked.connect(self.first)

    def load_data(self):
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
        self.first()
        self.load_edit_inventory()


    def search(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())
        command = ''' SELECT * from paint_table WHERE Gallons <= ? '''
        result = cursor.execute(command, [nbr])
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # Display Highest 3 volume paints
    def highest_3(self):
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
    def lowest_3(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        command = ''' SELECT Name, Location, Gallons from paint_table order by Gallons asc LIMIT 3 '''
        result = cursor.execute(command)
        self.table3.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table3.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def load_edit_inventory(self):
        global curr_id 
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        command = ''' SELECT * from paint_table WHERE ID = ? '''
        result = cursor.execute(command, [curr_id])
        row = result.fetchone()

        self.id.setText(str(row[0]))
        self.paint_name.setText(str(row[1]))
        self.sheen.setText(str(row[2]))
        self.location.setText(str(row[3]))
        self.gallons.setValue(row[4])

    def next(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        id_list = result.fetchall()
        
        global id_row 
        global curr_id
        id_list_len = len(id_list)
        id_row = id_row + 1

        if id_row < id_list_len:
            curr_id = id_list[id_row][0]
            self.load_edit_inventory()
        else:
            id_row = id_list_len - 1
    
    def previous(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        id_list = result.fetchall()
        
        global id_row
        global curr_id
        id_row = id_row - 1

        if id_row > -1:
            curr_id = id_list[id_row][0]
            self.load_edit_inventory()
        else:
            id_row = 0
    
    def first(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        id_list = result.fetchall()
        
        global id_row
        global curr_id
        id_row = 0

        if id_row > - 1:
            curr_id = id_list[id_row][0]
            self.load_edit_inventory()
        else:
            id_row = 0
    
    def last(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM paint_table '''
        result = cursor.execute(command)
        
        global id_row
        global curr_id
        id_list = result.fetchall()
        id_list_len = len(id_list)
        id_row = id_list_len - 1

        if id_row < id_list_len:
            curr_id = id_list[id_row][0]
            self.load_edit_inventory()
        else:
            id_row = id_list_len - 1

    def update(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()
        
        id_= int(self.id.text())
        paint_name_ = self.paint_name.text()
        sheen_ = self.sheen.text()
        location_ = self.location.text()
        gallons_= str(self.gallons.value())
        
        row = (paint_name_,sheen_,location_,gallons_,id_)
        command = ''' UPDATE paint_table SET Name=?,Sheen=?,Location=?,Gallons=? WHERE ID = ? '''  
        cursor.execute(command,row)
        db.commit()
    
    def delete(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        d = self.id.text()
        command = ''' DELETE FROM paint_table WHERE ID = ? '''
        cursor.execute(command, [d]) 
        db.commit()

    def add(self):
        db = sqlite3.connect("paint.db")
        cursor = db.cursor()

        paint_name_ = self.paint_name.text() 
        sheen_ = self.sheen.text()
        location_ = self.location.text()
        gallons_ = str(self.gallons.value())
        
        row = (paint_name_,sheen_,location_,gallons_)
        command = ''' INSERT INTO paint_table (Name,Sheen,Location,Gallons) VALUES (?, ?, ?, ?)  ''' 
        cursor.execute(command,row)
        db.commit()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()

if __name__== '__main__':
    main()
