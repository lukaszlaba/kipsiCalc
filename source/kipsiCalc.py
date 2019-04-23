'''
--------------------------------------------------------------------------
Copyright (C) 2019 Łukasz Laba (e-mail : lukaszlab@o2.pl)

This file is part of ksipsiCalc.
ksipsiCalc - simple calculator supporting unit calculations.

ksipsiCalc is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

ksipsiCalc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ksipsiCalc; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''


import traceback
from math import sin, asin, cos, acos, tan, atan, pi, e, log, log10

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QLabel, QTextBrowser, QTextEdit, QCheckBox, QComboBox)
        
from appinfo import version, appname, about
from units import *

from units_description import unit_description

#---------------------------------------------------------------------

unit_list = ['kg', 't', 'lb']
unit_list += ['um', 'mm', 'cm', 'dm', 'm', 'km', 'inch', 'ft', 'yd', 'mile']
unit_list += ['mm2', 'cm2','m2', 'ha', 'inch2', 'ft2', 'yd2']
unit_list += ['mm3', 'cm3', 'dm3','m3', 'inch3', 'ft3']
unit_list += ['mm4', 'cm4','m4', 'inch4', 'ft4']
unit_list += ['N', 'kN','lbf', 'kip']
unit_list += ['Nm', 'kNm','lbfinch', 'lbfft', 'kipinch', 'kipft']
unit_list += ['Pa', 'kN/m2', 'kPa','MPa', 'bar', 'GPa', 'psi', 'ksi', 'psf', 'ksf']
unit_list += ['kN/m', 'lbf/ft', 'plf', 'kip/ft']
unit_list += ['kN/m3', 'lbf/inch3', 'kip/ft3']
unit_list += ['kg/m3', 't/m3', 'lb/ft3',]
unit_list += ['s', 'h']


user_used_units = ['kg', 'm','m2', 'm3', 'm4', 'kN', 'kNm', 'kPa', 'kN/m', 'kN/m3', 'kg/m3', 's']

def are_the_same_unit(val1, val2):
    try:
        val1 + val2
        return True
    except:
        return False

def unit_color(val):
    if are_the_same_unit(val, kg):
        colour = "background-color: rgb(251,155,111)"
    elif are_the_same_unit(val, m):
        colour = "background-color: rgb(251,239,112)"
    elif are_the_same_unit(val, m2):
        colour = "background-color: rgb(134,250,128)"
    elif are_the_same_unit(val, m3):
        colour = "background-color: rgb(129,248,242)"
    elif are_the_same_unit(val, m4):
        colour = "background-color: rgb(183,193,251)"
    elif are_the_same_unit(val, N):
        colour = "background-color: rgb(250,183,246)"
    elif are_the_same_unit(val, Nm):
        colour = "background-color: rgb(251,155,111)"
    elif are_the_same_unit(val, Pa):
        colour = "background-color: rgb(251,239,112)"
    elif are_the_same_unit(val, N/m):
        colour = "background-color: rgb(134,250,128)"
    elif are_the_same_unit(val, N/m3):
        colour = "background-color: rgb(129,248,242)"
    elif are_the_same_unit(val, kg/m3):
        colour = "background-color: rgb(183,193,251)"
    else:
        colour = "background-color: rgb(250,183,246)"
    return colour

    
#---------------------------------------------------------------------

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 15)
        size.setWidth(max(size.width(), size.height()))
        return size
        
def createButton(text, member):
    button = Button(text)
    button.clicked.connect(member)
    return button


#---------------------------------------------------------------------

ans = 0

class Calculator(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.block = False

        #---------
        self.display = QLineEdit('')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        font = self.display.font()
        font.setPointSize(font.pointSize() + 4)
        self.display.setFont(font)
        self.display.textChanged.connect(self.auto_calculate)
        
        self.display_res = QLineEdit('')
        self.display_res.setReadOnly(True)
        self.display_res.setAlignment(Qt.AlignRight)
        font = self.display_res.font()
        font.setPointSize(font.pointSize() + 4)
        self.display_res.setFont(font)
        
        self.warnings = QLabel()
        self.warnings.setText("-")
        self.warnings.setAlignment(Qt.AlignRight)
        
        self.autoCheckBox = QCheckBox('auto eval')
        self.autoreportCheckBox = QCheckBox('auto add to report')
        self.errorCheckBox = QCheckBox('error msg')
        self.add_to_reportButton = createButton("add to report",self.add_to_report)
        self.unit_ComboBox = QComboBox()
        self.unit_ComboBox.currentIndexChanged.connect(self.user_unit_changed)
        self.textEditor = QTextEdit()

        self.digitButtons = []
        for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(createButton(str(i),
                    self.basicClicked))

        self.unitButtons = []
        for i in unit_list:
            self.unitButtons.append(createButton(str(i),
                    self.unitClicked))

        self.eButton = createButton("E", self.basicClicked)
        self.pointButton = createButton(".", self.basicClicked)
        self.deleteButton = createButton("DEL",self.backspaceClicked)
        self.clearButton = createButton("C", self.clear)
        self.divisionButton = createButton(" / ",self.basicClicked)
        self.timesButton = createButton(" * ",self.basicClicked)
        self.minusButton = createButton(" - ", self.basicClicked)
        self.plusButton = createButton(" + ", self.basicClicked)
        self.squareRootButton = createButton("^",self.basicClicked)
        self.brackedopenButton = createButton("(",self.basicClicked)
        self.brackedcloseButton = createButton(")",self.basicClicked)
        self.evallButton = createButton("eval", self.evalClicked)
        self.ansButton = createButton("ans", self.basicClicked)
        self.equalButton = createButton("=", self.equalClicked)
        self.infoButton = createButton("app info", self.info)

        #--------------app layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(self.display, 0, 0, 1, 10)
        mainLayout.addWidget(self.display_res, 0, 10, 1, 8)
        mainLayout.addWidget(self.unit_ComboBox, 1, 17)
        
        mainLayout.addWidget(self.warnings, 1, 0, 1, 10)
        mainLayout.addWidget(self.errorCheckBox, 1, 10, 1, 2)
        
        #--numpad
        startcol = 0
        startrow = 3
        mainLayout.addWidget(self.deleteButton, 0 + startrow, 0 + startcol, 1, 2)
        mainLayout.addWidget(self.clearButton, 0 + startrow, 2 + startcol, 1, 2)
        for i in range(1, Calculator.NumDigitButtons): # 1-9
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 0
            mainLayout.addWidget(self.digitButtons[i], row + startrow, column + startcol)
        mainLayout.addWidget(self.digitButtons[0], 5 + startrow, 0 + startcol)    # 0
        mainLayout.addWidget(self.pointButton, 5 + startrow, 1 + startcol)        # .
        mainLayout.addWidget(self.eButton, 5 + startrow, 2 + startcol)            # e
        mainLayout.addWidget(self.divisionButton, 1 + startrow, 0 + startcol, 1, 2)     # /
        mainLayout.addWidget(self.timesButton, 1 + startrow, 2 + startcol)        # *
        mainLayout.addWidget(self.minusButton, 1 + startrow, 3 + startcol)        # -
        mainLayout.addWidget(self.plusButton, 2 + startrow, 3 + startcol)         # +
        mainLayout.addWidget(self.squareRootButton, 3 + startrow, 3 + startcol)   # ^
        mainLayout.addWidget(self.brackedopenButton, 4 + startrow, 3 + startcol)  # (
        mainLayout.addWidget(self.brackedcloseButton, 5 + startrow, 3 + startcol) # )
        mainLayout.addWidget(self.equalButton, 6 + startrow, 2 + startcol, 1, 2)  # =
        mainLayout.addWidget(self.evallButton, 6 + startrow, 0 + startcol, 1, 2)  # =
        mainLayout.addWidget(self.add_to_reportButton, 7 + startrow, 0 + startcol, 1, 2)
        mainLayout.addWidget(self.ansButton, 7 + startrow, 2 + startcol, 1, 2)
        mainLayout.addWidget(self.autoCheckBox, 8 + startrow, 0 + startcol, 1, 4)
        mainLayout.addWidget(self.autoreportCheckBox, 9 + startrow, 0 + startcol, 1, 4)
        
        
        #--units
        startcol = 5
        startrow = 3

        row = startrow
        column = startcol

        for i in range(0, len(unit_list)):
            row = i / 7
            column = i  % 7
            mainLayout.addWidget(self.unitButtons[i], row + startrow, column + startcol)
            self.unitButtons[i].setStyleSheet( unit_color(eval(unit_list[i])))
            self.unitButtons[i].setToolTip(unit_description(unit_list[i]))
            
        #---info
        mainLayout.addWidget(self.infoButton, 7, 17)

        #---text editor
        mainLayout.addWidget(self.textEditor, 20, 0, 1, 18)        
        #-------------        
        self.setLayout(mainLayout)
        #-------------
        self.setWindowTitle("%s %s - simple calculator supporting unit calculations"%(appname, version))
        self.setWindowIcon(QtGui.QIcon('app.ico'))
    
    @property
    def result_string(self):
        result_string = str(self.result).replace(' ','')
        if result_string.endswith('*'):
            result_string = result_string[:-1]
        return result_string
        
    
    
    def basicClicked(self):
        clickedButton = self.sender()
        content = clickedButton.text()
        self.display_res.setText('')
        self.warnings.setText('-')
        self.display.setText(self.display.text() + content)

    def unitClicked(self):
        try:
            last_sing_in_curent_expresion = self.display.text().replace(' ', '')[-1]
        except:
            last_sing_in_curent_expresion = None
        clickedButton = self.sender()
        if last_sing_in_curent_expresion in ['+', '-', '/', '*', '(', ')', None]:
            content = clickedButton.text()
        else:
            content = '*' + clickedButton.text()
        self.display_res.setText('')
        self.warnings.setText('-')
        self.display.setText(self.display.text() + content)

    def evalClicked(self):
        self.calculate()
        if self.autoreportCheckBox.isChecked():
            self.add_to_report()

    def equalClicked(self):
        global ans
        if not self.result is None:
            self.calculate()
            if self.autoreportCheckBox.isChecked():
                self.add_to_report()
            ans = self.result
            self.display.setText('ans')
            
            

    def backspaceClicked(self):
        self.display_res.setText('')
        self.warnings.setText('-')
        text = self.display.text()[:-1]
        self.display.setText(text)

    def clear(self):
        self.display_res.setText('0')
        self.warnings.setText('-')
        self.display.setText('')

    def auto_calculate(self):
        if self.autoCheckBox.isChecked():
            self.calculate()
            
    def calculate(self):
        expresion = self.display.text()
        expresion = self.decode(expresion)
        try:
            self.result = eval(expresion) * m/m
            self.display_res.setText(self.result_string)
            self.warnings.setText('-')
        except Exception as e:
            self.result = None
            self.display_res.setText("ERROR")
            if self.errorCheckBox.isChecked():
                self.warnings.setText(str(e))
        if not expresion:
            self.display_res.setText("0")
            if self.errorCheckBox.isChecked():
                self.warnings.setText('-')
        self.set_unit_list()
        
    def decode(self, expreson):
        expreson = expreson.replace('^', '**')
        expreson = expreson.replace(',', '.')
        return expreson 
        
    def add_to_report(self):
        ans_string = str(ans)
        if ans_string.endswith('*'):
            ans_string = ans_string[:-1]
        expresion = self.display.text().replace('ans', '(%s)'%ans_string)
        #---
        result = self.display_res.text()
        #---
        record = expresion + ' = ' + result
        #---
        calc.textEditor.toPlainText()
        calc.textEditor.setText(calc.textEditor.toPlainText() + '\n' + record)
    
    def set_unit_list(self):
        self.block = True
        calc.unit_ComboBox.clear()
        default = None
        native = None
        for unit in unit_list:
                this_unit = eval(unit)
                try:
                    this_unit + self.result
                    calc.unit_ComboBox.addItem(unit)
                    if unit in user_used_units:
                        default = unit
                    if self.result.asNumber() == self.result/this_unit:
                        native = unit
                except:
                    pass
        calc.unit_ComboBox.setCurrentIndex(calc.unit_ComboBox.findText(native))
        self.block = False
        if default:
            calc.unit_ComboBox.setCurrentIndex(calc.unit_ComboBox.findText(default))
        
    def user_unit_changed(self):
        if not self.block:
            try:
                unit_string = self.unit_ComboBox.currentText()
                user_unit= eval(unit_string)
                self.result = self.result.asUnit(user_unit)
                self.display_res.setText(self.result_string)
                self.add_to_used(unit_string)
            except:
                pass
                
    def add_to_used(self, unit):
        already_exist = None
        for i in range(len(user_used_units)):
            u = user_used_units[i]
            try:
                eval(u) + eval(unit)
                user_used_units[i] = unit
                already_exist = True
            except:
                pass
        if not already_exist:
            user_used_units.append(unit)

    def info(self):
        QMessageBox.about(self, "App Info", about)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.autoCheckBox.setChecked(True)
    calc.calculate()
    calc.textEditor.setText('Here you can write simple report. Use the |Add to report| botton to get results here. Enjoy!')
    calc.show()
    sys.exit(app.exec_())
    
'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ...\kipsiCalc.py
'''