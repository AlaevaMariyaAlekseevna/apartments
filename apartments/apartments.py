import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
class ApartmentManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApartmentManager, self).__init__()
        uic.loadUi('apartments.ui', self)
        self.filename = "apartments.txt"
        self.data = self.load_data()
        # Подключаем кнопки
        self.addButton.clicked.connect(self.add_record)
        self.deleteButton.clicked.connect(self.delete_record)
        self.editButton.clicked.connect(self.edit_record)
        self.updateButton.clicked.connect(self.display_data)
        self.setup_table()# Настраиваем таблицу
        self.apply_styles()# Применяем стили
        self.display_data()# Отображаем данные при запуске
    def apply_styles(self):
        """Применение CSS стилей"""
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5;}
            QTabWidget::pane { border: 1px solid #ccc; background: white;}
            QTabBar::tab { padding: 8px; background: #e0e0e0; border: 1px solid #ccc;}
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #4CAF50;}
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px 16px; font-size: 14px;}
            QPushButton:hover { background-color: #45a049;}
            QLineEdit, QTextEdit { border: 1px solid #ccc; padding: 5px;}
            QTableWidget { gridline-color: #ddd; border: 1px solid #ccc;}
            QTableWidget QHeaderView::section { background-color: #4CAF50; color: white; padding: 5px; border: none;}
        """)
    def setup_table(self):
        """Настройка таблицы для отображения данных"""
        headers = [ "№", "Фамилия", "Имя", "Отчество", "Комнат", "Общая пл.", "Жилая пл.", "Этаж", "Телефон", "Цена", "Адрес"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setAlternatingRowColors(True)
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [line.strip().split('&') for line in file if line.strip()]
        except FileNotFoundError:
            return []
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            for record in self.data:
                file.write('&'.join(record) + '\n')
    def display_data(self):
        """Отображение данных в текстовом поле и таблице"""
        self.outputText.clear()# Очищаем перед обновлением
        if not self.data:
            self.outputText.setText("Нет данных о квартирах.")
            self.tableWidget.setRowCount(0)
            return
        headers = [ "№", "Фамилия", "Имя", "Отчество", "Комнат", "Общая пл.", "Жилая пл.", "Этаж", "Телефон", "Цена", "Адрес"]# Отображение в текстовом поле
        header_line = "\t".join(headers) + "\n" + "-" * 100
        self.outputText.append(header_line)
        for idx, record in enumerate(self.data, 1):
            self.outputText.append(f"{idx}\t" + "\t".join(record))
        # Отображение в таблице
        self.tableWidget.setRowCount(len(self.data))
        for row_idx, record in enumerate(self.data):
            self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
            for col_idx in range(1, 11):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(record[col_idx - 1]))
                self.tableWidget.resizeColumnsToContents()
    def add_record(self):
        """Добавление новой записи"""
        fields = [
            self.lineEdit_4.text(),  # Фамилия
            self.lineEdit_5.text(),  # Имя
            self.lineEdit_6.text(),  # Отчество
            self.lineEdit_7.text(),  # Комнат
            self.lineEdit_8.text(),  # Общая площадь
            self.lineEdit_9.text(),  # Жилая площадь
            self.lineEdit_10.text(),  # Этаж
            self.lineEdit_11.text(),  # Телефон
            self.lineEdit_12.text(),  # Цена
            self.lineEdit_13.text()  # Адрес
        ]
        if not all(fields):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
        self.data.append(fields)
        self.save_data()
        for line_edit in [
            self.lineEdit_4, self.lineEdit_5, self.lineEdit_6,
            self.lineEdit_7, self.lineEdit_8, self.lineEdit_9,
            self.lineEdit_10, self.lineEdit_11, self.lineEdit_12,
            self.lineEdit_13
        ]:
            line_edit.clear()
        self.display_data()
        QMessageBox.information(self, "Успех", "Запись добавлена!")
    def delete_record(self):
        """Удаление записи по индексу"""
        try:
            index = int(self.deleteIndexEdit.text()) - 1
            if 0 <= index < len(self.data):
                del self.data[index]
                self.save_data()
                self.deleteIndexEdit.clear()
                self.display_data()
                QMessageBox.information(self, "Успех", "Запись удалена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный индекс записи!")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер записи!")
    def edit_record(self):
        """Редактирование записи по индексу"""
        try:
            index = int(self.editIndexEdit.text()) - 1
            if 0 <= index < len(self.data):
                new_value = self.editValueEdit.text()
                if not new_value:
                    QMessageBox.warning(self, "Ошибка", "Введите новое значение!")
                    return
                self.data[index][0] = new_value
                self.save_data()
                self.editIndexEdit.clear()
                self.editValueEdit.clear()
                self.display_data()
                QMessageBox.information(self, "Успех", "Запись изменена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный индекс записи!")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер записи!")
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ApartmentManager()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()