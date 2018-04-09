# importeer alle modules
import pyewf
import pytsk3
import exifread

from Utils.FileType import *
from tabulate import tabulate
from StringIO import StringIO


class Foto():
    # de init functie start de class op
    def __init__(self, main):
        self.main = main

    # als de input 2 is vanuit de main module dan start die de functie run op en voert die alle code uit onder deze functie
    def run(self):
        # dit menu blijft die herhalen omdat het altijd true is
        while True:
            print 'Hallo Wereld, dit is de fotomodule! \nMaak je keuze:'
            print '\t[1] Lijst van alle bestanden met hash'
            print '\t[2] Lijst van alle foto\'s'
            print '\t[3] Lijst van alle camera\'s'
            print '\t[4] Lijst van alle bestanden per camera'
            print '\t[5] lijst van bestanden met EXIF informatie'
            print '\t[0] Terug'

            # hier zijn alle uitvoeringen van het menu, hij roept per input een andere functie op
            input = int(raw_input('Maak een keuze [0-9]'))
            if input == 1:
                self.generate_hashlist()
            if input == 2:
                self.isfoto()
            if input == 3:
                self.soortcamera()
            if input == 4:
                self.bestandpercamera()
            if input == 5:
                self.heeftexif()
            if input == 0:
                break

    def get_fotos(self):
        partities = self.main.images[0].ewf_img_info.get_partitions()
        # maak een lege array aan en loop door de bestanden van de partities. Als uit de analyse voor een betreffend bestand komt dat de extentie een van de types is, dan voegt die het toe aan de files array.
        files = []
        for bestand in partities[0].files:
            info = FileType(bestand).analyse()
            types = ['ANI', 'BMP', 'CAL', 'FAX', 'GIF', 'IMG', 'JBG', 'JPE', 'JPEG', 'JPG', 'MAC',
                     'PBM', 'PCD', 'PCX', 'PCT', 'PGM', 'PNG', 'PPM', 'PSD', 'RAS', 'TGA', 'TIFF', 'WMF']
            if info[0] in types:
                files.append(bestand)
        return files

    def isfoto(self):
        # dit is precies hetzelfde als de get_fotos functie alleen print die de bestandsnamen in plaats dat die ze returnt
        partities = self.main.images[0].ewf_img_info.get_partitions()
        for bestand in partities[0].files:
            info = FileType(bestand).analyse()
            types = ['ANI', 'BMP', 'CAL', 'FAX', 'GIF', 'IMG', 'JBG', 'JPE', 'JPEG', 'JPG', 'MAC',
                     'PBM', 'PCD', 'PCX', 'PCT', 'PGM', 'PNG', 'PPM', 'PSD', 'RAS', 'TGA', 'TIFF', 'WMF']
            if info[0] in types:
                print bestand.name

    def soortcamera(self):
        # met StringIO open je virtueel een bestand zoals die op je computer zou zijn.
        fabrikanten = []
        for foto in self.get_fotos():
            bestand = StringIO(foto.read_raw_bytes())
            tags = exifread.process_file(bestand)
            fabriekant = str(tags['Image Make'])
            if fabriekant not in fabrikanten:
                fabrikanten.append(fabriekant)
                print fabriekant

    def bestandpercamera(self):
        # Er is hier voor elke camera soort een array gemaakt, daarna kijkt die met exifread naar de metadata Image make en daaruit haalt die het soort camera en voegt die het aan de goede lijst toe.
        sony = []
        canon = []
        nikon = []
        pentax = []
        olympus = []
        fujifilm = []
        gopro = []
        leica = []
        kodak = []

        issony = "SONY"
        iscanon = "CANON"
        isnikon = "NIKON"
        ispentax = "PENTAX"
        isolympus = "OLYMPUS"
        isfujifilm = "FUJIFILM"
        isgopro = "GOPRO"
        isleica = "LEICA"
        iskodak = "KODAK"

        cameras = []

        for item in self.get_fotos():
            bestand = StringIO(item.read_raw_bytes())

            tags = exifread.process_file(bestand)

            fabrikant = str(tags['Image Make'])
            model = tags['Image Model']

            cameras.append([fabrikant, model])
            if issony in fabrikant:
                sony.append(item.name)
            if iscanon in fabrikant:
                canon.append(item.name)
            if isnikon in fabrikant:
                nikon.append(item.name)
            if ispentax in fabrikant:
                pentax.append(item.name)
            if isolympus in fabrikant:
                olympus.append(item.name)
            if isfujifilm in fabrikant:
                fujifilm.append(item.name)
            if isgopro in fabrikant:
                gopro.append(item.name)
            if isleica in fabrikant:
                leica.append(item.name)
            if iskodak in fabrikant:
                kodak.append(item.name)

        print str(len(cameras)) + " foto's gevonden:"
        if len(sony) >= 1:
            print "sony's: " + str(sony)
        if len(canon) >= 1:
            print "canon's: " + str(canon)
        if len(nikon) >= 1:
            print "nikon's: " + str(nikon)
        if len(pentax) >= 1:
            print "pentax's: " + str(pentax)
        if len(olympus) >= 1:
            print "olympus's: " + str(olympus)
        if len(fujifilm) >= 1:
            print "fujifilm's: " + str(fujifilm)
        if len(gopro) >= 1:
            print "gopro's: " + str(gopro)
        if len(leica) >= 1:
            print "leica's: " + str(leica)
        if len(kodak) >= 1:
            print "kodak's: " + str(kodak)

    def heeftexif(self):
        # loop door de foto's heen en kijk per foto naar de lengte van de exifdata en print dat.
        for item in self.get_fotos():
            bestand = StringIO(item.read_raw_bytes())
            tags = exifread.process_file(bestand)
            print item.name + " heeft " + str(len(tags)) + " regels exifdata"

    def generate_hashlist(self):
        # in de class EWFImgInfo, in de module partition_report krijgt die een adres terug waarna die door alle files loopt en de sha-waarde (van de class FSFileInfo) terug geeft
        self.main.images[0].ewf_img_info.partition_report()
        array = []
        for file in self.main.images[0].ewf_img_info.get_partitions()[0].files:
            array.append([file.name, file.sha256()])

        print tabulate(array, headers=['Naam', 'SHA256'])
