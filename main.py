from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from bs4 import BeautifulSoup
from PyQt5.uic import loadUi
import ebooklib
from ebooklib import epub
import sys 

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("tut.ui", self)

        self.actionOpen.triggered.connect(self.openFile)



    def openFile(self): # selecting the epub file
        print("BUTTON CLICKED!") # that button was CLICKED!!!

        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'EPUB files (*.epub)') # opens file dialog, shoves epub into a variable (brackets are file dialogue parameters)
        self.setWindowTitle(fname[0]) # window title 2 whatever file name is :)

        book = epub.read_epub(fname[0]) 

        with open(fname[0], 'r') as f:
            contents = f.read()

            soup = BeautifulSoup(contents, "html.parser")
            for child in soup.descendants:
                    if child.name:
                         print(child.name)

        for items in book.get_items():
            if items.get_type() == ebooklib.ITEM_DOCUMENT:
                bodyContent = items.get_body_content()


                # self.textEdit.setText(items)
              # print (items.get_body_content())
              #  print ('it worked loser')



""""
soupers idea
   def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return ''.join(text)
"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()