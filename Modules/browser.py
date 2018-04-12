# importeren van de libraries en modules

import win32crypt
import os

from Utils.FileType import *
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tabulate import tabulate
from Utils.log import *
from Utils.Models import *




class Browser:
    def __init__(self, hoofdmenu):
        Debugger("Starting Module Browser...")
        Logger("Module Browser gestart")
        self.hoofdmenu_refrentie = hoofdmenu
        self.browse_arr = []
        self.browse_arr2 = []

    def generate_hashlist(self):
        Debugger("Generating Hashlist..", True)
        #  Gebruiker een partitie uit een image laten selecteren
        partitie = self.select_partition()
        #  Array van bestanden opslaan
        files = partitie.files
        #  Nieuwe array maken om metadata per file op te lsaan
        array_list = []
        #  Voor iedere file meta-data opslaan naar array_list
        for file in files:
            try:
                file.name.decode()
            except UnicodeDecodeError:
                continue

            # Vanwege Memory Error tijdens het testen is er een limiet gegeven aan de grootte die de bestanden mogen zijn om in de array gezet te worden
            if file.size < 99999999:
                array_list.append(file.get_attributes())

        #  Printen van mooie tabel
        print tabulate(array_list, headers=[
                       'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
        Logger("Heeft een lijst van hashes gegenereert op het scherm")

    # Hier kan de gebruiker kiezen welke Image en welke partitie op de gekozen Image hij wilt onderzoeken
    def select_partition(self):
        print 'Please select an image: '
        Debugger("Gebruiker kiest Image")
        #  Printing all images with their path
        for a in range(len(self.hoofdmenu_refrentie.images)):
            print '\t[' + str(a) + '] ' + self.hoofdmenu_refrentie.images[a].image_path
        image = int(raw_input('\nPlease Choose an option [0-9]: '))
        Debugger("Gebruiker kiest Image " + str(image) + ": " + str(self.hoofdmenu_refrentie.images[a].image_path))
        Logger("Gebruiker kiest Image " + str(image) + ": " + str(self.hoofdmenu_refrentie.images[a].image_path))
        print 'Please select an Partition: '
        #  Printing all Partitions from Selected Image
        for part in range(len(self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions())):
            partition_pointer = self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part]
            print '\t[' + str(part) + '] ' + partition_pointer.desc + " - " + str(partition_pointer.size / 1024) + "MB"

        part = int(raw_input('\nPlease Choose an option [0-9]: '))
        Debugger("Gebruiker kiest Partitie " + str(part) + ": " + str(self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part].desc))
        Logger("Gebruiker kiest Partitie " + str(part) + ": " + str(self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part].desc))
        return self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part]

    # deze verwijzing zorgt ervoor dat de geladen Images gevonden worden zodat ze in de functie hierboven gevonden kunnen worden
    def find_images(self):
        self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files_rapport()

    def cli(self):
        # D.M.V. deze List te gebruiken worden de Browsers maar 1x geprint
        uniq_browser = []
        # Hier wordt de teller voor de gebruiker gedeclared
        i = 1
        # Loop om terug te komen bij de opties
        while True:
            # Opties voor de gebruiker
            print "\t[1] Identify browsers (If not done yet, please use this before selecting [2])"
            print "\t[2] Atributes"
            print "\t[3] Generate HashList"
            print "\t[0] Back"

            inpoet = int(raw_input('Please choose an option: '))
            Debugger("Gekozen voor optie: " + str(inpoet))
            Logger("Gekozen voor optie: " + str(inpoet))
            if inpoet == 1:
                self.identify_browser_windows()
            if inpoet == 2:
                Debugger("Generating attributes of found Browsers...")

                # Browser lijst wordt gedeclared zodat het programma kan kijken welke browsers gevonden zijn op de image
                browser = self.browse_arr2

                # Als de browser lijst niet leeg is wordt de for loop geactiveerd
                if len(browser) > 0:
                    for bestand in browser:

                        # Zit de browser niet in de lijst "uniq_browser" dan wordt hij toegevoegd en de optie om de attributen hiervoor te kiezen gegeven
                        if "firefox.exe" not in uniq_browser:
                            print "\t[",i,"] Attributes Mozilla Firefox"
                            i = i + 1
                            uniq_browser.append("firefox.exe")
                            # print bestand
                        if "chrome.exe" not in uniq_browser:
                            print "\t[",i,"] Attributes Google Chrome"
                            i = i + 1
                            uniq_browser.append("chrome.exe")

                    # Zit hij er wel in dan wordt de waarde van de keuze [i] gereset en de lijst geleegd
                    # Zo kan het programma opnieuw gebruikt worden voor andere images zonder dat er dubbele opties geprint worden
                    # Dit betekent wel dat er elke keer browser geidentificeerd moeten worden per andere Image
                    if "firefox.exe" in uniq_browser:
                        i = 1
                        uniq_browser = []
                    if "chrome.exe" in uniq_browser:
                        i = 1
                        uniq_browser = []
                    input1 = int(raw_input('Please choose an option: '))
                    if input1 == 1:
                        print "\t[1] Cookies"
                        print "\t[2] Bookmarks"
                        print "\t[3] History"
                        print "\t[4] Downloads"
                        print "\t[0] Back"

                        input2 = int(raw_input('Please choose an option: '))
                        if input2 == 1:
                            self.cookies()
                        if input2 == 2:
                            self.bookmarks()
                        if input2 == 3:
                            self.history()
                        if input2 == 4:
                            self.downloads()
                        if input2 == 0:
                            break
                    if input1 == 2:
                        print "\t[1] Chrome Login"
                        print "\t[2] Chrome History"
                        print "\t[3] Chrome Cookies"
                        print "\t[4] Chrome Top Sites"
                        print "\t[0] Back"

                        input = int(raw_input('Please choose an option: '))

                        if input == 1:
                            self.chrome_login()
                        if input == 2:
                            self.chrome_history()
                        if input == 3:
                            self.cookies_chrome()
                        if input == 4:
                            self.chrome_topsites()
                        if input == 0:
                            break
            if inpoet == 3:
                self.generate_hashlist()
            # Break om uit de while loop te komen en terug te gaan naar het hoofdmenu
            if inpoet == 0:
                break

    # Hier worden de browser geidentificeerd
    def identify_browser_windows(self):
        #  D.M.V. deze List te gebruiken worden de Browsers maar 1x geprint
        uniq_browser = []
        browse_arr = self.browse_arr
        print (23 * "*")
        partition = self.select_partition()
        # Per bestand in partition.files wordt gekeken of de bestandsnaam nog niet in "uniq_browser" zit
        for bestand in partition.files:
            if bestand.name not in uniq_browser:

                # Zit er 1 van de browsers in dan wordt deze toegevoegd aan de browse_arr en aan uniq_browser
                if bestand.name == "firefox.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append(bestand.name)
                if bestand.name == "opera.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append("opera.exe")
                if bestand.name == "chrome.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append("chrome.exe")
                if bestand.name == "safari.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append("safari.exe")
                if bestand.name == "iexplore.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append("iexplore.exe")
                if bestand.name == "microsoftedge.exe":
                    browse_arr.append([bestand.name, bestand.sha256()])
                    uniq_browser.append("microsoftedge.exe")

        # Het printen van de resultaten
        print "De gevonden browsers zijn: "
        print tabulate(browse_arr, headers=['Naam', 'Sha256'])
        print ""
        # Zit er iets in uniq_browser dan wordt de browse_arr gereset en overgenomen door browse_arr2 zodat deze aan het begin van de module gebruikt kan worden
        if len(uniq_browser) > 0:
            self.browse_arr2 = self.browse_arr
            self.browse_arr = []
        Logger("Browsers gevonden: " + str(uniq_browser))
        Debugger("Identifying Browsers...")
        Debugger("Browsers gevonden: " + str(uniq_browser))

    def cookies(self):
        # In deze lijst worden de gevonden cookies opgeslagen
        cookies_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            #  Om te voorkomen dat het programma crasht worden alleen de bestandsnamen die in utf-8 te lezen zijn doorgevoerd
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'cookies.sqlite' in bestand.name:
                path = bestand.name
                #  Hier wordt de gevonden database gekoppeld aan een engine waardoor hij uit te lezen is
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(bind=engine)
                moz_cookies = Table('newtable', meta, autoload=True)
                # Een select Statement om de juiste tabel uit te lezen
                select_st = select([moz_cookies])
                cookies = conn.execute(select_st)
                #  printen van de resultaten
                print 'Gevonden cookie\'s in Mozilla Firefox zijn: '
                for cookie in cookies:
                    cookies_arr.append([cookie.id, cookie.name, cookie.host])
                print tabulate(cookies_arr, headers=["ID","Naam", "Host"])
                Debugger("Generating Found Cookies in Mozilla Firefox")
                Logger("Heeft Mozilla Firefox cookies gezocht")

    def cookies_chrome(self):
        # In deze lijst worden de gevonden cookies opgeslagen
        cookies_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            #  Om te voorkomen dat het programma crasht worden alleen de bestandsnamen die in utf-8 te lezen zijn doorgevoerd
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'cookies.sqlite' in bestand.name:
                #  Hier wordt de gevonden database gekoppeld aan een engine waardoor hij uit te lezen is
                path = bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_cookies = Table('cookies', meta, autoload=True)
                # Een select Statement om de juiste tabel uit te lezen
                select_st = select([moz_cookies])
                cookies = conn.execute(select_st)
                #  printen van de resultaten
                print 'Gevonden cookie\'s in Google Chrome zijn: '
                for cookie in cookies:
                    pwd = win32crypt.CryptUnprotectData(cookie.encrypted_value)
                    cookies_arr.append([cookie.host_key, cookie.name, str(pwd[1])])
                print tabulate(cookies_arr, headers=["Host", "Naam", "Value"])
                Logger("Heeft Chrome cookies gezocht")
                Debugger("Generating Found Cookies in Google Chrome")

    def bookmarks(self):
        # In deze lijst worden de gevonden bookmarks opgeslagen
        bookmarks_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            #  Om te voorkomen dat het programma crasht worden alleen de bestandsnamen die in utf-8 te lezen zijn doorgevoerd
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'places.sqlite' in bestand.name:
                bestand.export()
                #  Hier wordt de gevonden database gekoppeld aan een engine waardoor hij uit te lezen is
                path = bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_bookmarks = Table('moz_bookmarks', meta, autoload=True)
                # Een select Statement om de juiste tabel uit te lezen
                select_st = select([moz_bookmarks])
                bookmarks = conn.execute(select_st)
                #  printen van de resultaten
                print 'Gevonden Bookmarks\'s in Mozilla Firefox zijn: '
                for bookmark in bookmarks:
                    bookmarks_arr.append([bookmark.id, bookmark.title])
                print tabulate(bookmarks_arr, headers=["ID", "Naam"])
                Logger("Heeft Mozilla Firefox Bookmarks gezocht")
                Debugger("Generating found Bookmarks in Mozilla Firefox")

    def history(self):
        # In deze lijst worden de gevonden bezochte pagina's opgeslagen
        history_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            #  Om te voorkomen dat het programma crasht worden alleen de bestandsnamen die in utf-8 te lezen zijn doorgevoerd
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'places.sqlite' in bestand.name:
                bestand.export()
                #  Hier wordt de gevonden database gekoppeld aan een engine waardoor hij uit te lezen is
                path = bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_history = Table('moz_places', meta, autoload=True)
                # Een select Statement om de juiste tabel uit te lezen
                select_st = select([moz_history])
                history = conn.execute(select_st)
                #  printen van de resultaten
                print 'Gevonden bezochte pagina\'s in Mozilla Firefox zijn: '
                for pagina in history:
                    history_arr.append([pagina.id, pagina.title, pagina.url])
                print tabulate(history_arr, headers=["ID", "Naam", "URL"])
                Logger("Heeft Mozilla Firefox Geschiedenis gezocht")
                Debugger("Generating History found in Mozilla Firefox")

    def downloads(self):
        # In deze lijst worden de gevonden downloads opgeslagen
        downloads_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            #  Om te voorkomen dat het programma crasht worden alleen de bestandsnamen die in utf-8 te lezen zijn doorgevoerd
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'downloads.sqlite' in bestand.name:
                #  bestand.export_to()
                path = bestand.name #  bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_cookies = Table('moz_downloads', meta, autoload=True)
                # Een select Statement om de juiste tabel uit te lezen
                select_st = select([moz_cookies])
                downloads = conn.execute(select_st)
                #  printen van de resultaten
                print 'Gevonden download\'s in Mozilla Firefox zijn: '
                for download in downloads:
                    downloads_arr.append([download.name, download.source])
                print tabulate(downloads_arr, headers=["Naam", "Afkomst"])
                Logger("Heeft Mozilla Firefox Downloads gezocht")
                Debugger("Generating Mozilla Firefox Downloaded files")

    def chrome_login(self):
        # In deze lijst worden de gevonden Login Data opgeslagen
        chrome_arr = []
        paritie = self.select_partition()
        #  Elk bestand wordt doorzocht
        for bestand in paritie.files:
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                pass
            if 'Login Data.sqlite' in bestand.name: # cookies = Login Data
                #bestand.export()
                path = bestand.name  #  "Database\\" + bestand.name
                #  Hier wordt de gevonden database gekoppeld aan een engine waardoor hij uit te lezen is
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(bind=engine)
                moz_cookies = Table('logins', meta, Column("origin_url", Integer, primary_key=True), autoload=True, autoload_with=engine)
                select_st = select([moz_cookies])
                cookies = conn.execute(select_st)
                print 'Gevonden login\'s in Google Chrome zijn: '
                for cookie in cookies:
                    pwd = win32crypt.CryptUnprotectData(cookie.password_value)
                    chrome_arr.append([cookie.origin_url, cookie.username_value, cookie.times_used, str(pwd[1])])
                print tabulate(chrome_arr, headers=["URL","Username","Hoe vaak gebruikt","Wachtwoord"])
                Logger("Heeft Chrome login data gezocht")
                Debugger("Generating found Chrome Login Data + passwords")

    def chrome_history(self):
        Logger("Heeft Chrome History gezocht")
        chrome_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'History.sqlite' in bestand.name:
                bestand.export_to()
                path = bestand.name  #  bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_cookies = Table('urls', meta, Column("id", Integer, primary_key=True), autoload=True)
                select_st = select([moz_cookies])
                cookies = conn.execute(select_st)
                print 'Gevonden bezochte pagina\'s in Google Chrome zijn: '
                for cookie in cookies:
                    for bestand in chrome_arr:
                        if cookie.id not in chrome_arr:
                            chrome_arr.append([cookie.id, cookie.url, cookie.title, cookie.visit_count])
                print tabulate(chrome_arr, headers=["ID", "URL", "Naam", "Hoe vaak bezocht"])

    def chrome_topsites(self):
        Logger("Heeft Chrome's meest bezochte pagina's gezocht")
        chrome_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            try:
                bestand.name.decode()
            except UnicodeDecodeError:
                continue

            if 'Top Sites.sqlite' in bestand.name:
                bestand.export()
                path = bestand.name  #  bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                conn = engine.connect()
                meta = MetaData(engine)
                moz_history = Table('thumbnails', meta, autoload=True)
                select_st = select([moz_history])
                cookies = conn.execute(select_st)
                print 'Meest bezochte pagina\'s in Google Chrome zijn: '
                for cookie in cookies:
                    # koenkie = self.hoofdmenu_refrentie.is_ascii(cookie)
                    chrome_arr.append([cookie.url, cookie.title, cookie.boring_score])
                print tabulate(chrome_arr, headers=["URL", "TITLE", "Boring Score(in %)"])

    def run(self):
        print 'Hallo Wereld, dit is de Browsermodule!'
        self.cli()
        #  for partitie in self.main.images[0].ewf_img_info.partities:
        #     print partitie.desc

        #  for bestand in self.main.images[0].ewf_img_info.partities[0].files:
        #     print bestand.name

        '''if "firefox.exe" in bestand.name:
            print "firefox gevonden \t" + bestand.name + '\t' + bestand.sha256()
        if "opera.exe" in bestand.name:
            print "opera gevonden \t" + bestand.name + '\t' + bestand.sha256()'''

        '''def generate_hashlist(self):
        # TODO: Selecteren van image
        self.hoofdmenu_refrentie.images[0].ewf_img_info.partition_report()
        input = int(raw_input('Please choose an parition to generate hashlist for [0-9]: '))
        self.hoofdmenu_refrentie.images[0].ewf_img_info.get_partitions()[input].files_rapport()'''

        #  dbPath = self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files[486]
        #  engine = create_engine('sqlite:///%s' % dbPath, echo=True)

        '''#  Create a MetaData instance
        metadata = MetaData()
        print metadata.tables

        #  reflect db schema to MetaData
        metadata.reflect(bind=engine)
        print metadata.tables'''

        '''def tel_files(self):
            for file in range(len(self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files)):
                try:
                    print '\t[' + str(file) + '] ' + \
                          self.hoofdmenu_refrentie.images[0].ewf_img_info.get_partitions()[0].files[file].name
                except:
                    pass'''

        '''if "cookies.sqlite" in bestand.name:
        dbPath = bestand.name

        engine = create_engine('sqlite:///%s' % dbPath, echo=True)

        metadata = MetaData(engine)
        moz_bookmarks = Table('moz_bookmarks', metadata, autoload=True)
        mapper(self.Bookmarks, moz_bookmarks)

        Session = sessionmaker(bind=engine)
        session = Session()
        return session.query(self.Bookmarks).all()

         for x in bestand.get_strings():
            print str(x)'''
