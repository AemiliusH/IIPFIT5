from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, DateTime, select, update
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
from sqlalchemy import Column, Integer
from tabulate import tabulate
from datetime import datetime

from Models import *


class Database():
    userid = -1
    caseid = -1

    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu
        # path = '..//DataBase//DB.sqlite' voor testen vanuit deze class
        path = 'DataBase//DB.sqlite'
        engine = create_engine('sqlite:///%s' % path, echo=False)
        self.conn = engine.connect()
        self.meta = MetaData(bind=engine)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.pad = None
        if hoofdmenu is not None:
            self.setSettings()
        else:
            self.getSettings()

    def setSettings(self):
        settings = open('settings.cfg', 'w+')
        settings.write(str(self.userid)+';'+str(self.caseid))
        settings.close()

    def getSettings(self):
        settings = open('settings.cfg', 'r')
        inhoud = settings.read().split(';')
        self.userid = int(inhoud[0])
        self.caseid = int(inhoud[1])

    def timestamp(self):
        return str('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')

    def select_user(self):
        # inladen self.userid voor later gebruik
        print "Selecteer een gebruiker: "

        for name in self.session.query(User):
            print '\t[' + str(name.ID) + \
                '] ', name.Naam, name.Achternaam

        self.userid = raw_input("Kies een optie: ")
        self.setSettings()

    def add_user(self):
        voornaam = raw_input("Vul uw voornaam in: ")
        achternaam = raw_input("Vul uw achternaam in: ")

        user = User(Naam=voornaam, Achternaam=achternaam, Datum=datetime.now())

        self.session.add(user)
        self.session.commit()

        self.write_log("Nieuwe gebruiker toegevoegd: " +
                       voornaam + " " + achternaam)

    def select_case(self):
        # TEST database kan niet een user geselecteerd hebben en tegelijk een nieuwe toevoegen.
        # Lees image paden uit met ;
        # Leest case ID uit

        case = self.session.query(Case)
        for i in case:
            print '[' + str(i.ID) + ']', i.Naam, i.Datum
        case_nr = int(raw_input("Kies een optie"))
        self.caseid = case_nr
        self.setSettings()
        select_st = select([Case]).where(
            Case.ID == case_nr)
        selected_case = self.conn.execute(select_st)
        for row in selected_case:
            images = row.Image.split(';')
            for image in images:
                if len(image) > 5:
                    self.hoofdmenu_refrentie.add_image(image)

    def add_case(self):
        naam = str(raw_input("Case naam: "))
        case = Case(Image='', Naam=naam, Datum=datetime.now())

        self.session.add(case)
        self.session.commit()

        self.write_log("Case toegevoegd")

    def add_image(self):
        img = None
        img_path = None
        select_st = select([Case]).where(
            Case.ID == self.caseid)
        selected_case = self.conn.execute(select_st)

        # Eerst alle images uitlezen, vervolgens herschrijven
        print "De ingeladen Images zijn: "
        for row in selected_case:
            print row.Image
            img = row.Image

        path = raw_input("Voer het pad naar uw nieuwe Image in: ")
        self.hoofdmenu_refrentie.add_image(path)

        # werk met ;;;; om meerdere images toe te voegen
        self.session.query(Case).filter_by(
            ID=self.caseid).update({"Image": img + ";" + path})
        self.session.commit()

        # Stap loggen!!
        self.write_log("Nieuw Image toegevoegd aan Case")

    def write_log(self, bericht):
        # Log wegschrijven met self.userid en CaseID / Timestamp
        log = Logboek(UserID=self.userid, CaseID=self.caseid,
                      Handeling=bericht, Datum=datetime.now())

        self.session.add(log)
        self.session.commit()

    def write_rapportage(self, titel, rapport):
        # meerdere regels??
        # Wegschrijven met self.userid en CaseID
        data = None
        select_st = select([Case]).where(
            Case.ID == self.caseid)
        selected_case = self.conn.execute(select_st)

        # Eerst alle images uitlezen, vervolgens herschrijven
        print "De ingeladen Images zijn: "
        for row in selected_case:
            print row.Image
            data = row.Image

        rapport = Logboek(UserID=self.userid, CaseID=self.caseid,
                          Titel=titel, Data=rapport, Datum=datetime.now())

        self.session.query(Rapportage).filter_by(
            ID=self.caseid).update({"Data": data + ";" + path})
        self.session.commit()

    # def write_error(self, error):
        # same met self.userid en caseid

    # def write_export(self, naam, meta, doel, bron):
        # wegschrijven met self.userid en caseid

    def user(self):
        while True:
            print "\t[1] Nieuwe User"
            print "\t[2] Bestaande User kiezen"
            optie = int(raw_input("Kies een optie [1-2] "))
            if optie == 1:
                self.add_user()
            if optie == 2:
                self.select_user()
                self.case()
                break

    def case(self):
        while True:
            print "\t[1] Nieuwe Case"
            print "\t[2] Bestaande Case Kiezen"
            optie = int(raw_input("Kies een optie [1-2] "))
            # date = DateTime()

            if optie == 1:
                self.add_case()
            if optie == 2:
                self.select_case()
                break

    def run(self):
        self.user()
