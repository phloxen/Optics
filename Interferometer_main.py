from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import QPainter, QColor
from color import wavelength_to_rgb
from Interferometer import Ui_Form
from PySide6.QtCore import QTimer, QRect
import numpy as np


def draw_arc(painter, x_1, y_1, x_2, y_2):
    # 获取当前画笔
    pen = painter.pen()
    painter.setPen(pen)
    x = x_2 - x_1
    y = y_2 - y_1
    # 计算 r
    r = np.sqrt(x ** 2 + y ** 2)
    # 计算 theta，以弧度为单位
    theta = np.arctan2(y, x)
    # 将 theta 转换为角度（如果需要）
    theta_degrees = - np.degrees(theta)
    start_angle = (theta_degrees - 30) * 16
    span_angle = 60 * 16
    for i in range(int(r // 10)):
        # 绘制圆弧所需的矩形框，中心在(x_1, y_1)，半径为r
        rect = QRect(x_1 - r, y_1 - r, 2 * r, 2 * r)
        painter.drawArc(rect, start_angle, span_angle)
        r = r - 10


def standard(number, length):
    return 2 * np.arctan(number) * length / np.pi


class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.setupUi(self)
        self.bind()

        self.contants_1 = 700  # 波长/nm
        self.contants_2 = 2  # 缝数量/个
        self.contants_3 = 2  # 缝间距/mm
        self.contants_4 = 1  # 缝屏距/m

        # 初始化
        self.isWave = False  # 光波模式
        self.isFunction = False  # 函数显示
        self.pushButton_stop.setVisible(False)
        self.pushButton_stop.setStyleSheet("background-color: red;")
        self.delta_y = 0
        self.line_drawn = False
        self.line_color = QColor(0, 0, 0)  # 默认颜色为黑色
        self.r = 0
        self.g = 0
        self.b = 0
        self.plant()

    def bind(self):
        # 光波模式
        self.radioButton.toggled.connect(self.WaveChange)
        self.radioButton_2.toggled.connect(self.WaveChange)
        # 显示函数
        self.checkBox.stateChanged.connect(self.Function)
        # 自动递增
        self.pushButton_1.clicked.connect(self.progress_1)
        self.pushButton_2.clicked.connect(self.progress_2)
        self.pushButton_3.clicked.connect(self.progress_3)
        self.pushButton_4.clicked.connect(self.progress_4)
        self.pushButton_stop.clicked.connect(self.stop)

        # 滑动条
        self.horizontalSlider_1.valueChanged.connect(self.valueChanged_1)
        self.horizontalSlider_2.valueChanged.connect(self.valueChanged_2)
        self.horizontalSlider_3.valueChanged.connect(self.valueChanged_3)
        self.horizontalSlider_4.valueChanged.connect(self.valueChanged_4)

        # 值
        self.doubleSpinBox_14.valueChanged.connect(self.SpinBoxChanged_1)
        self.spinBox_24.valueChanged.connect(self.SpinBoxChanged_2)
        self.doubleSpinBox_34.valueChanged.connect(self.SpinBoxChanged_3)
        self.doubleSpinBox_44.valueChanged.connect(self.SpinBoxChanged_4)

        # 上下限
        self.doubleSpinBox_11.valueChanged.connect(self.downChanged_1)
        self.doubleSpinBox_12.valueChanged.connect(self.upChanged_1)
        self.spinBox_21.valueChanged.connect(self.downChanged_2)
        self.spinBox_22.valueChanged.connect(self.upChanged_2)
        self.doubleSpinBox_31.valueChanged.connect(self.downChanged_3)
        self.doubleSpinBox_32.valueChanged.connect(self.upChanged_3)
        self.doubleSpinBox_41.valueChanged.connect(self.downChanged_4)
        self.doubleSpinBox_42.valueChanged.connect(self.upChanged_4)

    def WaveChange(self):
        if self.radioButton.isChecked():
            self.isWave = False  # 光线模式
            self.plant()
        else:
            self.isWave = True  # 光波模式
            self.plant()

    def Function(self):
        if self.checkBox.isChecked():
            self.isFunction = True
            self.plant()
        else:
            self.isFunction = False
            self.plant()

    def stop(self):
        self.timer.stop()  # 如果条件不再满足，停止定时器
        self.pushButton_stop.setVisible(False)

    def progress_1(self):
        self.pushButton_stop.setVisible(True)
        # 停止任何之前的定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_1)
        self.timer.start(100)  # 每100毫秒执行一次

    def update_progress_1(self):
        if self.doubleSpinBox_12.value() > self.doubleSpinBox_14.value():
            value = self.doubleSpinBox_13.value() + self.doubleSpinBox_14.value()
            self.horizontalSlider_1.setValue(value)
            self.doubleSpinBox_14.setValue(value)
            self.contants_1 = value
            self.plant()
        else:
            self.timer.stop()  # 如果条件不再满足，停止定时器
            self.pushButton_stop.setVisible(False)

    def progress_2(self):
        self.pushButton_stop.setVisible(True)
        # 停止任何之前的定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_2)
        self.timer.start(100)  # 每100毫秒执行一次

    def update_progress_2(self):
        if self.spinBox_22.value() > self.spinBox_24.value():
            value = self.spinBox_23.value() + self.spinBox_24.value()
            self.horizontalSlider_2.setValue(value)
            self.spinBox_24.setValue(value)
            self.contants_2 = value
            self.plant()
        else:
            self.timer.stop()  # 如果条件不再满足，停止定时器
            self.pushButton_stop.setVisible(False)

    def progress_3(self):
        self.pushButton_stop.setVisible(True)
        # 停止任何之前的定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_3)
        self.timer.start(100)  # 每100毫秒执行一次

    def update_progress_3(self):
        if self.doubleSpinBox_32.value() > self.doubleSpinBox_34.value():
            value = self.doubleSpinBox_33.value() + self.doubleSpinBox_34.value()
            self.horizontalSlider_3.setValue(value * 100)
            self.doubleSpinBox_34.setValue(value)
            self.contants_3 = value
            self.plant()
        else:
            self.timer.stop()  # 如果条件不再满足，停止定时器
            self.pushButton_stop.setVisible(False)

    def progress_4(self):
        self.pushButton_stop.setVisible(True)
        # 停止任何之前的定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_4)
        self.timer.start(100)  # 每100毫秒执行一次

    def update_progress_4(self):
        if self.doubleSpinBox_42.value() > self.doubleSpinBox_44.value():
            value = self.doubleSpinBox_43.value() + self.doubleSpinBox_44.value()
            self.horizontalSlider_4.setValue(value * 100)
            self.doubleSpinBox_44.setValue(value)
            self.contants_4 = value
            self.plant()
        else:
            self.timer.stop()  # 如果条件不再满足，停止定时器
            self.pushButton_stop.setVisible(False)

    def downChanged_1(self):
        value = self.doubleSpinBox_11.value()
        self.horizontalSlider_1.setMinimum(value)
        self.doubleSpinBox_14.setMinimum(value)

    def upChanged_1(self):
        value = self.doubleSpinBox_12.value()
        self.horizontalSlider_1.setMaximum(value)
        self.doubleSpinBox_14.setMaximum(value)

    def downChanged_2(self):
        value = self.spinBox_21.value()
        self.horizontalSlider_2.setMinimum(value)
        self.spinBox_24.setMinimum(value)

    def upChanged_2(self):
        value = self.spinBox_22.value()
        self.horizontalSlider_2.setMaximum(value)
        self.spinBox_24.setMaximum(value)

    def downChanged_3(self):
        value = self.doubleSpinBox_31.value()
        self.horizontalSlider_3.setMinimum(value * 100)
        self.doubleSpinBox_34.setMinimum(value)

    def upChanged_3(self):
        value = self.doubleSpinBox_32.value()
        self.horizontalSlider_3.setMaximum(value * 100)
        self.doubleSpinBox_34.setMaximum(value)

    def downChanged_4(self):
        value = self.doubleSpinBox_41.value()
        self.horizontalSlider_4.setMinimum(value * 100)
        self.doubleSpinBox_44.setMinimum(value)

    def upChanged_4(self):
        value = self.doubleSpinBox_42.value()
        self.horizontalSlider_4.setMaximum(value * 100)
        self.doubleSpinBox_44.setMaximum(value)

    def SpinBoxChanged_1(self):
        value = self.doubleSpinBox_14.value()
        self.horizontalSlider_1.setValue(value)
        self.contants_1 = value
        self.plant()

    def SpinBoxChanged_2(self):
        value = self.spinBox_24.value()
        self.horizontalSlider_2.setValue(value)
        self.contants_2 = value
        self.plant()

    def SpinBoxChanged_3(self):
        value = self.doubleSpinBox_34.value()
        self.horizontalSlider_3.setValue(value * 100)
        self.contants_3 = value
        self.plant()

    def SpinBoxChanged_4(self):
        value = self.doubleSpinBox_44.value()
        self.horizontalSlider_4.setValue(value * 100)
        self.contants_4 = value
        self.plant()

    def valueChanged_1(self):
        value = self.horizontalSlider_1.value()
        self.doubleSpinBox_14.setValue(value)
        self.contants_1 = value
        self.plant()

    def valueChanged_2(self):
        value = self.horizontalSlider_2.value()
        self.spinBox_24.setValue(value)
        self.contants_2 = value
        self.plant()

    def valueChanged_3(self):
        value = self.horizontalSlider_3.value() / 100
        self.doubleSpinBox_34.setValue(value)
        self.contants_3 = value
        self.plant()

    def valueChanged_4(self):
        value = self.horizontalSlider_4.value() / 100
        self.doubleSpinBox_44.setValue(value)
        self.contants_4 = value
        self.plant()

    def plant(self):
        # 计算delta_y
        self.delta_y = int((self.contants_4 * (self.contants_1 * 10 ** -9) / (self.contants_3 * 10 ** -3)) * 10 ** 5)
        # print(delta_y)

        try:
            rgb = wavelength_to_rgb(self.contants_1)  # 获取 RGB 值
            self.r = rgb[0]
            self.g = rgb[1]
            self.b = rgb[2]
            self.line_color = QColor(rgb[0], rgb[1], rgb[2])  # 创建 QColor 对象
            self.line_drawn = True  # 设置标记为 True
            self.update()  # 请求重绘窗口
        except ValueError:
            print("请输入有效的波长值！")  # 错误处理

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)  # 开启抗锯齿

        # 获取当前画笔
        pen = qp.pen()
        pen.setColor(QColor(0, 0, 0))  # 黑色
        pen.setWidth(1)
        qp.setPen(pen)
        qp.drawLine(20 + 50, 20 + 30, 20 + 50, 300 + 30)
        qp.drawLine(20 + 50, 300 + 30, 480 + 50, 300 + 30)
        qp.drawLine(480 + 50, 20 + 30, 480 + 50, 300 + 30)
        qp.drawLine(20 + 50, 20 + 30, 480 + 50, 20 + 30)

        # 获取当前画笔
        pen = qp.pen()
        pen.setColor(QColor(0, 0, 0))  # 黑色
        pen.setWidth(4)
        qp.setPen(pen)

        # 绘制光屏
        qp.drawLine(333 + 50, 30 + 30, 333 + 50, 280 + 30)

        # 绘制双缝
        # for y in [107, 141, 175]:
        #     qp.drawLine(166, y, 166, y + 27)
        x_0 = 250 - standard(self.contants_4, 100)
        qp.drawLine(x_0, 107 + 30, x_0, 202 + 30)

        # 绘制单缝
        for y in [130, 160]:
            qp.drawLine(83 + 50, y + 30, 83 + 50, y + 20 + 30)

        # 绘制用户选择的颜色线
        if self.line_drawn:
            pen.setColor(self.line_color)
            pen.setWidth(1)
            qp.setPen(pen)
            if self.isWave:  # 光波模式
                # 绘制入射光线
                for y in [130, 140, 150, 160, 170, 180]:
                    draw_arc(qp, 40 + 50, y + 30, 80 + 50, y + 30)
                    draw_arc(qp, 80 + 50, y + 30, 77 + 50, y + 3 + 30)
                    draw_arc(qp, 80 + 50, y + 30, 77 + 50, y - 3 + 30)
                # 绘制分光
                n = self.contants_2
                max_length = 96 / (n - 1)
                standard_y = standard(self.doubleSpinBox_34.value(), max_length)
                y_0 = []
                for i in range(n):
                    y_0 += [185 + (i - ((n - 1) / 2)) * standard_y]
                for y in y_0:
                    draw_arc(qp, 83 + 50, 155 + 30, x_0, y)
                # 绘制干涉
                if self.delta_y == 0:
                    QMessageBox.information(self, '警告', '超出阈值', QMessageBox.StandardButton.Ok)
                    app.quit()
                n = int(125 // self.delta_y)
                for i in range(-n, n + 1):
                    for y in y_0:
                        draw_arc(qp, x_0, y, 333 + 50, 155 + 30 + i * self.delta_y)
            else:  # 光线模式（默认）
                # 绘制入射光线
                for y in [130, 140, 150, 160, 170, 180]:
                    qp.drawLine(40 + 50, y + 30, 80 + 50, y + 30)
                    qp.drawLine(80 + 50, y + 30, 77 + 50, y + 3 + 30)
                    qp.drawLine(80 + 50, y + 30, 77 + 50, y - 3 + 30)
                # 绘制分光
                n = self.contants_2
                max_length = 96 / (n - 1)
                standard_y = standard(self.doubleSpinBox_34.value(), max_length)
                y_0 = []
                for i in range(n):
                    y_0 += [185 + (i - ((n - 1) / 2)) * standard_y]
                for y in y_0:
                    qp.drawLine(83 + 50, 155 + 30, x_0, y)
                # 绘制干涉
                if self.delta_y == 0:
                    QMessageBox.information(self, '警告', '超出阈值', QMessageBox.StandardButton.Ok)
                    app.quit()
                n = int(125 // self.delta_y)
                for i in range(-n, n + 1):
                    for y in y_0:
                        qp.drawLine(x_0, y, 333 + 50, 155 + 30 + i * self.delta_y)
            # 绘制干涉图形
            qp.setRenderHint(QPainter.Antialiasing, False)  # 开启抗锯齿
            fun_xy = [[], []]
            for y in range(-125, 125):
                # 计算渐变值
                x = 3.14159 * y / self.delta_y
                n = self.contants_2
                if x == 0:
                    value = 255
                else:
                    value = int((((np.sin(n * x)) ** 2) / ((n ** 2) * (np.sin(x)) ** 2)) * 255)
                color = QColor(self.r * value // 255, self.g * value // 255, self.b * value // 255)
                qp.setPen(color)
                qp.drawLine(350 + 50, 155 + 30 + y, 400 + 50, 155 + 30 + y)
                if self.isFunction:
                    fun_xy[0] += [int(470 + value / 5)]
                    fun_xy[1] += [155 + 30 + y]
            qp.setRenderHint(QPainter.Antialiasing, True)  # 开启抗锯齿

            # 绘制干涉图形函数
            if self.isFunction:
                color = QColor(self.r, self.g, self.b)
                qp.setPen(color)
                for i in range(len(fun_xy[0]) - 1):
                    qp.drawLine(fun_xy[0][i], fun_xy[1][i], fun_xy[0][i + 1], fun_xy[1][i + 1])


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
