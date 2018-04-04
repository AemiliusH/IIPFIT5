import pyewf
import pytsk3
import sqlite3
import os

import win32crypt

from Utils.FileType import *
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
from sqlalchemy import Column, Integer
from tabulate import tabulate


class Browser():
    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu

    def select_partition(self):
        print 'Please select an image: '
        # Printing all images with their path
        for a in range(len(self.hoofdmenu_refrentie.images)):
            print '\t[' + str(a) + '] ' + self.hoofdmenu_refrentie.images[a].image_path
        image = int(raw_input('\nPlease Choose an option [0-9]: '))
        print 'Please select an Partition: '
        # Printing all Partitions from Selected Image
        for part in range(len(self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions())):
            partition_pointer = self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part]
            print '\t[' + str(part) + '] ' + partition_pointer.desc + " - " + str(partition_pointer.size / 1024) + "MB"

        part = int(raw_input('\nPlease Choose an option [0-9]: '))
        return self.hoofdmenu_refrentie.images[image].ewf_img_info.get_partitions()[part]

    def find_images(self):
        self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files_rapport()

    def cli(self):
        while True:
            print "\t[1] Identify Browsers"
            print "\t[2] Attributes"
            print "\t[3] Back"

            input = int(raw_input('Please choose an option [0-9]: '))
            if input == 1:
                self.identify_browser_windows()
            if input == 2:
                self.attributes()
            if input == 3:
                break

    def attributes(self):
        while True:
            print "\t[1] Cookies"
            print "\t[2] Bookmarks"
            print "\t[3] History"
            print "\t[4] Downloads"
            print "\t[5] Chrome Login"
            print "\t[6] Chrome History"
            print "\t[7] Chrome Cookies"
            print "\t[8] Chrome Top Sites"
            print "\t[9] Back"

            input = int(raw_input('Please choose an option [0-9]: '))
            if input == 1:
                self.cookies()
            if input == 2:
                self.bookmarks()
            if input == 3:
                self.history()
            if input == 4:
                self.downloads()
            if input == 5:
                self.chrome_login()
            if input == 6:
                self.chrome_history()
            if input == 7:
                self.cookies_chrome()
            if input == 8:
                self.chrome_topsites()
            if input == 9:
                break

    def identify_browser_windows(self):
        browse_arr = []
        print (23 * "*")
        # self.hoofdmenu_refrentie.images[0].ewf_img_info.get_partitions[0].get_strings()
        partition = self.select_partition()
        for bestand in partition.files:
            if "firefox.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])
            if "opera.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])
            if "chrome.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])
            if "safari.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])
            if "iexplore.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])
            if "microsoftedge.exe" in bestand.name:
                browse_arr.append([bestand.name, bestand.sha256()])

        print "De gevonden browsers zijn: "
        print tabulate(browse_arr, headers=['Naam', 'Sha256'])
        print ""



    def identify_browser_linux(self):
        print""

    class Bookmarks(object):
        pass

    class History(object):
        pass

    class Cookie(object):
        pass



    def loadSession(self):
        """"""
        dbPath = 'places.sqlite'
        engine = create_engine('sqlite:///%s' % dbPath, echo=True)

        metadata = MetaData(engine)
        moz_bookmarks = Table('moz_bookmarks', metadata, autoload=True)
        mapper(self.Bookmarks, moz_bookmarks)

        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def cookies(self):
        cookies_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name:
                # bestand.export_to()
                path = 'cookies.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_cookies = Table('moz_cookies', meta, autoload=True)
                mapper(self.Cookie, moz_cookies)

                Session = sessionmaker(bind=engine)
                session = Session()
                cookies = session.query(self.Cookie).all()
                print 'Gevonden cookie\'s in Mozilla Firefox zijn: '
                for cookie in cookies:
                    cookies_arr.append([cookie.id, cookie.name, cookie.host])
                print tabulate(cookies_arr, headers=["ID","Naam", "Host"])
                clear_mappers()
                #os.remove(path)

            # if type[0] is '.SQLITE3':
            #   print bestand.path + bestand.name

    def cookies_chrome(self):
        cookies_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name:
                # bestand.export_to()
                path = 'cookies_chrome.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_cookies = Table('cookies', meta, autoload=True)
                mapper(self.Cookie, moz_cookies)

                Session = sessionmaker(bind=engine)
                session = Session()
                cookies = session.query(self.Cookie).all()
                print 'Gevonden cookie\'s in Google Chrome zijn: '
                for cookie in cookies:
                    pwd = win32crypt.CryptUnprotectData(cookie.encrypted_value)
                    cookies_arr.append([cookie.host_key, cookie.name, str(pwd[1])])
                print tabulate(cookies_arr, headers=["Host","Naam","Value"])
                clear_mappers()


    def bookmarks(self):
        bookmarks_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'places' in bestand.name:
                # bestand.export_to()
                path = 'places.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_bookmarks = Table('moz_bookmarks', meta, autoload=True)
                mapper(self.Bookmarks, moz_bookmarks)

                Session = sessionmaker(bind=engine)
                session = Session()

                bookmarks = session.query(self.Bookmarks).all()
                print 'Gevonden Bookmarks\'s in Mozilla Firefox zijn: '
                for bookmark in bookmarks:
                    bookmarks_arr.append([bookmark.id, bookmark.title])
                print tabulate(bookmarks_arr, headers=["ID", "Naam"])
                clear_mappers()
                # path.remove()

    def history(self):
        history_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'places' in bestand.name:
                # bestand.export_to()
                path = 'places.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_history = Table('moz_places', meta, autoload=True)
                mapper(self.History, moz_history)

                Session = sessionmaker(bind=engine)
                session = Session()

                history = session.query(self.History).all()
                print 'Gevonden bezochte pagina\'s in Mozilla Firefox zijn: '
                for pagina in history:
                    history_arr.append([pagina.id, pagina.title, pagina.url])
                print tabulate(history_arr, headers=["ID", "Naam", "URL"])
                clear_mappers()

    def downloads(self):
        downloads_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'downloads' in bestand.name:
                # bestand.export_to()
                path = 'downloads.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_cookies = Table('moz_cookies', meta, autoload=True)
                mapper(self.Cookie, moz_cookies)

                Session = sessionmaker(bind=engine)
                session = Session()
                downloads = session.query(self.Cookie).all()
                print 'Gevonden download\'s in Mozilla Firefox zijn: '
                for download in downloads:
                    downloads_arr.append([download.name, download.source])
                print tabulate(downloads_arr, headers=["Naam", "Afkomst"])
                clear_mappers()

    def chrome_login(self):
        chrome_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name: #cookies = Login Data
                #bestand.export_to()
                path = 'Login Data.sqlite'  # "Database\\" + bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_cookies = Table('logins', meta, Column("origin_url", Integer, primary_key=True), autoload=True)
                mapper(self.Cookie, moz_cookies)

                Session = sessionmaker(bind=engine)
                session = Session()
                cookies = session.query(self.Cookie).all()
                print 'Gevonden login\'s in Google Chrome zijn: '
                for cookie in cookies:
                    pwd = win32crypt.CryptUnprotectData(cookie.password_value)
                    #koenkie = self.hoofdmenu_refrentie.is_ascii(cookie)
                    chrome_arr.append([cookie.origin_url, cookie.username_value, cookie.times_used, str(pwd[1])])
                print tabulate(chrome_arr, headers=["URL","Username","Hoe vaak gebruikt","Wachtwoord"])
                clear_mappers()
                # os.remove(path)

    def chrome_history(self):
        chrome_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name:
                # bestand.export_to()
                path = 'History.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_cookies = Table('urls', meta, Column("id", Integer, primary_key=True), autoload=True)
                mapper(self.Cookie, moz_cookies)

                Session = sessionmaker(bind=engine)
                session = Session()
                cookies = session.query(self.Cookie).all()
                print 'Gevonden bezochte pagina\'s in Google Chrome zijn: '
                for cookie in cookies:
                    #koenkie = self.hoofdmenu_refrentie.is_ascii(cookie)
                    chrome_arr.append([cookie.id, cookie.url, cookie.title, cookie.visit_count])
                print tabulate(chrome_arr, headers=["ID", "URL", "Naam", "Hoe vaak bezocht"])
                clear_mappers()
                #os.remove(path)

    def chrome_topsites(self):
        chrome_arr = []
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            # Checken of bestand van type sqlite3 is
            # if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name:
                # bestand.export_to()
                path = 'Top Sites.sqlite'  # bestand.name
                engine = create_engine('sqlite:///%s' % path, echo=False)
                meta = MetaData(engine)
                moz_history = Table('thumbnails', meta, autoload=True)
                mapper(self.Cookie, moz_history)

                Session = sessionmaker(bind=engine)
                session = Session()
                cookies = session.query(self.Cookie).all()
                print 'Meest bezochte pagina\'s in Google Chrome zijn: '
                for cookie in cookies:
                    #koenkie = self.hoofdmenu_refrentie.is_ascii(cookie)
                    chrome_arr.append([cookie.url, cookie.title, cookie.boring_score])
                print tabulate(chrome_arr, headers=["URL", "TITLE", "Boring Score(in %)"])
                clear_mappers()
                #os.remove(path)


    def run(self):
        print 'Hallo Wereld, dit is de Browsermodule!'
        self.cli()
        # for partitie in self.main.images[0].ewf_img_info.partities:
        #    print partitie.desc

        # for bestand in self.main.images[0].ewf_img_info.partities[0].files:
        #    print bestand.name

        '''if "firefox.exe" in bestand.name:
            print "firefox gevonden \t" + bestand.name + '\t' + bestand.sha256()
        if "opera.exe" in bestand.name:
            print "opera gevonden \t" + bestand.name + '\t' + bestand.sha256()'''

        '''def generate_hashlist(self):
        #TODO: Selecteren van image
        self.hoofdmenu_refrentie.images[0].ewf_img_info.partition_report()
        input = int(raw_input('Please choose an parition to generate hashlist for [0-9]: '))
        self.hoofdmenu_refrentie.images[0].ewf_img_info.get_partitions()[input].files_rapport()'''

        # dbPath = self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files[486]
        # engine = create_engine('sqlite:///%s' % dbPath, echo=True)

        '''# Create a MetaData instance
        metadata = MetaData()
        print metadata.tables

        # reflect db schema to MetaData
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
