#!/usr/bin/env python

import math

from strupy.units import*

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget)


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

unit_list = ['mm', 'cm','m', 'ft', 'inch']
unit_list = ['mm2', 'cm2','m2', 'ft2', 'inch2']
unit_list = ['mm3', 'cm3','m3', 'ft3', 'inch3']
unit_list = ['N', 'kN','lbf', 'kip']
unit_list = ['Pa', 'kPa','MPa', 'GPa', 'psi', 'ksi']


class Calculator(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)

        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''

        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True

        self.display = QLineEdit('')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        #self.display.setMaxLength(8)
    
        font = self.display.font()
        font.setPointSize(font.pointSize() + 2)
        self.display.setFont(font)
        
        self.display_res = QLineEdit('')
        self.display_res.setReadOnly(True)
        self.display_res.setAlignment(Qt.AlignRight)
        #self.display_res.setMaxLength(8)

        font = self.display_res.font()
        font.setPointSize(font.pointSize() + 2)
        self.display_res.setFont(font)

        self.digitButtons = []
        
        for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(createButton(str(i),
                    self.basicClicked))

        self.unitButtons = []
        
        for i in unit_list:
            self.unitButtons.append(createButton(str(i),
                    self.basicClicked))

        self.pointButton = createButton(".", self.basicClicked)

        self.backspaceButton = createButton("Backspace",self.backspaceClicked)
        
        self.clearButton = createButton("Clear", self.clear)

        self.divisionButton = createButton("/",self.basicClicked)
        self.timesButton = createButton("*",self.basicClicked)
        self.minusButton = createButton("-", self.basicClicked)
        self.plusButton = createButton("+", self.basicClicked)
        self.squareRootButton = createButton("**",self.basicClicked)
        
        self.brackedopenButton = createButton("(",self.basicClicked)
        self.brackedcloseButton = createButton(")",self.basicClicked)

        self.equalButton = createButton("=", self.equalClicked)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 6)
        
        mainLayout.addWidget(self.display_res, 0, 6, 1, 10)
        
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)


        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)
            

        for i in range(0, 4):
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

        self.display.setWindowTitle("kipsiCalc")     

    def basicClicked(self):
        clickedButton = self.sender()
        content = clickedButton.text()
        self.display.setText(self.display.text() + content)
        self.equalClicked()
        
    def equalClicked(self):
        result = eval(self.display.text())
        self.display_res.setText(str(result))

    def backspaceClicked(self):
        text = self.display.text()[:-1]
        self.display.setText(text)

    def clear(self):
        self.display.setText('')

    def calculate(self):
        pass

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())