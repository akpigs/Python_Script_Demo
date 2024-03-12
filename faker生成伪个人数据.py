import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QCheckBox, \
    QGridLayout
from faker import Faker


class DetailedFakerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.faker = Faker('zh_CN')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('伪身份数据生成')
        self.setGeometry(800, 800, 1000, 700)
        layout = QVBoxLayout()
        self.setLayout(layout)
        grid_layout = QGridLayout()

        self.checkBoxes = {
            '姓名': QCheckBox('姓名'),
            '性': QCheckBox('姓'),
            '名': QCheckBox('名'),
            '出生日期': QCheckBox('出生日期'),
            '联系方式': QCheckBox('联系方式'),
            '身份证号': QCheckBox('身份证号'),
            '银行卡号': QCheckBox('银行卡号'),
            '信用卡供应商': QCheckBox('信用卡供应商'),
            '密码': QCheckBox('密码'),
            '地址': QCheckBox('地址'),
            '公司': QCheckBox('公司'),
            '工作': QCheckBox('工作'),
            '邮件': QCheckBox('邮件'),
            '国家': QCheckBox('国家'),
            '城市': QCheckBox('城市'),
            '车辆识别码（VIN）': QCheckBox('车辆识别码（VIN）'),
            '车牌号': QCheckBox('车牌号'),
            'IPV4': QCheckBox('IPV4'),
            '网址': QCheckBox('网址'),
            '条形码': QCheckBox('条形码'),
            '用户代理': QCheckBox('用户代理'),
        }

        row, col = 0, 0
        for name, checkBox in self.checkBoxes.items():
            checkBox.setChecked(True)  # 默认勾选
            grid_layout.addWidget(checkBox, row, col)
            col += 1
            if col >= 6:  # 每行放置6个复选框，可根据需要调整
                row += 1
                col = 0

        layout.addLayout(grid_layout)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setMinimumSize(960, 500)
        layout.addWidget(self.textEdit)

        # 按钮
        buttons_layout = QHBoxLayout()
        self.generateButton = QPushButton('生成数据')
        self.generateButton.clicked.connect(self.generateData)
        buttons_layout.addWidget(self.generateButton)

        self.copyButton = QPushButton('复制到剪贴板')
        self.copyButton.clicked.connect(self.copyToClipboard)
        buttons_layout.addWidget(self.copyButton)

        layout.addLayout(buttons_layout)

    def generateData(self):
        text = ""
        for name, cb in self.checkBoxes.items():
            if cb.isChecked():
                text += f"{name}：{self.generateFakerData(name)}\n"
        self.textEdit.setText(text)

    def generateFakerData(self, name):
        # 根据复选框名称生成相应的数据
        data_mapping = {
            '姓名': self.faker.name,
            '性': self.faker.last_name,
            '名': self.faker.first_name,
            '出生日期': lambda: self.faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            '联系方式': self.faker.phone_number,
            '身份证号': self.faker.ssn,
            '银行卡号': self.faker.credit_card_number,
            '信用卡供应商': self.faker.credit_card_provider,
            '密码': lambda: self.faker.password(length=20, special_chars=True, digits=True, upper_case=True,
                                              lower_case=True),
            '地址': self.faker.address,
            '公司': self.faker.company,
            '工作': self.faker.job,
            '邮件': self.faker.company_email,
            '国家': self.faker.country,
            '城市': self.faker.city,
            '车辆识别码（VIN）': self.faker.vin,
            '车牌号': self.faker.license_plate,
            'IPV4': self.faker.ipv4,
            '网址': self.faker.url,
            '条形码': self.faker.ean13,
            '用户代理': self.faker.user_agent,
        }
        func = data_mapping.get(name, lambda: "未知数据类型")
        return func()

    def copyToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textEdit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetailedFakerTool()
    window.show()
    sys.exit(app.exec_())
