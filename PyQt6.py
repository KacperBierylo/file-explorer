import os
import sys
from pathlib import Path
import shlex
from PyQt6.QtGui import QPixmap, QPalette, QColor, QIcon, QAction
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QWidget, QPushButton, QListWidgetItem, QVBoxLayout,
    QMenu, QInputDialog, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QSize


class ErrDialog(QDialog):
    def __init__(self, txt):
        super().__init__()
        self.setWindowTitle("Błąd!")
        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel(txt)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    def accept(self):
        self.close()
class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("O programie")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: gray; color: white;")
        self.layout = QVBoxLayout()
        self.label_title = QLabel("Eksplorator plików", self)
        self.label_version = QLabel("Wersja 1.0", self)
        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.label_version)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.path = os.getcwd()
        self.folder_icon = QIcon('folder.png')
        self.file_icon = QIcon('file.png')
        self.setWindowTitle("Eksplorator plików")
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(app.primaryScreen().size().width(), app.primaryScreen().size().height()))
        self.l1 = QLabel("Lista ulubionych")
        self.lista_ulubionych = QListWidget()
        self.lista_ulubionych.addItem("Dodaj")
        self.selected_item = ""
        self.lista_plikow = QListWidget()
        self.lista_plikow.addItem("...")
        lista = os.listdir(self.path)
        for element in lista:
            if os.path.isdir(element):
                el = QListWidgetItem(self.folder_icon, element)
                self.lista_plikow.addItem(el)
            elif os.path.isfile(element):
                self.lista_plikow.addItem(QListWidgetItem(self.file_icon, element))

        self.lista_plikow.currentItemChanged.connect(self.selected_changed)
        self.lista_plikow.itemActivated.connect(self.itemActivated)
        self.lista_plikow.clearFocus()
        self.pole_sciezki = QLineEdit(self.path)
        self.pole_sciezki.textChanged.connect(self.pole_sciezki_changed)
        self.home_button = QPushButton('Katalog domowy')
        self.home_button.clicked.connect(self.home_button_clicked)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(0, 1)
        layout.addWidget(self.pole_sciezki, 0, 1,1,2)
        layout.addWidget(self.home_button, 0, 0,1,1)
        layout.addWidget(self.lista_plikow, 1, 0,2,2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        menu = self.menuBar()
        file_menu = menu.addMenu("&Pomoc")
        button_action = QAction(QIcon("bug.png"), "&O programie", self)
        button_action.setStatusTip("This is your button")
        file_menu.addAction(button_action)
        button_action.triggered.connect(self.onMyToolBarButtonClick)

    def selected_changed(self, i):
        if self.lista_plikow.indexFromItem(i).row() != 0 and i is not None:
            self.selected_item = i.text()
        else:
            self.selected_item = ""

    def itemActivated(self, s):
        self.open_selected()

    def home_button_clicked(self):
        self.set_path(os.path.expanduser("~"))

    def set_path(self, path):
        if self.path != path:
            self.path = path
            self.lista_plikow.clear()
            self.lista_plikow.addItem("...")
            lista = os.listdir(self.path)
            self.pole_sciezki.setText(path)
            for element in lista:
                if os.path.isdir(path + "/" + element):
                    self.lista_plikow.addItem(QListWidgetItem(self.folder_icon, element))
                elif os.path.isfile(path + "/" + element):
                    self.lista_plikow.addItem(QListWidgetItem(self.file_icon, element))

    def pole_sciezki_changed(self,s):
        if os.path.isdir(s):
            self.set_path(s)
        elif os.path.isfile(s):
            self.set_path(os.path.dirname(s))
            os.system("open " + s)

    def onMyToolBarButtonClick(self, s):
        self.w = InfoWindow()
        self.w.show()

    def contextMenuEvent(self, e):
        if(self.selected_item!=""):
            context = QMenu(self.lista_plikow)
            context.addAction("Otwórz", self.open_selected)
            context_new = context.addMenu("Nowy")
            context_new.addAction("Nowy plik", self.create_new_file)
            context_new.addAction("Nowy folder", self.create_new_folder)
            context.addAction("Zmień nazwę", self.rename_selected)
            context.addAction("Usuń", self.delete_selected)
            context.addAction("Kopiuj", self.copy_selected)
            context.addAction("Wytnij", self.move_selected)
            context.exec(e.globalPos())
        else:
            context = QMenu(self.lista_plikow)
            context_new = context.addMenu("Nowy")
            context_new.addAction("Nowy plik", self.create_new_file)
            context_new.addAction("Nowy folder", self.create_new_folder)
            context.exec(e.globalPos())

    def refresh_list(self):
        self.lista_plikow.clear()
        self.lista_plikow.addItem("...")
        lista = os.listdir(self.path)
        for element in lista:
            if os.path.isdir(self.path + "/" + element):
                self.lista_plikow.addItem(QListWidgetItem(self.folder_icon, element))
            elif os.path.isfile(self.path + "/" + element):
                self.lista_plikow.addItem(QListWidgetItem(self.file_icon, element))

    def open_selected(self):
        if self.lista_plikow.currentIndex().row() >= 0:
            fullname = self.path + "/" + self.selected_item
            openable_fullname = shlex.quote(fullname)
            if self.lista_plikow.currentIndex().row() == 0:
                self.set_path(os.path.dirname(self.path))
            elif os.path.isdir(fullname):
                self.set_path(fullname)
            elif os.path.isfile(fullname):
                os.system("open "+openable_fullname)
            else:
                dlg = ErrDialog("Podany plik lub folder nie istnieje!")
                dlg.exec()

    def delete_selected(self):
        fullname = self.path + "/" + self.selected_item
        if (self.selected_item != ""):
            deletable_fullname = shlex.quote(fullname)
            os.system("rm -r "+deletable_fullname)
            self.refresh_list()

    def copy_selected(self):
        fullname = self.path + "/" + self.selected_item
        openable_fullname = shlex.quote(fullname)
        dialog = QInputDialog(self)
        dialog.setCancelButtonText("Cofnij")
        dialog.setOkButtonText("Zatwierdź")
        dialog.setWindowTitle("Kopiowanie")
        dialog.setLabelText("Wprowadź ścieżkę lub nazwę pliku:")
        if dialog.exec() == 1:
            sciezka = dialog.textValue()
            if os.path.isdir(sciezka) and fullname!=sciezka+"/"+self.selected_item:
                sciezka = sciezka + "/"+self.selected_item
                openable_sciezka = shlex.quote(sciezka)
                os.system("cp -r " + openable_fullname + " " + openable_sciezka)
            elif not os.path.isdir(sciezka):
                dlg = ErrDialog("Wprowadzono nieprawidłową ścieżkę!")
                dlg.exec()
            else:
                dlg = ErrDialog("Ścieżka źródłowa i docelowa jest taka sama!")
                dlg.exec()
        self.refresh_list()

    def move_selected(self):
        fullname = self.path + "/" + self.selected_item
        openable_fullname = shlex.quote(fullname)
        dialog = QInputDialog()
        dialog.setCancelButtonText("Cofnij")
        dialog.setOkButtonText("Zatwierdź")
        dialog.setWindowTitle("Kopiowanie")
        dialog.setLabelText("Wprowadź ścieżkę lub nazwę pliku:")
        if dialog.exec() == 1:
            sciezka = dialog.textValue()
            if os.path.isdir(sciezka) and fullname!=sciezka+"/"+self.selected_item:
                sciezka = sciezka + "/"+self.selected_item
                openable_sciezka = shlex.quote(sciezka)
                os.system("mv " + openable_fullname + " " + openable_sciezka)
            elif not os.path.isdir(sciezka):
                dlg = ErrDialog("Wprowadzono nieprawidłową ścieżkę!")
                dlg.exec()
            else:
                dlg = ErrDialog("Ścieżka źródłowa i docelowa jest taka sama!")
                dlg.exec()
        self.refresh_list()
    def rename_selected(self):
        fullname = self.path + "/" + self.selected_item
        dialog = QInputDialog()
        dialog.setCancelButtonText("Cofnij")
        dialog.setOkButtonText("Zatwierdź")
        dialog.setWindowTitle("Kopiowanie")
        dialog.setLabelText("Wprowadź ścieżkę lub nazwę pliku:")
        if dialog.exec() == 1:
            nazwa = dialog.textValue()

            if "/" in nazwa or nazwa == "":
                dlg = ErrDialog("Pliki i foldery muszę mieć niepustą nazwę bez ukośników!")
                dlg.exec()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dlg = ErrDialog("Plik lub folder o podanej nazwie już istnieje!")
                dlg.exec()
            else:
                sciezka = self.path +"/"+ nazwa
                os.rename(fullname, sciezka)
        self.refresh_list()

    def create_new_folder(self):
        fullname = self.path
        dialog = QInputDialog()
        dialog.setCancelButtonText("Cofnij")
        dialog.setOkButtonText("Zatwierdź")
        dialog.setWindowTitle("Dodawanie folderu")
        dialog.setLabelText("Wprowadź ścieżkę lub nazwę pliku:")
        if dialog.exec() == 1:
            nazwa = dialog.textValue()
            if "/" in nazwa or nazwa == "":
                dlg = ErrDialog("Pliki i foldery muszę mieć niepustą nazwę bez ukośników!")
                dlg.exec()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dlg = ErrDialog("Plik lub folder o podanej nazwie już istnieje")
                dlg.exec()
            else:
                fullname = fullname + "/" + nazwa
                openable_fullname = shlex.quote(fullname)
                os.system("mkdir "+openable_fullname)
        self.refresh_list()
    def create_new_file(self):
        fullname = self.path
        dialog = QInputDialog()
        dialog.setCancelButtonText("Cofnij")
        dialog.setOkButtonText("Zatwierdź")
        dialog.setWindowTitle("Dodawanie pliku")
        dialog.setLabelText("Wprowadź nazwę")
        if dialog.exec() == 1:
            nazwa = dialog.textValue()
            if "/" in nazwa or nazwa == "":
                dlg = ErrDialog("Pliki i foldery muszę mieć niepustą nazwę bez ukośników!")
                dlg.exec()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dlg = ErrDialog("Plik lub folder o podanej nazwie już istnieje")
                dlg.exec()
            else:
                fullname = fullname + "/" + nazwa
                openable_fullname = shlex.quote(fullname)
                os.system("touch "+openable_fullname)
        self.refresh_list()
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()