import os
import shlex

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class InputDialog:
    def __init__(self, parent):
        self.dialog = Gtk.Dialog(title="Dodawanie", transient_for=parent, modal=True)
        self.dialog.set_default_size(200, 100)

        content_area = self.dialog.get_content_area()
        label = Gtk.Label(label="Wprowadź ścieżkę lub nazwę pliku:")
        content_area.pack_start(label, False, False, 0)
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        content_area.add(self.entry)
        self.dialog.add_button("Cofnij", Gtk.ResponseType.CANCEL)
        self.dialog.add_button("Zatwierdź", Gtk.ResponseType.OK)

        self.dialog.connect("response", self.on_response)
    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            self.text = self.entry.get_text()
        else:
            self.text = None

        self.dialog.destroy()

class GridWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Eksplorator plików")
        self.set_default_size(400, 200)
        self.scroll = Gtk.ScrolledWindow()
        self.path = os.getcwd()
        lista = os.listdir(self.path)
        self.lista_plikow = Gtk.ListBox()
        self.lista_plikow.set_activate_on_single_click(False)
        self.pole_sciezki = Gtk.Entry()
        self.pole_sciezki.set_text(self.path)
        self.selected_item = ""
        self.folder = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.SMALL_TOOLBAR)
        self.plik = Gtk.Image.new_from_icon_name("document", Gtk.IconSize.SMALL_TOOLBAR)

        label = Gtk.Label(label="...")
        row = Gtk.ListBoxRow()
        row.add(label)
        self.lista_plikow.add(row)
        for element in lista:
            item = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            item.add(hbox)
            if os.path.isdir(element):
                icon = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.SMALL_TOOLBAR)
            elif os.path.isfile(element):
                icon = Gtk.Image.new_from_icon_name("document", Gtk.IconSize.SMALL_TOOLBAR)
            else:
                icon = Gtk.Image.new_from_icon_name("unknown", Gtk.IconSize.SMALL_TOOLBAR)
            hbox.pack_start(icon, False, False, 0)
            label = Gtk.Label(label=element)
            hbox.pack_start(label, True, True, 0)
            self.lista_plikow.add(item)
        self.scroll.add(self.lista_plikow)
        self.home_button = Gtk.Button(label="Katalog domowy")
        grid = Gtk.Grid()


        self.lista_plikow.set_hexpand(True)
        self.lista_plikow.set_vexpand(True)
        self.pole_sciezki.set_hexpand(True)
        self.add(grid)
        self.lista_plikow.connect("row-activated", self.itemActivated)
        self.lista_plikow.connect("row-selected", self.itemSelected)
        self.home_button.connect("clicked", self.home_button_clicked)
        self.pole_sciezki.connect("changed", self.pole_sciezki_changed)

        # Tworzenie paska menu
        self.menubar = Gtk.MenuBar()

        # Tworzenie menu "File"
        filemenu = Gtk.Menu()
        filemenu_item = Gtk.MenuItem(label="Pomoc")
        filemenu_item.set_submenu(filemenu)
        self.menubar.append(filemenu_item)
        # Tworzenie elementów w menu "File"
        o_programie = Gtk.MenuItem(label="O programie")
        o_programie.connect("activate", self.o_programie_clicked)
        filemenu.append(o_programie)
        grid.attach(self.menubar, 0,0,2,1)
        grid.attach(self.scroll,0,2,2,1)
        grid.attach(self.home_button,0,1,1,1)
        grid.attach(self.pole_sciezki, 1,1,1,1)

        self.popup_menu = Gtk.Menu()
        otworz_item = Gtk.MenuItem(label="otwórz")
        otworz_item.connect("activate", self.open_selected)
        self.popup_menu.append(otworz_item)
        nowy_item = Gtk.MenuItem(label="nowy")
        self.popup_menu.append(nowy_item)

        testmenu = Gtk.Menu()
        testmenu2 = Gtk.Menu()
        nowy_item2 = Gtk.MenuItem(label="nowy")
        nowy_item.set_submenu(testmenu)
        nowy_item2.set_submenu(testmenu2)
        plik_item = Gtk.MenuItem(label="plik")
        folder_item = Gtk.MenuItem(label="folder")
        plik_item.connect("activate", self.create_new_file)
        folder_item.connect("activate", self.create_new_folder)
        testmenu.append(plik_item)
        testmenu.append(folder_item)

        plik_item2 = Gtk.MenuItem(label="plik")
        folder_item2 = Gtk.MenuItem(label="folder")
        plik_item2.connect("activate", self.create_new_file)
        folder_item2.connect("activate", self.create_new_folder)
        testmenu2.append(plik_item2)
        testmenu2.append(folder_item2)

        zmien_nazwe_item = Gtk.MenuItem(label="zmień nazwę")
        self.popup_menu.append(zmien_nazwe_item)
        zmien_nazwe_item.connect("activate", self.rename_selected)
        usun_item = Gtk.MenuItem(label="usuń")
        self.popup_menu.append(usun_item)
        usun_item.connect("activate", self.delete_selected)
        kopiuj_item = Gtk.MenuItem(label="kopiuj")
        self.popup_menu.append(kopiuj_item)
        kopiuj_item.connect("activate", self.copy_selected)
        wytnij_item = Gtk.MenuItem(label="wytnij")
        self.popup_menu.append(wytnij_item)
        wytnij_item.connect("activate", self.move_selected)
        self.lista_plikow.connect("button-press-event", self.on_button_press)

        self.popup_menu_not_selected = Gtk.Menu()
        self.popup_menu_not_selected.append(nowy_item2)
    def on_button_press(self, x, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            a = self.lista_plikow.get_row_at_y(y)
            self.lista_plikow.select_row(a)
            if(self.selected_item != ""):
                self.popup_menu.show_all()
                self.popup_menu.popup_at_pointer(None)
            else:
                self.popup_menu_not_selected.show_all()
                self.popup_menu_not_selected.popup_at_pointer(None)

    def o_programie_clicked(self, x):
        okno = Gtk.Window(title="O programie")
        okno.show()
        opis_label = Gtk.Label(label="Eksplorator plików")
        wersja_label = Gtk.Label(label="wersja 1.0")
        vbox = Gtk.VBox(spacing=10)
        vbox.pack_start(opis_label, True, True, 0)
        vbox.pack_start(wersja_label, True, True, 0)
        okno.add(vbox)
        okno.show_all()
    def home_button_clicked(self, x):
        self.set_path(os.path.expanduser("~"))
    def itemSelected(self,list_box,row):
        if row is not None and row.get_index() > 0:
            label_text = ""
            child = row.get_child()
            children = child.get_children()
            for child in children:
                if isinstance(child, Gtk.Label):
                    label_text = child.get_text()
                    break
            self.selected_item = label_text
        else:
            self.selected_item = ""
    def itemActivated(self, list_box, row):
        if list_box is not None:
            self.open_selected(0)

    def open_selected(self, x):
        if self.lista_plikow.get_selected_row().get_index() >= 0:
            fullname = self.path + "/" + self.selected_item
            openable_fullname = shlex.quote(fullname)
            if self.lista_plikow.get_selected_row().get_index() == 0:
                self.set_path(os.path.dirname(self.path))
            elif os.path.isdir(fullname):
                self.set_path(fullname)
            elif os.path.isfile(fullname):
                os.system("open "+openable_fullname)

    def delete_selected(self, x):
        fullname = self.path + "/" + self.selected_item
        if(self.selected_item!=""):
            deletable_fullname = shlex.quote(fullname)
            os.system("rm -r "+deletable_fullname)
            self.selected_item = ""
            self.refresh_list()

    def create_new_file(self, e):
        fullname = self.path
        dialog = InputDialog(self)
        dialog.dialog.show_all()
        dialog.dialog.run()
        if dialog.text is not None:
            nazwa = dialog.text
            if "/" in nazwa or nazwa == "":
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Pliki i foldery muszę mieć niepustą nazwę bez ukośników!"
                )
                dialog.run()
                dialog.destroy()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Plik lub folder o podanej nazwie już istnieje!"
                )
                dialog.run()
                dialog.destroy()
            else:
                fullname = fullname + "/" + nazwa
                addible_fullname = shlex.quote(fullname)
                os.system("touch "+addible_fullname)
        self.refresh_list()
    def create_new_folder(self, e):
        fullname = self.path
        dialog = InputDialog(self)
        dialog.dialog.show_all()
        dialog.dialog.run()
        if dialog.text is not None:
            nazwa = dialog.text
            if "/" in nazwa or nazwa == "":
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Pliki i foldery muszę mieć niepustą nazwę bez ukośników!"
                )
                dialog.run()
                dialog.destroy()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Plik lub folder o podanej nazwie już istnieje!"
                )
                dialog.run()
                dialog.destroy()
            else:
                fullname = fullname + "/" + nazwa
                addible_fullname = shlex.quote(fullname)
                os.system("mkdir "+addible_fullname)
        self.refresh_list()

    def rename_selected(self, e):
        fullname = self.path + "/" + self.selected_item
        dialog = InputDialog(self)
        dialog.dialog.show_all()
        dialog.dialog.run()
        if dialog.text is not None:
            nazwa = dialog.text
            if "/" in nazwa or nazwa == "":
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Pliki i foldery muszę mieć niepustą nazwę bez ukośników!"
                )
                dialog.run()
                dialog.destroy()
            elif os.path.isdir(self.path +"/"+ nazwa) or os.path.isfile(self.path +"/"+ nazwa):
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Plik lub folder o podanej nazwie już istnieje!"
                )
                dialog.run()
                dialog.destroy()
            else:
                sciezka = self.path +"/" + nazwa
                os.rename(fullname, sciezka)

        self.refresh_list()

    def copy_selected(self, e):
        fullname = self.path + "/" + self.selected_item
        openable_fullname = shlex.quote(fullname)
        dialog = InputDialog(self)
        dialog.dialog.show_all()
        dialog.dialog.run()

        if dialog.text is not None:
            sciezka = dialog.text
            if os.path.isdir(sciezka) and fullname!=sciezka+"/"+self.selected_item:
                sciezka = sciezka + "/"+self.selected_item
                openable_sciezka = shlex.quote(sciezka)
                os.system("cp -r " + openable_fullname + " " + openable_sciezka)
            elif not os.path.isdir(sciezka):
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Wprowadzono nieprawidłową ścieżkę!"
                )
                dialog.run()
                dialog.destroy()
            else:
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Ścieżka źródłowa i docelowa jest taka sama!"
                )
                dialog.run()
                dialog.destroy()
        self.refresh_list()

    def move_selected(self, e):
        fullname = self.path + "/" + self.selected_item
        openable_fullname = shlex.quote(fullname)
        dialog = InputDialog(self)
        dialog.dialog.show_all()
        dialog.dialog.run()

        if dialog.text is not None:
            sciezka = dialog.text
            if os.path.isdir(sciezka) and fullname != sciezka + "/" + self.selected_item:
                sciezka = sciezka + "/" + self.selected_item
                openable_sciezka = shlex.quote(sciezka)
                os.system("mv " + openable_fullname + " " + openable_sciezka)
            elif not os.path.isdir(sciezka):
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Wprowadzono nieprawidłową ścieżkę!"
                )
                dialog.run()
                dialog.destroy()
            else:
                dialog = Gtk.MessageDialog(
                    parent=None,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    title="Błąd!",
                    text="Ścieżka źródłowa i docelowa jest taka sama!"
                )
                dialog.run()
                dialog.destroy()
        self.refresh_list()

    def set_path(self, path):
        self.path = path
        self.pole_sciezki.set_text(self.path)
        self.refresh_list()

    def refresh_list(self):
        self.lista_plikow.foreach(lambda row: self.lista_plikow.remove(row))
        lista = os.listdir(self.path)
        label = Gtk.Label(label="...")
        row = Gtk.ListBoxRow()
        row.add(label)
        self.lista_plikow.add(row)
        for element in lista:
            item = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            item.add(hbox)
            if os.path.isdir(self.path + "/" + element):
                icon = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.SMALL_TOOLBAR)
            elif os.path.isfile(self.path + "/" + element):
                icon = Gtk.Image.new_from_icon_name("document", Gtk.IconSize.SMALL_TOOLBAR)
            else:
                icon = Gtk.Image.new_from_icon_name("unknown", Gtk.IconSize.SMALL_TOOLBAR)
            hbox.pack_start(icon, False, False, 0)
            label = Gtk.Label(label=element)
            hbox.pack_start(label, True, True, 0)
            self.lista_plikow.add(item)
        self.lista_plikow.show_all()

    def pole_sciezki_changed(self,input):
        s = input.get_text()
        if os.path.isdir(s):
            self.set_path(s)
        elif os.path.isfile(s):
            self.set_path(os.path.dirname(s))
            os.system("open " + s)

win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
