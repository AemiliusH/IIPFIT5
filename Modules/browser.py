import pyewf
import pytsk3
import sqlite3

from Utils.FileType import *
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
from tabulate import tabulate


class Browser():
    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu

    def tel_files(self):
        for file in range(len(self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files)):
            try:
                print '\t[' + str(file) + '] ' + \
                      self.hoofdmenu_refrentie.images[0].ewf_img_info.get_partitions()[0].files[file].name
            except:
                pass

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
            print "\t[2] Cookies"
            print "\t[3] Bookmarks"
            print "\t[4] History"
            print "\t[5] Back"

            input = int(raw_input('Please choose an option [0-9]: '))
            if input == 1:
                self.identify_browser_windows()
            if input == 2:
                self.cookies()
            if input == 3:
                self.bookmarks()
            if input == 4:
                self.history()
            if input == 5:
                self.tel_files()

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

        print tabulate(browse_arr, headers=['Naam', 'Sha256'])
        print ""

    def identify_browser_linux(self):
        print""

    class Bookmarks(object):
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
        paritie = self.select_partition()
        for bestand in paritie.files:
            type = FileType(bestand).analyse()

            #Checken of bestand van type sqlite3 is
            #if 'SQLITE3' in type[0]:
            if 'cookies' in bestand.name:
                #bestand.export()
                engine = create_engine('sqlite:///%s' % bestand.name, echo=True)
                meta = MetaData(engine)
                moz_bookmarks = Table('moz_cookies', meta, autoload=True)
                mapper(self.Bookmarks, moz_bookmarks)

                Session = sessionmaker(bind=engine)
                session = Session()
                print session.query(self.Bookmarks).all()


            #if type[0] is '.SQLITE3':
             #   print bestand.path + bestand.name

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

    def bookmarks(self):
        for bestand in self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files:
            if "places.sqlite" in bestand.name:
                dbPath = self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files[486]
                engine = create_engine('sqlite:///%s' % dbPath, echo=True)

                # Create a MetaData instance
                metadata = MetaData()
                print metadata.tables

                # reflect db schema to MetaData
                metadata.reflect(bind=engine)
                print metadata.tables

    def history(self):
        for bestand in self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files:
            if "places.sqlite" in bestand.name:
                for x in bestand.get_strings():
                    print str(x)

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
