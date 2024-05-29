import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QMainWindow, QTreeView, QLineEdit
from PySide2.QtGui import QFont, QColor, QStandardItemModel, QStandardItem, QKeyEvent

''' This class creates a standard item object that will be inserted into the list. '''
class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size= 12, set_bold=False, color = QColor(200,0,0)):
        super().__init__(0)
        
        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

''' This class runs the demo for our search bar, creating tests and searching for specified objects.'''
class AppDemo(QMainWindow, QtCore.QObject):
    
    signal_qtdo = QtCore.Signal(object)
    
    countries = ['Portugal', 'Madagascar', 'Ukraine', 'Iraq', 'China', 'France', 'Italy', 'Russia', 'Belgium', 'Guatemala', "Colombia", 'Costa Rica', "UkRaInE"]

    # Creates the search bar widget within the app.
    def __init__(self, qApp):
        super().__init__()

        self.qApp = qApp
        self.qApp.installEventFilter(self)

        # Initializing the layout of the screen
        self.setWindowTitle('World Diagram')
        self.resize(500, 700)
        tree_view = QTreeView()
        tree_view.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        self.root_node = treeModel.invisibleRootItem()

        # Initializing the actual search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.resize(500,31)
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setPlaceholderText('Search')
        self.termSearchLen = 0
        self.hidden_rows = self.root_node.clone()
        self.search_bar_text = ''

        # Connecting the page and the searchbar
        tree_view.setModel(treeModel)
        tree_view.expandAll()
        self.setCentralWidget(tree_view)
        self.setContentsMargins(0,30,0,0)
        self.adding_countries()

    # Adding countries to app which are nested in some cases
    def adding_countries(self):
        # creating multiple test objects 
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
        
        # Adding test subjects to root node
        self.root_node.appendRows([usa, canada])

        self.root_node.sortChildren(0)

    ''' This function was the first iteration of my search function
    def term_search_key(self, term = str()):

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
            
        self.root_node.sortChildren(0)'''

    # Searches items and sorts them depending on the term given
    def term_search_enter(self, term = str()):

        # Adds all nodes starting with term to root node
        root_nodes = self.root_node.rowCount()
        if not (term.startswith(self.search_bar_text)):
            for hidden_row in range(self.hidden_rows.rowCount()-1,-1,-1):
                country_item = self.hidden_rows.child(hidden_row,0)
                if (country_item.text().lower().startswith(term.lower())):
                    self.root_node.appendRow(self.hidden_rows.takeRow(hidden_row))

        # Removes all nodes that don't start with term from the root node list
        for row in range(root_nodes -1, -1, -1):
            row_item = self.root_node.child(row, 0)
            if (not row_item.text().lower().startswith(term.lower())):
                self.hidden_rows.appendRow(self.root_node.takeRow(row))

        # Updating the text and visuals of our 
        self.search_bar_text = term
        self.root_node.sortChildren(0)

    # Calls search event if event key is pressed
    def eventFilter(self, watched, event):
        if isinstance(event, QKeyEvent): # gives me ability to call event.key()
            if (event.key() == 16777220 or event.key() == 16777221):
                self.term_search_enter(self.search_bar.text())
                return True
        return False

    # Closing the search bar and feature
    def close(self):
        pass

# Main function which calls everything
if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    demo = AppDemo(qApp)
    qApp.lastWindowClosed.connect(lambda: demo.close())
    demo.show()
    sys.exit(qApp.exec_())
