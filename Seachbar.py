import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QMainWindow, QTreeView, QLineEdit
from PySide2.QtGui import QFont, QColor, QStandardItemModel, QStandardItem, QKeyEvent


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size= 12, set_bold=False, color = QColor(200,0,0)):
        super().__init__(0)
        
        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

    
class AppDemo(QMainWindow, QtCore.QObject):
    
    signal_qtdo = QtCore.Signal(object)
    
    countries = ['Portugal', 'Madagascar', 'Ukraine', 'Iraq', 'China', 'France', 'Italy', 'Russia', 'Belgium', 'Guatemala', "Colombia", 'Costa Rica', "UkRaInE"]

    def __init__(self, qApp):
        super().__init__()

        self.qApp = qApp
        self.qApp.installEventFilter(self)

        # Initializing
        self.setWindowTitle('World Diagram')
        self.resize(500, 700)
        tree_view = QTreeView()
        tree_view.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        self.root_node = treeModel.invisibleRootItem()

        self.search_bar = QLineEdit(self)
        self.search_bar.resize(500,31)
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setPlaceholderText('Search')
        self.termSearchLen = 0
        self.hidden_rows = self.root_node.clone()
        self.search_bar_text = ''

        tree_view.setModel(treeModel)
        tree_view.expandAll()
        tree_view.doubleClicked.connect(self.get_value)
        self.setCentralWidget(tree_view)
        self.setContentsMargins(0,30,0,0)
        self.adding_countries()

    def adding_countries(self):
        #test 
        for x in range(10000):
            country = f'Mexico {x}'
            self.countries.append(country)

        for country in self.countries:
            country_item = StandardItem(country, 16, True, color=QColor(200,0,0))
            self.root_node.appendRow(country_item)

        usa = StandardItem('America', 16, True)

        ca = StandardItem('California', 14, True, QColor(0,100,0))
        hi = StandardItem("Hawaii", 14, True, QColor(0,100,0))
        nc = StandardItem('North Carolina', 14, True, QColor(0,100,0))
        usa.appendRows([ca, hi, nc])

        sd = StandardItem("San Diego", color=QColor(0,0,100))
        la = StandardItem("Los Angeles", color=QColor(0,0,100))
        sf = StandardItem("San Francisco", color=QColor(0,0,100))
        ca.appendRows([sd, la, sf])

        hon = StandardItem('Honolulu', color=QColor(0,0,100))
        koa = StandardItem('Kona', color=QColor(0,0,100))
        hi.appendRows([hon, koa])

        canada = StandardItem('Canada', 16, True)

        self.root_node.appendRows([usa, canada])

        self.root_node.sortChildren(0)

    def term_search(self, term = str()):

        if (term.__len__() < self.termSearchLen):
            for hidden_row in range(self.hidden_rows.rowCount()-1,-1,-1):
                country_item = self.hidden_rows.child(hidden_row,0)
                if (country_item.text().lower().startswith(term.lower())):
                    country_item.setEnabled(False)
                    self.root_node.appendRow(self.hidden_rows.takeRow(hidden_row))
            self.termSearchLen -= 1
        else:
            self.termSearchLen += 1

        for row in range(self.root_node.rowCount()-1,-1,-1):
            row_item = self.root_node.child(row, 0)
            if (not row_item.text().lower().startswith(term.lower())
                and row_item.isEnabled()):
                self.hidden_rows.appendRow(self.root_node.takeRow(row))
            row_item.setEnabled(True)
            
        self.root_node.sortChildren(0)

    def term_search_enter(self, term = str()):

        if not (term.startswith(self.search_bar_text)):
            for hidden_row in range(self.hidden_rows.rowCount()-1,-1,-1):
                country_item = self.hidden_rows.child(hidden_row,0)
                if (country_item.text().lower().startswith(term.lower())):
                    country_item.setEnabled(False)
                    self.root_node.appendRow(self.hidden_rows.takeRow(hidden_row))

        for row in range(self.root_node.rowCount()-1,-1,-1):
            row_item = self.root_node.child(row, 0)
            if (not row_item.text().lower().startswith(term.lower())):
                # and row_item.isEnabled()): 
                # while row_item.chil           while loop inside
                self.hidden_rows.appendRow(self.root_node.takeRow(row))
            row_item.setEnabled(True)

        self.search_bar_text = term
        self.root_node.sortChildren(0)

    def eventFilter(self, watched, event):
        if isinstance(event, QKeyEvent): # gives me ability to call event.key()
            if (event.key() == 16777220 or event.key() == 16777221):
                self.term_search_enter(self.search_bar.text())
                return True
        return False
        
    def get_value(self, val):
        print(val.data())
        print(val.row())
        print(val.column())

    def close(self):
        pass

if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    demo = AppDemo(qApp)
    qApp.lastWindowClosed.connect(lambda: demo.close())
    demo.show()
    sys.exit(qApp.exec_())