from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup
import sys, os, ebooklib
from ebooklib import epub 
    
class Main(QMainWindow):
    def __init__(self): #INITIALISE!
        super(Main, self).__init__()
        loadUi("tut.ui", self) # loads the main window 

        title = "WOMSE-R"
        self.setWindowTitle(title) # sets window to be called WOMSE-R :) 
        self.resize(600, 650)
        
        self.actionConvert.triggered.connect(self.convertFile) # trigger function on button press
        self.actionOpen_Window.triggered.connect(self.openHTMLWindow)
        self.window_2 = SecondWindow() # have to mention for function below

    def openHTMLWindow(self):
        self.window_2.show() # this is basically a portal to access the next window
        # couldn't figure how to transfer fname[0] across windows
        # as in, to be able to open the HTMLViewer from the file dialog in the main window
        # also with the way i connected the file to the GUI was convenient for time
        # all the tutorials were for .ui's converted into .py
        
    def convertFile(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'EPUB files (*.epub)') # opens file dialog, epub specified
        self.setWindowTitle(fname[0]) # sets window name to selected file's path
        output_dir = 'output_html/' 
        os.makedirs(output_dir, exist_ok=True) # allows creation of folder of line above 

        book = epub.read_epub(fname[0]) # selected file data GET! shove into book variable

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_body_content() # book text is now in the content variable
                
                soup = BeautifulSoup(content, 'html.parser') # soup variable contains... the Soup (content is parsed with integrated html parser)

                content_html = str(soup) # soup is now a string in html_content

                output_filename = os.path.join(output_dir, f"{item.get_id()}.html") # outputting files with id names

                with open(output_filename, 'w', encoding='utf-8') as html_file: # conversion stuff, puts the content into the files
                    html_file.write(content_html)
                    self.textBrowser.setText("Congrats, you converted it to HTML! Go ahead and open it by clicking 'Open Window' under 'Open HTML Window'.")
        print("DONE") # (testing on the same epub file writes over the same html files)
    


# this window is the HTMLviewer 
# different widgets = different window = different class
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("otherui.ui", self) 

        self.actionOpen_HTML.triggered.connect(self.openHTML)
        #self.actionDark_Mode_3.triggered.connect(self.darkMode)

        # this is all setting up the web viewer used to display the html 
        self.web_engine_view = QWebEngineView(self)
        self.setGeometry(100, 100, 500, 600) # it had a tendency of being really squashed, so default window size parameters :D
        self.central_layout = QVBoxLayout() # organize widget in gui
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.central_layout.addWidget(self.web_engine_view)

    def openHTML(self): # enter file explorer, click your HTML file, and it'll display the path + formatted contents
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'HTML files (*.html)') # same file dialog, specifies HTML!
        self.setWindowTitle(fname[0])
        self.web_engine_view.setUrl(QUrl.fromLocalFile(fname[0])) # web engine needs a URL, get one from selected local file

# stuff to make the .ui load and work
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()