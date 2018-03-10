import pyewf
import pytsk3
import binascii
import StringIO
import re
 
from langdetect import detect_langs 
from tabulate import tabulate 
from zipfile import ZipFile

from Utils.FileType import * 

class Bestand():

    def __init__(self, main):
        self.main = main
        self.sql = main.sql 

    def generate_hashlist(self): 
        #TODO: Selecteren van image 
        self.main.images[0].ewf_img_info.partition_report()  
        input = int(raw_input('Please choose an parition to generate hashlist for [0-9]: '))
        self.main.images[0].ewf_img_info.partities[input].files_rapport() 
        
    def generate_timeline(self): 
        print 'Please select an image to create Timeline: '

        for a in range(len(self.main.images)):
            print '\t[' + str(a) + '] '+ self.main.images[a].image_path

        image = int(raw_input('\nPlease Choose an option [0-9]: '))
      
        print 'Please select on what value to order:'
        print '\t[0] File Created'
        print '\t[1] File Modified'
        print '\t[2] File Changed'

        type = int(raw_input('\nPlease Choose an option [0-9]: '))

        print '\t[0] Oldest First'
        print '\t[1] Newest First'

        order = bool(int(raw_input('\nPlease choose an option[0-9]: ')))
      
        print 'Generating List......' 

        timeline = []
        files = self.main.images[image].get_all_files() 
    
        for file in files:
            timeline.append((file.create, file.modify, file.change, file))
 
        timeline = sorted(timeline, key=lambda x:x[type], reverse=order)
        
        array_list = []
        for file in timeline:
            array_list.append(file[3].get_attributes())
        
        print '\t[0] Print Timeline'
        print '\t[1] Export Timeline (CSV)'

        result = int(raw_input('\nPlease choose an option[0-9]: '))

        if result == 0:
            print tabulate(array_list, headers=['Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
        else:
            self.save_array_to_csv(array_list, 'Name;Size;Created;Changed;Modified;MD5;SHA256\n')
                
    def save_array_to_csv(self, array, head):
        filename = raw_input('\nEnter Filename: ')
        file = open(filename + '.csv', 'w')
        file.write(head + '\n')       
        for obj in array:
            file.write(';'.join(str(e) for e in obj) + '\n')

    def detect_language(self):

        print 'Please select an image: '
        
        #Printing all images with their path
        for a in range(len(self.main.images)):
            print '\t[' + str(a) + '] '+ self.main.images[a].image_path

        image = int(raw_input('\nPlease Choose an option [0-9]: '))
      
        print 'Please select an Partition: '
        #Printing all Partitions from Selected Image
        for part in range(len(self.main.images[image].ewf_img_info.partities)):
            print '\t[' + str(part) + '] '+ self.main.images[image].ewf_img_info.partities[part].desc

        part = int(raw_input('\nPlease Choose an option [0-9]: '))

        #Printing all files with ID
        for file in range(len(self.main.images[image].ewf_img_info.partities[part].files)):
            try:
                print '\t[' + str(file) + '] '+ self.main.images[image].ewf_img_info.partities[part].files[file].name
            except:
                pass

        file = int(raw_input('\nPlease select an file: '))

        #Getting object of selected file
        file_handle = self.main.images[image].ewf_img_info.partities[part].files[file]

        #Printing basic information
        print ' ' + '==' * 22  
        print 'Filename:\t' + file_handle.name
        print 'SHA1:\t\t' + str(file_handle.sha1())
        print 'SHA256:\t\t' + str(file_handle.sha256())   

        #Requested language from file  
        file_handle.print_language_table()
        print ' ' + '==' * 22
  
    def generate_ziplist(self):
        #zip = ZipFile(file) 
        #print zip.namelist()  

        files = self.main.images[0].get_all_files()

        timeline = []
        for file in files:
            timeline.append((file.change, file.create, file.modify, file))

        print timeline[0]

        timeline = sorted(timeline, key=lambda bestand:bestand[2], reverse=False)
 
        for file in timeline:
            print 
        print timeline[0][0]

        '''for file in files:
            try:
                for format in self.signatures: 
                    bin = binascii.unhexlify(format['hex']) 
                    head = file.head(len(bin))
                    if bin == head:
                        print file.name,  format['format']
                        break
            except:
                pass
                #data = f.read(len(bin))
            #if(bin == data):
            #    found.append('Byte: '+str(i)+' \tExtension: '+format['ext']+' \tFormat: '+format['format'])
        '''

     
         
    def generate_filetypelist(self):
        print 'Please select an image: '
        
        #Printing all images with their path
        for a in range(len(self.main.images)):
            print '\t[' + str(a) + '] '+ self.main.images[a].image_path

        image = int(raw_input('\nPlease Choose an option [0-9]: '))
      
        print 'Please select an Partition: '
        #Printing all Partitions from Selected Image
        for part in range(len(self.main.images[image].ewf_img_info.partities)):
            print '\t[' + str(part) + '] '+ self.main.images[image].ewf_img_info.partities[part].desc

        part = int(raw_input('\nPlease Choose an option [0-9]: '))

        #Saving files array to local object
        files = self.main.images[image].ewf_img_info.partities[part].files
        file_array = []
        for file in files:
            type = FileType(file).analyse()  
            if type[1] is not '':
                type.append(file.name)
                file_array.append(type )  

        print '\t[0] Print Filetypes'
        print '\t[1] Export Filetypes (CSV)'
        
        input = int(raw_input('\nPlease Choose an option [0-9]: '))

        if input == 0:
            print tabulate(file_array, headers=['Extention', 'Description', 'Filename'])
        else:
            self.save_array_to_csv(file_array, 'Extention;Description;FileName')


    def cli(self):
        while True:
            print ''
            print ' ' + '==' * 22
            print '|                  Bestand                   |'
            print ' ' + '==' * 22
            print ''
            print "\t[1] Generate Hashlist"
            print '\t[2] List ZIP/Archives'
            print '\t[3] Generate Timeline'
            print '\t[4] List Filetypes'
            print '\t[5] Find Used Languages'
            print '\t[6] Back'
            print ''

            input = int(raw_input('Please choose an option [0-9]: '))
            if input == 1: 
                self.generate_hashlist() 
            if input == 2:
                self.generate_ziplist() 
            if input == 3:
                self.generate_timeline() 
            if input == 4:
                self.generate_filetypelist() 
            if input == 5:
                self.detect_language()
            if input == 6:
                break
 
    def run(self):
        if len(self.main.images) == 0:
            print "Please import an image before using modules!"
        else: 
            self.cli() 
 