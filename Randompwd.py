import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLineEdit, QPushButton, QComboBox, QTextEdit

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('密码生成器')
        self.layout = QVBoxLayout()
        self.uppercaseCheckBox = QCheckBox('A-Z')
        self.lowercaseCheckBox = QCheckBox('a-z')
        self.specialCharsCheckBox = QCheckBox('~!@#$%^&*()_-+={};:\'",./|?><`')
        self.numbersCheckBox = QCheckBox('0-9')
        self.passwordLengthInput = QLineEdit()
        self.passwordLengthInput.setPlaceholderText('密码长度')
        self.numberOfPasswordsComboBox = QComboBox()
        self.numberOfPasswordsComboBox.addItems([str(i) for i in range(1, 100)])
        self.generateButton = QPushButton('生成密码')
        self.generateButton.clicked.connect(self.generatePasswords)
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)
        self.layout.addWidget(self.uppercaseCheckBox)
        self.layout.addWidget(self.lowercaseCheckBox)
        self.layout.addWidget(self.specialCharsCheckBox)
        self.layout.addWidget(self.numbersCheckBox)
        self.layout.addWidget(self.passwordLengthInput)
        self.layout.addWidget(self.numberOfPasswordsComboBox)
        self.layout.addWidget(self.generateButton)
        self.layout.addWidget(self.resultTextEdit)
        self.setLayout(self.layout)

    def generatePasswords(self):
        characters = ''
        if self.uppercaseCheckBox.isChecked():
            characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.lowercaseCheckBox.isChecked():
            characters += 'abcdefghijklmnopqrstuvwxyz'
        if self.specialCharsCheckBox.isChecked():
            characters += '~!@#$%^&*()_-+={};:\'",./|?><`'
        if self.numbersCheckBox.isChecked():
            characters += '0123456789'
        if not characters or not self.passwordLengthInput.text().isdigit():
            self.resultTextEdit.setText("无法生成密码，请选择至少一种字符类型并输入有效的密码长度。")
            return
        passwordLength = int(self.passwordLengthInput.text())
        if passwordLength <= 0:
            self.resultTextEdit.setText("密码长度必须大于0。")
            return
        numberOfPasswords = int(self.numberOfPasswordsComboBox.currentText())
        passwords = ''
        for _ in range(numberOfPasswords):
            password = ''.join(random.choice(characters) for _ in range(passwordLength))
            passwords += password + '\n'

        self.resultTextEdit.setText(passwords)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())

'''
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLineEdit, QPushButton, QComboBox, QTextEdit

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('密码生成器')
        self.layout = QVBoxLayout(self)
        self.create_ui_components()
        self.add_components_to_layout()
    def create_ui_components(self):
        self.create_checkboxes()
        self.create_password_length_input()
        self.create_number_of_passwords_combobox()
        self.create_generate_button()
        self.create_result_text_edit()
    def create_checkboxes(self):
        self.uppercase_checkbox = QCheckBox('A-Z')
        self.lowercase_checkbox = QCheckBox('a-z')
        self.special_chars_checkbox = QCheckBox('~!@#$%^&*()_-+={};:\'",./|?><`')
        self.numbers_checkbox = QCheckBox('0-9')
    def create_password_length_input(self):
        self.password_length_input = QLineEdit()
        self.password_length_input.setPlaceholderText('密码长度')
    def create_number_of_passwords_combobox(self):
        self.number_of_passwords_combobox = QComboBox()
        self.number_of_passwords_combobox.addItems([str(i) for i in range(1, 100)])
    def create_generate_button(self):
        self.generate_button = QPushButton('生成密码')
        self.generate_button.clicked.connect(self.generate_passwords)
    def create_result_text_edit(self):
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
    def add_components_to_layout(self):
        for component in [self.uppercase_checkbox, self.lowercase_checkbox,
                          self.special_chars_checkbox, self.numbers_checkbox,
                          self.password_length_input, self.number_of_passwords_combobox,
                          self.generate_button, self.result_text_edit]:
            self.layout.addWidget(component)
    def generate_passwords(self):
        selected_characters = self.get_selected_characters()
        if not selected_characters or not self.is_valid_password_length():
            self.result_text_edit.setText("无法生成密码，请选择至少一种字符类型并输入有效的密码长度。")
            return
        passwords = self.create_passwords(selected_characters)
        self.result_text_edit.setText(passwords)
    def get_selected_characters(self):
        characters = ''
        if self.uppercase_checkbox.isChecked():
            characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.lowercase_checkbox.isChecked():
            characters += 'abcdefghijklmnopqrstuvwxyz'
        if self.special_chars_checkbox.isChecked():
            characters += '~!@#$%^&*()_-+={};:\'",./|?><`'
        if self.numbers_checkbox.isChecked():
            characters += '0123456789'
        return characters
    def is_valid_password_length(self):
        password_length_str = self.password_length_input.text()
        return password_length_str.isdigit() and int(password_length_str) > 0
    def create_passwords(self, characters):
        password_length = int(self.password_length_input.text())
        number_of_passwords = int(self.number_of_passwords_combobox.currentText())
        return '\n'.join(''.join(random.choice(characters) for _ in range(password_length))
                         for _ in range(number_of_passwords))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())
'''
