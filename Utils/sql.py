from log import * 

class SQL():
    filename = 'sql.cfg'

    #Shit opslaan met csv format ; 
    #[0] type
    #[1] value

    items = [] 

    def read(self):
        self.raw_file = open(self.filename, 'r').read()
        #kijken of file niet leeg is 
        if len(self.raw_file) > 3:
            self.raw_file = self.raw_file.split('\n') 
            DebugLog("Found " + str(len(self.raw_file)) + " object in sql.cfg")
            for object in self.raw_file:
                blocks = object.split('$')
                self.items.append([blocks[0], blocks[1]])

    def find_all(self, type):
        results = []
        for object in self.items:
            if object[0] == type:
                results.append(object)
        return results 

    def write(self, type, object):
        file = open(self.filename, 'a')
        file.write(type + "$" + object)
        file.close() 

    def __init__(self):
        self.read() 
    

