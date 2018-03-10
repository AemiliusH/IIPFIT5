import sys



class Case():
    naam = ''
    locatie = ''
    onderzoekers = []

    #TODO Cases via mysql laten werken ipv via losse files

    def __init__(self, main):
        self.main = main 
        self.sql = main.sql 

        cases_raw = self.sql.find_all('case')

        if cases_raw is None or len(cases_raw) == 0:
            print "[Case] No excisting case found... Creating new one"
            self.create() 
        else: 
            print "[Case] Found existing cases: "
            for a in range(len(cases_raw)):
                blocks = cases_raw[a][1].split(';')
                print "\t[" + str(a) + "] Name: " + blocks[0] + " Location: " + blocks[1]

            print "\t[" + str(len(cases_raw) + 1) + "] Create New Case" 
            input = int(raw_input("[Case] Please choose an option [0-9]: "))

            if input == len(cases_raw) + 1:
                self.create() 
            else:
                self.name = cases_raw[input][0]
                self.locatie = cases_raw[input][1]
                

    def create(self): 
        self.naam = raw_input("[Case] Please enter case name: ")
        self.locatie = raw_input("[Case] Please enter case location: ")
        self.sql.write('case', self.naam + ";" + self.locatie)
