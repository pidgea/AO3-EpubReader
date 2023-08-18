from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QMessageBox
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
        self.window_2 = SecondWindow()

    def openHTMLWindow(self):
        self.window_2.show() 
        # this is basically a portal to access the next window
        
    def convertFile(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'EPUB files (*.epub)') # opens file dialog, epub specified

        try:
            self.setWindowTitle(fname[0]) # sets window name to selected file's path
            output_dir = 'output_html/' 
            os.makedirs(output_dir, exist_ok=True) # allows creation of folder of line above 

            book = epub.read_epub(fname[0]) # selected file data GET! shove into book variable

            for item in book.get_items(): # loop because there's multiple items to collect from the epub
                if item.get_type() == ebooklib.ITEM_DOCUMENT: # check type
                    content = item.get_body_content() # extract content of the item into the content variable
                    
                    soup = BeautifulSoup(content, 'html.parser') # soup variable contains... the Soup (content is parsed with integrated html parser)

                    content_html = str(soup) # soup is now a string in html_content

                    output_filename = os.path.join(output_dir, f"{item.get_id()}.html") # outputting files with unique id names

                    with open(output_filename, 'w', encoding='utf-8') as html_file: # opens the files in write mode with utf-8 encoding
                        html_file.write(content_html) # content is written into the files
                        self.textBrowser.setText("Congrats, you converted it to HTML! Go ahead and open it by clicking 'Open Window' under 'Open HTML Window'.")
            print("DONE") # (testing on the same epub file writes over the same html files)
        except:
            QMessageBox.critical(self, 'Error!', 'Try selecting a file!') # error pop up
            self.setWindowTitle("WOMSE-R") # the window title changes back to 'python', so change the title again
            return
    


# this window is the HTMLviewer 
# different widgets = different window = different class
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("otherui.ui", self) 

        self.setWindowTitle("HTMLViewer")

        self.actionOpen_HTML.triggered.connect(self.openHTML)
        self.actionDark_Mode_3.triggered.connect(self.setDarkMode)
        self.actionLight_Mode_2.triggered.connect(self.setLightMode)
        

        # this is all setting up the web viewer used to display the html 
        self.web_engine_view = QWebEngineView(self)
        self.resize(500, 600) # it had a tendency of being really squashed, so default window size parameters :D
        self.central_layout = QVBoxLayout() # organize widget in gui
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.central_layout.addWidget(self.web_engine_view)

    def openHTML(self): # enter file explorer, click your HTML file, and it'll display the path + formatted contents
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'HTML files (*.html)') # same file dialog, specifies HTML!
        self.setWindowTitle(fname[0])
        self.web_engine_view.setUrl(QUrl.fromLocalFile(fname[0])) # web engine needs a URL, get one from selected local file

    def setDarkMode(self):
        self.setStyleSheet('''QWidget{
            background-color: rgb(33,33,33);
            color: rgb(255, 255, 255);
            }
            QMenuBar::item:selected{
            color: rgb(0, 0, 0)
            }
            ''')
        

    def setLightMode(self):
        self.setStyleSheet("")

# stuff to make the .ui load and work
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()