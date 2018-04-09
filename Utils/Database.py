from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, DateTime, select
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
from sqlalchemy import Column, Integer
from tabulate import tabulate

from Models import *

class Database():
    userid = 2
    caseid = -1
    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu
        path = 'DataBase//DB.sqlite'  # path = '..//DataBase//DB.sqlite' voor testen vanuit deze class
        engine = create_engine('sqlite:///%s' % path, echo=False)
        self.conn = engine.connect()
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.pad = None
        self.run()

    def select_user(self):
        #inladen userid voor later gebruik
        print "Welke gebruiker wilt u kiezen?"
        for name in self.session.query(User):
            print name.ID,name.Naam,name.Achternaam
        self.userid = raw_input("Kies een optie")


    def add_user(self, voornaam, achternaam):
        voornaam = raw_input("Vul uw voornaam in: ")
        achternaam = raw_input("Vul uw achternaam in: ")

        user = User(Naam=voornaam, Achternaam=achternaam)

        self.session.add(user)
        self.session.commit()


    def select_case(self):
        # Lees image paden uit met ;
        # Leest case ID uit

        case = self.session.query(Case)
        for i in case:
            print i.ID, i.Naam, i.Image
        case_nr = int(raw_input("Kies een optie"))
        self.caseid = case_nr
        select_st = select([Case]).where(
            Case.ID == case_nr)
        selected_case = self.conn.execute(select_st)
        for row in selected_case:
            print 'Inladen van ', row.Image
            self.hoofdmenu_refrentie.add_image(row.Image)

    def select_image(self, path):


    def add_case(self, naam):

    def add_image(self, path):
        # Eerst alle images uitlezen, vervolgens herschrijven
        # werk met ;;;;   om meerdere images toe te voegen

        # Stap loggen!!

    def write_log(self, log):
        # Log wegschrijven met UserID en CaseID / Timestamp


    def write_rapportage(self, rapport):
        #meerdere regels??
        # Wegschrijven met USerid en CaseID

    def write_error(self, error):
        # same met userid en caseid

    def write_export(self, naam, meta, doel, bron):
        # wegschrijven emt userid en caseid




    #def add_image(self, path):
        #self.write_log('Heeft image toegevoegd aan case')

    def cli(self):
        while True:
            print "\t[1] Nieuwe Case"
            print "\t[2] Bestaande Case Kiezen"
            print "\t[3] Terug"

            optie = int(raw_input("Kies een optie [0-9]"))
            # date = DateTime()

            if optie == 1:
                self.add_case()


            if optie == 2:
                self.select_case()


            if optie == 3:
                break

    def add_case(self):
        image = str(raw_input("Voer het pad naar de image in"))
        naam = str(raw_input("Voer de naam van de case in: "))

        case = Case(Image=image, Naam=naam)

        self.session.add(case)
        self.session.commit()

    def select_case(self):






    def run(self):
        self.cli()





















