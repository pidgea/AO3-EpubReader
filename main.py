import ebooklib
from ebooklib import epub
from PyQt5.QtWidgets import QMainWindow, QApplication
from PytQt5.uic import loadUiType
import sys

class Main(QMainWindow):
    def __init__(self):
        super(Main, self). __init__()
        loadUi("demo.ui", self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()

# read the named file
book = epub.read_epub('pg84.epub')

# extract everything within the body content of the file, print to console
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print('==================================')
        print('Name : ', item.get_name())
        print('----------------------------------')
        print(item.get_body_content())
        print('==================================')
