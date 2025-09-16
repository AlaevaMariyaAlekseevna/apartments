import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
class ApartmentManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApartmentManager, self).__init__()
        uic.loadUi('apartments.ui', self)
        self.filename = "apartments.txt"
        self.data = self.load_data()
        # Сохраняем оригинальные данные для сброса сортировки
        self.original_data = self.data.copy()
        # Подключаем кнопки
        self.addButton.clicked.connect(self.add_record)
        self.deleteButton.clicked.connect(self.delete_record)
        self.editButton.clicked.connect(self.edit_record)
        self.updateButton.clicked.connect(self.display_data)
        self.sortButton.clicked.connect(self.sort_by_surname)
        self.resetSortButton.clicked.connect(self.reset_sort)
        self.searchButton.clicked.connect(self.search_records)
        # Настраиваем таблицу
        self.setup_table()
        # Применяем стили
        self.apply_styles()
        # Отображаем данные при запуске
        self.display_data()
    def apply_styles(self):
        """Применение CSS стилей"""
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5;}
            QTabWidget::pane { border: 1px solid #ccc; background: white;}
            QTabBar::tab { padding: 8px; background: #e0e0e0; border: 1px solid #ccc;}
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #4CAF50;}
            QPushButton { background-color: #41992D; color: white; border: none; padding: 8px 16px; font-size: 14px;}
            QPushButton:hover { background-color: #41992D;}
            QLineEdit, QTextEdit { border: 1px solid #ccc; padding: 5px;}
            QTableWidget { gridline-color: #ddd; border: 1px solid #ccc;}
            QTableWidget QHeaderView::section { background-color: #41992D; color: white; padding: 5px; border: none;}
            QComboBox { border: 1px solid #ccc; padding: 5px; min-width: 150px;}
        """)
    def setup_table(self):
        """Настройка таблицы для отображения данных"""
        headers = ["№", "Фамилия", "Имя", "Отчество", "Комнат", "Общая пл.", "Жилая пл.", "Этаж", "Телефон", "Цена", "Адрес"]
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
    def display_data(self, data_to_display=None):
        """Отображение данных в текстовом поле и таблице"""
        if data_to_display is None:
            data_to_display = self.data
        # Очищаем перед обновлением
        self.outputText.clear()
        if not data_to_display:
            self.outputText.setText("Нет данных о квартирах.")
            self.tableWidget.setRowCount(0)
            return
        headers = ["№", "Фамилия", "Имя", "Отчество", "Комнат", "Общая пл.", "Жилая пл.", "Этаж", "Телефон", "Цена",  "Адрес"]
        # Отображение в текстовом поле
        header_line = "\t".join(headers) + "\n" + "-" * 100
        self.outputText.append(header_line)
        for idx, record in enumerate(data_to_display, 1):
            self.outputText.append(f"{idx}\t" + "\t".join(record))
        # Отображение в таблице
        self.tableWidget.setRowCount(len(data_to_display))
        for row_idx, record in enumerate(data_to_display):
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
        # Проверка заполненности полей
        if not all(fields):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
        # Проверка числовых полей
        try:
            int(fields[3])  # Комнат
            float(fields[4])  # Общая площадь
            float(fields[5])  # Жилая площадь
            int(fields[6])  # Этаж
            float(fields[8])  # Цена
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некоторые поля должны содержать числовые значения!")
            return
        # Проверка поля "Телефон"
        if fields[7].lower() not in ['да', 'нет']:
            QMessageBox.warning(self, "Ошибка", "Поле 'Телефон' должно содержать 'да' или 'нет'!")
            return
        self.data.append(fields)
        # Обновляем оригинальные данные
        self.original_data.append(fields)
        self.save_data()
        # Очищаем поля ввода
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
                del self.original_data[index]  # Обновляем оригинальные данные
                self.save_data()
                self.deleteIndexEdit.clear()
                self.display_data()
                QMessageBox.information(self, "Успех", "Запись удалена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный индекс записи!")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер записи!")
    def edit_record(self):
        """Редактирование записи по индексу и выбранному полю"""
        try:
            index = int(self.editIndexEdit.text()) - 1
            if 0 <= index < len(self.data):
                field_index = self.fieldComboBox.currentIndex()
                new_value = self.editValueEdit.text()
                if not new_value:
                    QMessageBox.warning(self, "Ошибка", "Введите новое значение!")
                    return
                # Проверки для числовых полей
                if field_index in [3, 6]:  # Комнат или Этаж
                    try:
                        int(new_value)
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Это поле должно содержать целое число!")
                        return
                elif field_index in [4, 5, 8]:  # Площади или Цена
                    try:
                        float(new_value)
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Это поле должно содержать число!")
                        return
                elif field_index == 7:  # Телефон
                    if new_value.lower() not in ['да', 'нет']:
                        QMessageBox.warning(self, "Ошибка", "Поле 'Телефон' должно содержать 'да' или 'нет'!")
                        return
                self.data[index][field_index] = new_value
                # Обновляем оригинальные данные
                self.original_data[index][field_index] = new_value
                self.save_data()
                self.editIndexEdit.clear()
                self.editValueEdit.clear()
                self.display_data()
                QMessageBox.information(self, "Успех", "Запись изменена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный индекс записи!")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер записи!")
    def sort_by_surname(self):
        """Сортировка данных по фамилии"""
        self.data.sort(key=lambda x: x[0].lower())
        self.display_data()
    def reset_sort(self):
        """Сброс сортировки к исходному порядку"""
        self.data = self.original_data.copy()
        self.display_data()
    def search_records(self):
        """Поиск записей по ключевому слову"""
        search_text = self.searchEdit.text().lower().strip()
        if not search_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст для поиска!")
            return
        found_records = []
        for record in self.original_data:
            # Ищем во всех полях записи
            if any(search_text in field.lower() for field in record):
                found_records.append(record)
        if found_records:
            self.display_data(found_records)
            QMessageBox.information(self, "Результаты поиска", f"Найдено записей: {len(found_records)}")
        else:
            QMessageBox.information(self, "Результаты поиска", "Записи не найдены")
            self.display_data()
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ApartmentManager()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
