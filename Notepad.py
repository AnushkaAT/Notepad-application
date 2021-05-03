import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, \
    QStatusBar, QToolBar, QVBoxLayout, QFileDialog, QMessageBox, QAction, QFontDialog, \
        QColorDialog, QTextEdit
from PyQt5.QtCore import Qt, QSize, QTime, QDate, QFileInfo
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence, QColor, QSyntaxHighlighter, QTextCharFormat, QPalette
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

#we have imported the above classes from PyQt5 module, we will use their objects or inherit from them wherever needed

class AppNotepad(QMainWindow):
    #this child class will inherit the features of its parent: QMainWindow class
    #use of feature: Inheritance
    def __init__(self):
        #constructor
        super().__init__() 
        self.setWindowTitle("Notepad")
        self.setWindowIcon(QIcon("./icons/notepad.ico"))
        self.swidth, self.sheight = self.geometry().width(), self.geometry().height()
        self.resize(self.swidth, self.sheight)
        
        self.types = "Text Document(*.txt) ;; Python file(*.py) ;; All documents(*.*)"
        self.path= None
        
        fixfont= QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixfont.setPointSize(12)
        mainLayout= QVBoxLayout()
        
        #managing the text area
        self.editor= QTextEdit()
        self.editor.setFont(fixfont)
        self.editor.setAutoFillBackground(False)
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        
        mainLayout.addWidget(self.editor)
        
        #create a widget, a container
        global cntnr
        cntnr= QWidget()
        cntnr.setLayout(mainLayout)
        self.setCentralWidget(cntnr)
        
        #create status bar for application
        self.status= self.statusBar()
        
        #file menus of text editor
        filemenu= self.menuBar().addMenu("&File")
        fileTool= QToolBar('File')
        fileTool.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.BottomToolBarArea, fileTool)
        
        #in file menu- new file, open an existing, save and save as
        
        newAction= self.createAction(self, "./icons/new.ico", "New File", "New File", self.NewFile)
        newAction.setShortcut(QKeySequence.New)
        openAction= self.createAction(self, "./icons/open.ico", "Open File", "Open File", self.OpenFile)
        openAction.setShortcut(QKeySequence.Open) #enables user to use ctrl+o shortcut
        saveAction= self.createAction(self, "./icons/save.ico", "Save File", "Save File", self.SaveFile)
        saveAction.setShortcut(QKeySequence.Save) #enables user to use ctrl+s shortcut
        saveasAction= self.createAction(self, "./icons/saveas.ico", "Save File As", "Save File As", self.SaveAs)
        saveasAction.setShortcut(QKeySequence("Ctrl+Shift+S")) #enables user to use ctrl+Shift+s shortcut
        
        #print contents of file(printer)
        printAction= self.createAction(self, "./icons/print.ico", "Print File", "prints file", self.PrintFile)
        printAction.setShortcut(QKeySequence.Print)
        exita = self.createAction(self, "", "Exit", "Exit", self.exit)
        exppdf = self.createAction(self, "", "Export PDF", "EXport PDF", self.exportpdf)

        filemenu.addActions([newAction, openAction, saveAction, saveasAction, printAction, exita, exppdf])
        fileTool.addActions([newAction, openAction, saveAction, saveasAction, printAction])
        
        #edit menu: cut, copy, paste, undo, redo
        editmenu= self.menuBar().addMenu("&Edit")
        editTool= QToolBar('Edit')
        editTool.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.BottomToolBarArea, editTool)
        
        #undo
        undoAction= self.createAction(self, "./icons/undo.ico", "Undo", "Undo", self.editor.undo)
        undoAction.setShortcut(QKeySequence.Undo) #ctrl+z shortcut
        
        #redo
        redoAction= self.createAction(self, "./icons/redo.ico", "Redo", "Redo", self.editor.redo)
        redoAction.setShortcut(QKeySequence.Redo) #ctrl+shift+z shortcut
        
        #clear
        clearAction = self.createAction(self, "./icons/clear.ico", 'Clear', 'Clear', self.clear_content)
        
        #add these actions to menu and toolbar
        editmenu.addActions([undoAction, redoAction, clearAction])
        editTool.addActions([undoAction, redoAction, clearAction])
        #add a separator, to separate cut, copy, paste from above options
        editmenu.addSeparator()
        editTool.addSeparator()
        
        #cut, copy, paste and select all
        cutAction = self.createAction(self, './icons/cut.ico', 'Cut', 'Cut', self.editor.cut)
        cutAction.setShortcut(QKeySequence.Cut) #ctrl+x shortcut
        copyAction = self.createAction(self, './icons/copy.ico', 'Copy', 'Copy', self.editor.copy)
        copyAction.setShortcut(QKeySequence.Copy)#ctrl+c shortcut
        pasteAction = self.createAction(self, './icons/paste.ico', 'Paste', 'Paste', self.editor.paste)
        pasteAction.setShortcut(QKeySequence.Paste) #ctrl+v shortcut
        selectallAtion = self.createAction(self, './icons/selectall.ico', 'Select All', 'Select all', self.editor.selectAll)
        selectallAtion.setShortcut(QKeySequence.SelectAll) #ctrl+a shortcut
        
        #add these actions to toolbar and menu, after the separator
        editmenu.addActions([cutAction, copyAction, pasteAction, selectallAtion])
        editTool.addActions([cutAction, copyAction, pasteAction, selectallAtion])
        #add a separator
        editmenu.addSeparator()
        editTool.addSeparator()
        
        #wrap text feature
        wrapAction= self.createAction(self, "./icons/wrap.ico", "Wrap text", "Wrap text", self.toggle_wrap_text)
        wrapAction.setShortcut('Ctrl+Shift+W')
        editmenu.addAction(wrapAction)
        editTool.addAction(wrapAction)
        
        formatmenu= self.menuBar().addMenu("&Format")
        formatTool= QToolBar('Format')
        formatTool.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.BottomToolBarArea, formatTool)
        
        fontchoice= self.createAction(self, "./icons/font.ico", "Font", "Font", self.fontChoose)
        #fontchoice.triggered.connect(self.fontChoose)
        colorAction= self.createAction(self, "./icons/color.ico", "Font color", "Font color", self.ColorChoice)
        bgAction= self.createAction(self, "./icons/bg.ico", "Background color", "Background color", self.BGChoice)
        hlAction= self.createAction(self, "./icons/highlight.ico", "Highlight text", "Highlight text", self.Highlight)
        lalign = self.createAction(self, "./icons/left.ico","Align Left", "Align Left", self.leftalign)
        ralign = self.createAction(self, "./icons/right.ico","Align Right", "Align Right", self.rightalign)
        centalign = self.createAction(self, "./icons/centre.ico", "Align Centre", "Align Centre", self.centrealign)
        justifyl = self.createAction(self, "./icons/justify.ico", "Justify", "Justify", self.justify)
        #colorAction.triggered.connect(self.ColorChoice)
        formatmenu.addActions([fontchoice, colorAction, bgAction, hlAction, lalign, ralign, centalign, justifyl])
        formatTool.addActions([fontchoice, colorAction, bgAction, hlAction, lalign, ralign, centalign, justifyl])

        #displaying time and date
        editmenu= self.menuBar().addMenu("&Time And Date")
        dtime = self.createAction(self, "", "Time", "Time", self.disptime)
        ddate = self.createAction(self, "", "Date", "Date", self.dispdate)
        editmenu.addActions([dtime, ddate])
        self.titleUpdate()
    
    #methods of the class AppNotepad, Encapsulation intended
    def createAction(self, parent, icon, name, statustip, trigmethod):
        action= QAction(QIcon(icon), name, parent)
        action.setStatusTip(statustip) #this will be displayed when mouse is placed on icon
        action.triggered.connect(trigmethod)
        return action
    
    def titleUpdate(self):
        self.setWindowTitle('{0} - Notepad'.format(os.path.basename(self.path) if self.path else 'Untitled'))
        
    def dialog(self, msg):
        dig= QMessageBox(self)
        dig.setText(msg)
        dig.setIcon(QMessageBox.Critical)
        dig.show()
    
    def NewFile(self):
        self.win= AppNotepad()
        self.win.show()
        
    def OpenFile(self):
        path, _ = QFileDialog.getOpenFileName(parent= self, caption= "Open File", directory= "", filter=self.types)
        
        #use of exception handling
        if path:
            try: 
                with open(path, "r") as f:
                    text= f.read() #take the contents of the file
                    f.close()
            except Exception as e:
                self.dialog(str(e))
            else:
                self.path= path
                self.editor.setAcceptRichText(True)
                self.editor.setText(text)
                self.titleUpdate()
                
    def SaveFile(self):
        if self.path is None:
            self.SaveAs()
        else:
            try: 
                #text = self.editor.toHtml() if os.path.splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()
                text = self.editor.toPlainText()
                with open(self.path, "w") as f:
                    f.write(text) #write contents of text area into file
                    f.close()
            except Exception as e:
                self.dialog(str(e))
        
    def SaveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file as", "", self.types)
        text= self.editor.toPlainText()
        if not path:
            return
        else:
            try: 
                with open(path, "w") as f:
                    f.write(text) #write contents of text area into file
                    f.close()
            except Exception as e:
                self.dialog(str(e))
            else:
                self.path = path
                self.titleUpdate()
     
    #print contents of file through printer if available
    def PrintFile(self):
        printDialog = QPrintDialog()
        if printDialog.exec_():
            self.editor.print_(printDialog.printer())
    
    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def clear_content(self):
        self.editor.setPlainText('')
        
    def fontChoose(self):
        font, valid= QFontDialog.getFont()
        if valid:
            self.editor.setFont(font)
            
    def ColorChoice(self):
        color= QColorDialog.getColor()
        self.editor.setTextColor(color)
    
    def Highlight(self):
        color= QColorDialog.getColor()
        self.editor.setTextBackgroundColor(color)
        
    def BGChoice(self):
        color= QColorDialog.getColor()
        if(color.isValid()):
            self.editor.setAutoFillBackground(True)
            p= self.palette()
            p.setColor(QPalette.Base, color)
            self.setPalette(p)
        

    #align text to left
    def leftalign(self):
        self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft)

    #align text to centre
    def centrealign(self):
        self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #algn text to right
    def rightalign(self):
        self.editor.setAlignment(Qt.AlignmentFlag.AlignRight)

    #justify text
    def justify(self):
        self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify)

    #display current time
    def disptime(self):
        time = QTime.currentTime()
        self.editor.append(time.toString(Qt.DateFormat.DefaultLocaleLongDate))

    #display current date
    def dispdate(self):
        date = QDate.currentDate()
        self.editor.append(date.toString(Qt.DateFormat.DefaultLocaleLongDate))
        #self.editor.setText(date.toString(Qt.DateFormat.DefaultLocaleLongDate))

    #Exporting file as PDF
    def exportpdf(self):
        fn,_ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF Files (.pdf) ;; ALl Files")
        if fn != "":
            if QFileInfo(fn).suffix() == "":fn +='.pdf'
            pr = QPrinter(QPrinter.HighResolution)
            pr.setOutputFormat(QPrinter.PdfFormat)
            pr.setOutputFileName(fn)
            self.editor.document().print_(pr)

    #exit Notepad
    def exit(self):
        self.close()

#create object of our class
app= QApplication(sys.argv)
notePad= AppNotepad()
notePad.show()

sys.exit(app.exec_())