import pyewf 
import pytsk3

class Browser(): 

    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu  
 
    def test(self):
        print self.hoofdmenu_refrentie
 
    def find_images(self):
        self.hoofdmenu_refrentie.images[0].ewf_img_info.partities[0].files_rapport()
            

    def run(self):
        print 'Hallo Wereld, dit is de fotomodule!'
        #for partitie in self.main.images[0].ewf_img_info.partities:
        #    print partitie.desc

        #for bestand in self.main.images[0].ewf_img_info.partities[0].files:
        #    print bestand.name