import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        btn_list = [["C", "<-", "%", "/"],
                    ["7", "8", "9", "*"],
                    ["4", "5", "6", "-"],
                    ["1", "2", "3", "+"],
                    ["", "0", ".", "="]]

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.vbox.addLayout(self.hbox_input)
        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        for btn_row in btn_list:
            hbox = QHBoxLayout()
            self.vbox.addLayout(hbox)
            for btn_str in btn_row:
                btn = QPushButton(btn_str, self)
                hbox.addWidget(btn)
                btn.clicked.connect(lambda state, numBtn=btn_str: self._button(numBtn))

    def _button(self, param: str):
        try:
            if param == "=":
                line = self.input.text()
                self.input.setText(str(eval(line)))
            elif param == "C":
                self.input.setText("")
            elif param == "<-":
                line = self.input.text()
                self.input.setText(line[:-1])
            else:
                line = self.input.text()
                self.input.setText(line + param)
        except ZeroDivisionError:
            self.input.setText("Сам дели если такой умный(((")


app = QApplication(sys.argv)
win = Calculator()
win.show()
sys.exit(app.exec_())
