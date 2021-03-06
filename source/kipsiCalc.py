'''
--------------------------------------------------------------------------
Copyright (C) 2019 Łukasz Laba (e-mail : lukaszlaba@gmail.pl)

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
from math import sin, asin, cos, acos, tan, atan, pi, e, log, log10, sqrt
import webbrowser

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QLabel, QTextBrowser, QTextEdit, QCheckBox, QComboBox)
from PyQt5.QtGui import QClipboard
        
from appinfo import version, appname, about, hidden_features
from units import *

from units_description import unit_description
from imperial_lengh_format import imperial_lengh_format

#---------------------------------------------------------------------

unit_list = ['kg', 't', 'lb', 'UKton', 'USton']
unit_list += ['um', 'mm', 'cm', 'dm', 'm', 'km', 'inch', 'ft', 'yd', 'mile']
unit_list += ['mm2', 'cm2','m2', 'ha', 'inch2', 'ft2', 'yd2']
unit_list += ['mm3', 'cm3', 'dm3','m3', 'inch3', 'ft3']
unit_list += ['mm4', 'cm4','m4', 'inch4', 'ft4']
unit_list += ['N', 'kN','lbf', 'kip']
unit_list += ['Nm', 'kNm','lbfinch', 'lbfft', 'kipinch', 'kipft']
unit_list += ['Pa', 'kN/m2', 'kPa','MPa', 'bar', 'GPa', 'psi', 'ksi', 'psf', 'ksf']
unit_list += ['kN/m', 'lbf/ft', 'plf', 'kip/ft', 'klf']
unit_list += ['kN/m3', 'lbf/inch3', 'kip/ft3' ,'pci' ,'pcf', 'kcf']
unit_list += ['kg/m3', 't/m3', 'lb/ft3',]
unit_list += ['s', 'h']

extra_units_list = ['ft_inch'] #those units has no button

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

report_default_text = 'Here you can write simple report. Use the |Add to report| button to get results here. Enjoy!'

class MAINWINDOW(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super(MAINWINDOW, self).__init__(parent)
        
        #---------
        self.result = 0
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
        self.autoCheckBox.setToolTip('if checked, every time you change the expression it will be evaluated')
        self.autoreportCheckBox = QCheckBox('auto add to report')
        self.autoreportCheckBox.setToolTip('if checked, every time you use |eval| or |=| result will be added to report')
        self.errorCheckBox = QCheckBox('error msg')
        self.errorCheckBox.setToolTip('if checked, you will get info why ERROR occurred')
        self.add_to_reportButton = createButton("add to report",self.add_to_report)
        self.unit_ComboBox = QComboBox()
        self.unit_ComboBox.currentIndexChanged.connect(self.user_unit_changed)
        self.textEditor = QTextEdit()

        self.digitButtons = []
        for i in range(self.NumDigitButtons):
            self.digitButtons.append(createButton(str(i),
                    self.basicClicked))

        self.unitButtons = []
        for i in unit_list:
            self.unitButtons.append(createButton(str(i),
                    self.unitClicked))

        self.eButton = createButton("E", self.basicClicked)
        self.eButton.setToolTip('E-notation (1E2 = 100, 1E-2 = 0.01 ..)')
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
        self.evallButton.setToolTip('it evaluate expression')
        self.ansButton = createButton("ans", self.basicClicked)
        self.ansButton.setToolTip('last answer key - it holds the result after the equals (=) key was last pressed')
        self.equalButton = createButton("=", self.equalClicked)
        self.equalButton.setToolTip('it evaluate expression and move result to ans')
        self.infoButton = createButton("app info", self.info_app)
        self.cb1Button = createButton("cb_res>>", self.copy_res_to_clipboard)
        self.cb1Button.setToolTip('copy only result text to clipboard')
        self.cb2Button = createButton("cb_eq>>", self.copy_equ_to_clipboard)
        self.cb2Button.setToolTip('copy all equation text to clipboard')
        self.cbinButton = createButton("<<cb_in", self.insert_form_clipboard)
        self.cbinButton.setToolTip('insert expresion from clipboard')
        self.featuresButton = createButton("...", self.info_hidden_features)
        self.featuresButton.setToolTip('hidden features info')

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
        for i in range(1, self.NumDigitButtons): # 1-9
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
        mainLayout.addWidget(self.featuresButton, 8 + startrow, 3 + startcol)
        mainLayout.addWidget(self.autoCheckBox, 8 + startrow, 0 + startcol, 1, 3)
        mainLayout.addWidget(self.autoreportCheckBox, 9 + startrow, 0 + startcol, 1, 3)
        
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
        mainLayout.addWidget(self.infoButton, 10, 17)
        
        #---copy to cliboard
        mainLayout.addWidget(self.cbinButton, 4, 17)
        mainLayout.addWidget(self.cb1Button, 6, 17)
        mainLayout.addWidget(self.cb2Button, 5, 17)

        #---text editor
        mainLayout.addWidget(self.textEditor, 20, 0, 1, 18)        
        #-------------        
        self.setLayout(mainLayout)
        #-------------
        self.setWindowTitle("%s %s - simple calculator supporting unit calculations"%(appname, version))
        self.setWindowIcon(QtGui.QIcon('app.ico'))
    
    @property
    def result_string(self):
        if self.unit_ComboBox.currentText()=='ft_inch':
            result_string = imperial_lengh_format(self.result).replace(' ','')
        else:
            result_string = str(self.result).replace(' ','')
        #---
        if result_string.endswith('*'):
            result_string = result_string[:-1]
        return result_string

    def basicClicked(self):
        clickedButton = self.sender()
        content = clickedButton.text()
        self.display_res.setText('')
        self.warnings.setText('-')
        self.display.insert(content)

    def unitClicked(self):
        text_before_cursor = self.display.text()[0:self.display.cursorPosition()]
        try:
            last_sing_in_curent_expresion = text_before_cursor.replace(' ', '')[-1]
        except:
            last_sing_in_curent_expresion = None
        clickedButton = self.sender()
        if last_sing_in_curent_expresion in ['+', '-', '/', '*', '(', ')', None]:
            content = clickedButton.text()
        else:
            content = '*' + clickedButton.text()
        self.display_res.setText('')
        self.warnings.setText('-')
        self.display.insert(content)

    def evalClicked(self):
        self.calculate()
        if self.autoreportCheckBox.isChecked():
            self.add_to_report()

    def equalClicked(self):
        global ans
        self.calculate()
        if not self.result is None:
            if self.autoreportCheckBox.isChecked():
                self.add_to_report()
            ans = self.result
            self.display.setText('ans')
            
    def backspaceClicked(self):
        self.display_res.setText('')
        self.warnings.setText('-')
        myapp.display.backspace()

    def clear(self):
        self.display_res.setText('0')
        self.warnings.setText('-')
        self.display.setText('')

    def auto_calculate(self):
        if self.autoCheckBox.isChecked():
            self.calculate()
            
    def calculate(self):
        #expresion = self.display.text()
        #formated_expresion = self.format_expresion(expresion)
        #myapp.display.setText(formated_expresion)
        #---------------
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
        expreson = expreson.replace(' ', '')        
        return expreson
        
    def get_expresion_str(self):
        ans_string = str(ans)
        if ans_string.endswith('*'):
            ans_string = ans_string[:-1]
        expresion = self.display.text().replace('ans', '(%s)'%ans_string)
        return expresion
        
    def get_result_str(self):
        result = self.display_res.text()
        return result
        
    def add_to_report(self):
        if self.textEditor.toPlainText() == report_default_text:
            self.textEditor.clear()
        #----
        expresion = self.get_expresion_str()
        result = self.get_result_str()
        #---
        if self.textEditor.toPlainText() == '':
            record = expresion + ' = ' + result
        else:
             record =  '\n' + expresion + ' = ' + result   
        #---
        self.textEditor.insertPlainText(record)
    
    def set_unit_list(self):
        self.block = True
        self.unit_ComboBox.clear()
        default = None
        native = None
        for unit in unit_list + extra_units_list:
                this_unit = eval(unit)
                try:
                    this_unit + self.result
                    self.unit_ComboBox.addItem(unit)
                    if unit in user_used_units:
                        default = unit
                    if self.result.asNumber() == self.result/this_unit:
                        native = unit
                except:
                    pass
        self.unit_ComboBox.setCurrentIndex(self.unit_ComboBox.findText(native))
        self.block = False
        if default:
            self.unit_ComboBox.setCurrentIndex(self.unit_ComboBox.findText(default))
        
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
    
    def copy_res_to_clipboard(self):
        result = self.get_result_str()
        text = result
        cb = QApplication.clipboard()
        cb.setText(text)

    def copy_equ_to_clipboard(self):
        expresion = self.get_expresion_str()
        result = self.get_result_str()
        text = expresion + ' = ' + result
        cb = QApplication.clipboard()
        cb.setText(text)

    def insert_form_clipboard(self):
        cb = QApplication.clipboard()
        cbtext = cb.text()
        # if there is = thern split ant take only first part
        # also remowe whitespaces from left and right ends
        expresion = cb.text().split('=')[0].lstrip().rstrip()
        # now set the expresion
        myapp.display.setText(expresion)
        
    def info_app(self):
        QMessageBox.about(self, "App Info", about)
        webbrowser.open('https://github.com/lukaszlaba/kipsiCalc')
        
    def info_hidden_features(self):
        QMessageBox.about(self, "Hidden features", hidden_features)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myapp = MAINWINDOW()
    myapp.autoCheckBox.setChecked(True)
    myapp.calculate()
    #---
    myapp.textEditor.setText(report_default_text)
    #----
    myapp.show()
    sys.exit(app.exec_())
    
'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ...\kipsiCalc.py
'''