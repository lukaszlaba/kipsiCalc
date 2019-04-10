'''
--------------------------------------------------------------------------
Copyright (C) 2016-2017 Lukasz Laba <lukaszlab@o2.pl>

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

#!/usr/bin/env python
import traceback
import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget, QLabel, QTextBrowser, QTextEdit, QCheckBox, QComboBox)

from unum import Unum as __Unum

# Unum customization 
__Unum.UNIT_SEP = '*'
__Unum.UNIT_DIV_SEP = '/'
__Unum.UNIT_FORMAT = '*%s'
__Unum.VALUE_FORMAT = '%5.3f'
#__Unum.VALUE_FORMAT ="%.9g"

#---------------------------------------------------------------------
# SI units
from unum.units import m                       # [m] unit definition
from unum.units import cm                      # [cm] unit definition
from unum.units import mm                      # [mm] unit definition
from unum.units import um                      # [um] unit definition
from unum.units import kg                      # [kg] unit definition
from unum.units import rad                     # [rad] unit definition
from unum.units import deg                     # [deg] unit definition

m2=m**2                                        # [m2] unit definition
cm2=cm**2                                      # [cm2] unit definition
mm2=mm**2                                      # [mm2] unit definition

m3=m**3                                        # [m3] unit definition
cm3=cm**3                                      # [cm3] unit definition
mm3=mm**3                                      # [mm3] unit definition

m4=m**4                                        # [m4] unit definition
cm4=cm**4                                      # [cm4] unit definition
mm4=mm**4                                      # [mm4] unit definition
 
from unum.units import N                       # [N] unit definition
kN = __Unum.unit('kN', 1E3 * N)                # [kN] unit definition

Nm = __Unum.unit('Nm', N * m)                  # [Nm] unit definition
kNm = __Unum.unit('kNm', 1E3 * N * m)          # [kNm] unit definition
 
from unum.units import J                       # [J] unit definition

from unum.units import Pa as Pa                # [Pa] unit definition
kPa = __Unum.unit('kPa', 1E3 * Pa)             # [kPa] unit definition
MPa = __Unum.unit('MPa', 1E6 * Pa)             # [MPa] unit definition
GPa = __Unum.unit('GPa', 1E9 * Pa)             # [MPa] unit definition

from unum.units import s                       # [s] unit definition

#---------------------------------------------------------------------
#Imperial units

inch = __Unum.unit('inch', 0.0254 * m)          # [in] unit definition
ft = __Unum.unit('ft', 12. * inch)              # [ft] unit definition
yd = __Unum.unit('yd', 3. * ft)                 # [yd] unit definition

inch2 = inch**2                                 # [inch2] unit definition
ft2 = ft**2                                     # [ft2] unit definition
yd2 = yd**2                                     # [yrd2] unit definition
                
inch3 = inch**3                                 # [inch3] unit definition
ft3 = ft**3                                     # [ft3] unit definition

inch4 = inch**4                                 # [inch4] unit definition

lb = __Unum.unit('lb', 0.45359237 * kg)         # [lb] unit definition
lbf = __Unum.unit('lbf', 4.4482216152605 * N)   # [lbf] unit definition
kip = __Unum.unit('kip', 1E3 * lbf)             # [kip] unit definition

lbfinch = __Unum.unit('lbfinch', lbf * inch)    # [lbfinch] unit definition
lbfft = __Unum.unit('lbfft', lbf * ft)          # [lbfft] unit definition
kipft = __Unum.unit('kipft', kip * ft)          # [kipft] unit definition
kipinch = __Unum.unit('kipinch', kip * inch)    # [kipinch] unit definition

psi = __Unum.unit('psi', lbf / inch2)           # [psi] unit definition
ksi = __Unum.unit('ksi', 1E3 * psi)             # [ksi] unit definition
psf = __Unum.unit('psf', lbf / ft2)             # [psf] unit definition
ksf = __Unum.unit('ksf', 1E3 * psf)             # [ksf] unit definition

#---------------------------------------------------------------------

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 1)
        size.setWidth(max(size.width(), size.height()))
        return size
        
def createButton(text, member):
    button = Button(text)
    button.clicked.connect(member)
    return button  

#---------------------------------------------------------------------

unit_list = ['kg', 'lb']
unit_list += ['um', 'mm', 'cm','m', 'ft', 'inch', 'yd']
unit_list += ['mm2', 'cm2','m2', 'ft2', 'inch2', 'yd2']
unit_list += ['mm3', 'cm3','m3', 'ft3', 'inch3']
unit_list += ['mm4', 'cm4','m4', 'inch4']
unit_list += ['N', 'kN','lbf', 'kip']
unit_list += ['Nm', 'kNm','lbfinch', 'lbfft', 'kipft', 'kipinch']
unit_list += ['Pa', 'kPa','MPa', 'GPa', 'psi', 'ksi', 'psf', 'ksf']
unit_list += ['kN/m', 'kN/cm', 'kip/inch']
unit_list += ['kN/m3', 'kN/cm3', 'kip/inch3']
unit_list += ['deg', 'rad']

user_used_units = []

class Calculator(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.block = False

        #---------
        self.display = QLineEdit('')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        #self.display.setMaxLength(8)
        font = self.display.font()
        font.setPointSize(font.pointSize() + 2)
        self.display.setFont(font)
        self.display.textChanged.connect(self.auto_calculate)
        
        self.display_res = QLineEdit('')
        self.display_res.setReadOnly(True)
        self.display_res.setAlignment(Qt.AlignRight)
        #self.display_res.setMaxLength(8)
        font = self.display_res.font()
        font.setPointSize(font.pointSize() + 2)
        self.display_res.setFont(font)
        
        self.warnings = QLabel()
        self.warnings.setText("Hello World")
        self.warnings.setAlignment(Qt.AlignRight)
        
        self.autoCheckBox = QCheckBox('Auto calculate')
        self.errorCheckBox = QCheckBox('Show error massage')
        self.add_to_reportButton = createButton("Add to report",self.add_to_report)
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

        self.pointButton = createButton(".", self.basicClicked)
        self.backspaceButton = createButton("Backspace",self.backspaceClicked)
        self.clearButton = createButton("Clear", self.clear)
        self.divisionButton = createButton(" / ",self.basicClicked)
        self.timesButton = createButton(" * ",self.basicClicked)
        self.minusButton = createButton(" - ", self.basicClicked)
        self.plusButton = createButton(" + ", self.basicClicked)
        self.squareRootButton = createButton("^",self.basicClicked)
        self.brackedopenButton = createButton("(",self.basicClicked)
        self.brackedcloseButton = createButton(")",self.basicClicked)
        self.equalButton = createButton("=", self.equalClicked)

        #--------------app layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(self.display, 0, 0, 1, 10)
        mainLayout.addWidget(self.display_res, 0, 11, 1, 8)
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
        mainLayout.addWidget(self.warnings, 1, 4, 1, 8)
        mainLayout.addWidget(self.textEditor, 11, 0, 1, 14)
        mainLayout.addWidget(self.autoCheckBox, 1, 16)
        mainLayout.addWidget(self.errorCheckBox, 2, 16)
        mainLayout.addWidget(self.add_to_reportButton, 3, 16)
        mainLayout.addWidget(self.unit_ComboBox, 4, 16)
        
        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)

        for i in range(0, len(unit_list)):
            print(i)
            row = 10
            column = i
            mainLayout.addWidget(self.unitButtons[i], row, column)

        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)
        mainLayout.addWidget(self.squareRootButton, 2, 5)
        mainLayout.addWidget(self.brackedopenButton, 5, 8)
        mainLayout.addWidget(self.brackedcloseButton, 5, 9)
        mainLayout.addWidget(self.equalButton, 5, 5)
        self.setLayout(mainLayout)
        
        #-------------
        self.display.setWindowTitle("kipsiCalc")  
    
    @property
    def result_string(self):
        result_string = str(self.result).replace(' ','')
        if result_string.endswith('*'):
            result_string = result_string[:-1]
        return result_string

    def basicClicked(self):
        clickedButton = self.sender()
        content = clickedButton.text()
        self.display.setText(self.display.text() + content)

    def unitClicked(self):
        try:
            last_sing_in_curent_expresion = self.display.text().replace(' ', '')[-1]
        except:
            last_sing_in_curent_expresion = None
            
        print (last_sing_in_curent_expresion)
        
        clickedButton = self.sender()
        
        if last_sing_in_curent_expresion in ['+', '-', '/', '*', '(', ')', None]:
            content = clickedButton.text()
        else:
            content = '*' + clickedButton.text()
        self.display.setText(self.display.text() + content)

    def equalClicked(self):
        self.calculate()

    def backspaceClicked(self):
        text = self.display.text()[:-1]
        self.display.setText(text)

    def clear(self):
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
            print (str(e))
            print (str(traceback.format_exc()))
            if self.errorCheckBox.isChecked():
                self.warnings.setText(str(e))
        if not expresion:
            self.display_res.setText("0")
            if self.errorCheckBox.isChecked():
                self.warnings.setText('-')
        self.set_unit_list()
        
        
    def decode(self, expreson):
        expreson = expreson.replace('^', '**')
        return expreson 
        
    def add_to_report(self):
        expresion = self.display.text()
        result = self.display_res.text()
        record = expresion + ' = ' + result
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
                    print (self.result.asUnit(this_unit).asNumber())
                    if self.result.asNumber() == self.result/this_unit:
                        native = unit
                        print ('native', unit )
                except:
                    pass
        calc.unit_ComboBox.setCurrentIndex(calc.unit_ComboBox.findText(native))
        self.block = False
        if default:
            calc.unit_ComboBox.setCurrentIndex(calc.unit_ComboBox.findText(default))
        
    def user_unit_changed(self):
        print ('calll', self.block)
        if not self.block:
            try:
                unit_string = self.unit_ComboBox.currentText()
                user_unit= eval(unit_string)
                print (user_unit)
                self.result = self.result.asUnit(user_unit)
                self.display_res.setText(self.result_string)
                self.add_to_used(unit_string)
            except:
                pass
                
    def add_to_used(self, unit):
        print (unit)
        already_exist = None
        for i in range(len(user_used_units)):
            u = user_used_units[i]
            try:
                eval(u) + eval(unit)
                user_used_units[i] = unit
                already_exist = True
                print(user_used_units)
            except:
                pass
        if not already_exist:
            user_used_units.append(unit)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.autoCheckBox.setChecked(True)
    calc.calculate()
    calc.show()
    sys.exit(app.exec_())
    
'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ...\kipsiCalc.py
'''