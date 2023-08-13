import sys
import ebooklib
from ebooklib import epub
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
#imports

class Main(QMainWindow): #loading the gui shenanigans, so make a new class for it
    def __init__(self):
        super(Main, self). __init__()
        loadUi("demo.ui", self) #load the specified .ui file 

        #when the 'x' button is pressed, call function connected to it
        self.actionOpen.triggered.connect(self.openFile) 


    def openFile(self): # new function!!!!!!!
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text files (*.txt)') # fname variable = the file opened within the dialog(directory title, which directory, specified file type)
        self.setWindowTitle(fname[0]) # set the window title to selected fname
        with open(fname[0], 'r') as f: # return
            filetext = f.read()
            self.textEdit.setText(filetext)
        self.current_path = fname[0]
    from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()


book = epub.read_epub('pg84.epub') #assign epub file to book variable

for item in book.get_items(): # 
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print('==================================') # these act line breaks in the console
        print('Name : ', item.get_name())
        print('----------------------------------')
        print(item.get_body_content())
        print('==================================')
