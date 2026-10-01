import sys
import random
import tempfile
import os

from PySide6 import QtCore, QtWidgets, QtGui

# Импорт и проверка библиотек из requirements.txt
try:
    import numpy as np
    import pandas as pd
    import openpyxl
    import matplotlib
    matplotlib.use("QtAgg")  # Используем бэкенд Qt для Matplotlib
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    LIBS_LOADED = True
    LOAD_ERROR = ""
except Exception as e:
    LIBS_LOADED = False
    LOAD_ERROR = str(e)


class MatplotlibCanvas(FigureCanvas):
    """Виджет для отображения графиков Matplotlib в PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Phage Growth Analyzer — Pre-release Test")
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        # Элементы интерфейса
        self.text = QtWidgets.QLabel("Phage Growth Analyzer Initialized", alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton("Нажать для проверки функций")
        self.status_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        # Компоновка (Layout)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.status_label)

        # Интеграция Matplotlib и проверка работы NumPy / Pandas
        if LIBS_LOADED:
            self.canvas = MatplotlibCanvas(self, width=5, height=3, dpi=100)
            self.layout.addWidget(self.canvas)
            self.plot_test_data()
            self.status_label.setText("Все библиотеки успешно загружены (pandas, numpy, matplotlib, openpyxl)!")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText(f"Ошибка загрузки библиотек: {LOAD_ERROR}")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

        self.button.clicked.connect(self.magic)

    def plot_test_data(self):
        """Тестирование NumPy, Pandas и Matplotlib."""
        # Генерация моковых данных кинетики роста
        time_pts = np.linspace(0, 300, 50)
        od_values = 0.5 + 1.5 / (1 + np.exp(-(time_pts - 100) / 20)) + np.random.normal(0, 0.02, 50)

        df = pd.DataFrame({"Time_min": time_pts, "OD600": od_values})

        self.canvas.axes.clear()
        self.canvas.axes.plot(df["Time_min"], df["OD600"], 'r-', label="Тестовая кривая роста")
        self.canvas.axes.set_title("Тест визуализации (Matplotlib + Pandas)")
        self.canvas.axes.set_xlabel("Время, мин")
        self.canvas.axes.set_ylabel("OD600")
        self.canvas.axes.grid(True)
        self.canvas.axes.legend()
        self.canvas.draw()

    @QtCore.Slot()
    def magic(self):
        # Случайная фраза
        self.text.setText(random.choice(self.hello))

        # Тест создания Excel-файла с помощью pandas и openpyxl
        if LIBS_LOADED:
            try:
                temp_dir = tempfile.gettempdir()
                excel_path = os.path.join(temp_dir, "phage_test_export.xlsx")

                df_test = pd.DataFrame({
                    "Sample": ["A1", "A2", "A3"],
                    "Value": [0.12, 0.15, 0.14]
                })
                df_test.to_excel(excel_path, index=False, engine="openpyxl")

                self.status_label.setText(f"Тестовый Excel упешно создан: {excel_path}")
                self.status_label.setStyleSheet("color: blue;")
            except Exception as e:
                self.status_label.setText(f"Ошибка сохранения Excel: {e}")
                self.status_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
