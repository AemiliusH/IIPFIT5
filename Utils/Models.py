
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

'''CREATE TABLE `User` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Naam`	TEXT NOT NULL,
	`Achternaam`	TEXT NOT NULL
);'''

class User(Base):
    __tablename__ = 'User'
    ID= Column(Integer(), primary_key=True)
    Naam = Column(String(50))
    Achternaam = Column(String(50))
    Datum = Column(DateTime(timezone=True), server_default=func.now())

'''CREATE TABLE `Case` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Image`	INTEGER NOT NULL,
	`Naam`	TEXT NOT NULL,
	`Datum`	INTEGER NOT NULL,
	`UserID`	INTEGER NOT NULL
);'''

class Case(Base):
    __tablename__ = 'Case'
    ID= Column(Integer(), primary_key=True)
    Image = Column(Integer())
    Naam = Column(String(50))
    Datum = Column(DateTime(timezone=True), server_default=func.now())


'''CREATE TABLE `Error_Logs` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Melding`	TEXT NOT NULL,
	`Tijd`	INTEGER NOT NULL,
	`User ID`	INTEGER NOT NULL,
	`Case ID`	INTEGER NOT NULL,
	FOREIGN KEY(`Case ID`) REFERENCES `Case`(`ID`),
	FOREIGN KEY(`User ID`) REFERENCES `User`(`ID`)
);'''

class Error_Logs(Base):
    __tablename__ = 'Error_Logs'
    ID= Column(Integer(), primary_key=True)
    Melding = Column(String(50))
    Tijd = Column(Integer())
    UserID = Column(Integer(), ForeignKey('User.ID'))
    CaseID = Column(Integer(), ForeignKey('Case.ID'))

'''CREATE TABLE `Exports` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`UserID`	INTEGER NOT NULL,
	`CaseID`	INTEGER NOT NULL,
	`Bestandsnaam`	TEXT NOT NULL,
	`MetaData`	TEXT NOT NULL,
	`LocatieBron`	TEXT NOT NULL,
	`LocatieDoel`	TEXT NOT NULL,
	`Datum`	TEXT NOT NULL,
	FOREIGN KEY(`CaseID`) REFERENCES `Case`(`ID`),
	FOREIGN KEY(`UserID`) REFERENCES `User`(`ID`)
);'''


class Exports(Base):
    __tablename__ = 'Exports'
    ID= Column(Integer(), primary_key=True)
    UserID = Column(Integer(), ForeignKey('User.ID'))
    CaseID = Column(Integer(), ForeignKey('Case.ID'))
    Bestandsnaam = Column(String(50))
    MetaData = Column(String(50))
    LocatieBron = Column(String(50))
    LocatieDoel = Column(String(50))
    Datum = Column(DateTime(timezone=True), server_default=func.now())


'''CREATE TABLE `Image` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Naam`	TEXT NOT NULL,
	`Path`	TEXT NOT NULL,
	`Grootte`	INTEGER NOT NULL
);'''

class Images(Base):
    __tablename__ = 'Image'
    ID= Column(Integer(), primary_key=True)
    Naam = Column(String(50))
    Path = Column(String(50))
    Grootte = Column(String(50))


'''CREATE TABLE `Logboek` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`UserID`	INTEGER NOT NULL,
	`CaseID`	INTEGER NOT NULL,
	`Handeling`	TEXT NOT NULL,
	`Tijd`	INTEGER NOT NULL,
	FOREIGN KEY(`CaseID`) REFERENCES `Case`(`ID`),
	FOREIGN KEY(`UserID`) REFERENCES `User`(`ID`)
);'''

class Logboek(Base):
    __tablename__ = 'Logboek'
    ID = Column(Integer(), primary_key=True)
    UserID = Column(Integer(), ForeignKey('User.ID'))
    CaseID = Column(Integer(), ForeignKey('Case.ID'))
    Handeling = Column(String(500))
    Datum = Column(DateTime(timezone=True), server_default=func.now())


'''CREATE TABLE `Rapportage` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`UserID`	INTEGER NOT NULL,
	`CaseID`	INTEGER NOT NULL,
	`Resultaten`	TEXT NOT NULL,
	FOREIGN KEY(`UserID`) REFERENCES `User`(`ID`),
	FOREIGN KEY(`CaseID`) REFERENCES `Case`(`ID`)
);'''


class Rapportage(Base):
    __tablename__ = 'Rapportage'
    ID= Column(Integer(), primary_key=True)
    UserID = Column(Integer(), ForeignKey('User.ID'))
    CaseID = Column(Integer(), ForeignKey('Case.ID'))
    Titel = Column(String(50))
    Data = Column(String(500))
    Datum = Column(DateTime(timezone=True), server_default=func.now())
