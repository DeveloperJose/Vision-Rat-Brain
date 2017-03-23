# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView

class ResultsDialog(QDialog):
    def __init__(self, filename, matches, parent=None):
        super(ResultsDialog, self).__init__(parent)

        self.setWindowTitle("Results for " + filename)

        self.filename = filename
        self.matches = matches
        self.labels = ['Plate', 'Match Count', 'Inlier Count', 'Largest Distance', '', '']

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setMinimumWidth(750)
        self.table.setMinimumHeight(450)
        self.table.setRowCount(len(matches))
        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)

        self.matches = sorted(matches, key=lambda x: x.comparison_key(), reverse=True)
        row = 0
        for match in self.matches:
            string_repr = match.to_string_array()
            self.table.setItem(row, 0, QTableWidgetItem(string_repr[0]))
            self.table.setItem(row, 1, QTableWidgetItem(string_repr[1]))
            self.table.setItem(row, 2, QTableWidgetItem(string_repr[2]))
            self.table.setItem(row, 3, QTableWidgetItem(string_repr[3]))
            row += 1

        self.table.doubleClicked.connect(self.on_double_click_table)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def on_double_click_table(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))

        if (len(rows) > 0):
            row = rows[0]
            match = self.matches[row]

            im_result = match.result

            image_diag = ImageDialog(im=im_result)
            image_diag.show()


class ImageDialog(QDialog):
    def __init__(self, im, parent=None):
        super(ImageDialog, self).__init__(parent)

        self.setWindowTitle("Image")
        layout = QVBoxLayout()

        from graph import Graph
        self.canvas = Graph(self, width=5, height=5, dpi=100)
        self.canvas.is_interactive = False
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.canvas.imshow(im)