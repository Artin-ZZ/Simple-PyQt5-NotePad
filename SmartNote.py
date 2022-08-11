#######################
# Import Dependencies #
#######################
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *








##############
# Main Class #
##############
class MainWindow(QMainWindow):
    # Constractor Method
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()

        self.setMinimumWidth(1080)
        self.setMinimumHeight(860)
        ## Setup The Qtext Edit
        ## If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open File...", self)
        open_file_action.setStatusTip("Open File")
        open_file_action.triggered.connect(self.file_save)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save Current Page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save Current Page To Specified File")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Tools")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Tools")

        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        help_toolbar = QToolBar("Help")
        help_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(help_toolbar)
        edit_menu = self.menuBar().addMenu("&Help")

        ab_dv_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Creator", self)
        ab_dv_action.setStatusTip("Creator's Information")
        ab_dv_action.triggered.connect(self._about_dev_info)
        edit_menu.addAction(ab_dv_action)

        edit_menu.addSeparator()
        




        self.update_title()
        self.show()


    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


    def file_open(self):
        path , _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Documents (*.txt);All Files (*.*)")
        
        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()
            
            except Exception as e:
                self.dialog_critical(str(e))
            
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()
    
    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()
        
        self._save_to_path(self.path)
    
    def file_saveas(self):
        path , _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Documents (*.txt);All Files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return
        
        self._save_to_path(path)
    
    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
            
        except Exception as e:
            self.dialog_critical(str(e))
        
        else:
            self.path = path
            self.update_title()
    
    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())
    
    def update_title(self):
        self.setWindowTitle("%s - Smart Note" % (os.path.basename(self.path) if self.path else "Untitled"))
    
    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def _about_dev_info(self):
        dlg = AboutDialog()
        dlg.exec_()

##########################
## About Dev Page Class ##
##########################
class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(600)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()


        title = QLabel("About Creator :")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        lbl_pic = QLabel()
        pixmap = QPixmap('images/About.png')
        pixmap = pixmap.scaledToWidth(500)
        lbl_pic.setPixmap(pixmap)
        lbl_pic.setFixedHeight(400)

        layout.addWidget(title)

        layout.addWidget(QLabel("Version 2.0.0"))
        layout.addWidget(lbl_pic)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

###########
# Run App #
###########
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Smart Note")
    window = MainWindow()
    app.exec_()