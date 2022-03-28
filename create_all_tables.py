table_creator = """
	SET statement_timeout = 0;
	SET client_encoding = 'UTF8';
	SET standard_conforming_strings = on;
	SET check_function_bodies = false;
	SET client_min_messages = warning;

	CREATE TYPE spielklasse AS ENUM ('unter Landesliga', 'Landesliga', 'Oberliga', 'Regionalliga', '3. Liga', '2. Bundesliga','1. Bundesliga');
	CREATE TYPE strafe AS ENUM ('gelbe Karte', 'Zeitstrafe', 'gelb-rote Karte', 'rote Karte');
	CREATE TYPE altersklasse AS ENUM ('U13', 'U15', 'U17', 'U19', 'Erwachsene', 'Senioren');
	CREATE TYPE lizenz AS ENUM ('keine', 'C-Lizenz', 'B-Lizenz', 'A-Lizenz', 'Diplomebene');
	CREATE TYPE funktion AS ENUM ('AVAR', 'VAR', '4. Offizieller', '2. Assistent', '1. Assistent', 'Schiedsrichter');

	CREATE TABLE PersönlicheStrafen (
		SpielID int NOT NULL,
		Zeitpunkt time NOT NULL ,
		Typ strafe NOT NULL,
		MannschaftsID int NOT NULL
	);

	CREATE TABLE Spiele (
		SpielID SERIAL PRIMARY KEY,
		HeimmannschaftID int NOT NULL ,
		GastmannschaftID int NOT NULL ,
		Strasse char(30) NOT NULL,
		Hausnummer char(10) NOT NULL,
		PLZ char(5),
		Platzname char(30) NOT NULL,
		Datum date NOT NULL ,
		Startzeit time NOT NULL
	);

	CREATE TABLE Mannschaften (
		MannschaftsID SERIAL PRIMARY KEY ,
		VereinsID int NOT NULL ,
		Altersklasse altersklasse NOT NULL ,
		Spielklasse spielklasse  NOT NULL ,
		Rang int
	);

	CREATE TABLE Vereine (
		VereinsID SERIAL PRIMARY KEY ,
		VereinsName char(30) NOT NULL UNIQUE
	);

	CREATE TABLE Vereinsmitglieder (
		MitgliedsNr SERIAL PRIMARY KEY,
		VereinsID int NOT NULL ,
		Vorname char(30) NOT NULL ,
		Nachname char(30) NOT NULL ,
		Geburtstag date NOT NULL ,
		Strasse char(50) NOT NUll ,
		Hausnummer char(5) NOT NUll ,
		PLZ char(5),
		TelNr char(30) NOT NULL ,
		EMail char(50) NOT NULL
	);

	CREATE TABLE Trainer (
		MitgliedsNr int UNIQUE NOT NULL,
		Trainerlizenz lizenz NOT NULL
	);
	CREATE TABLE Spieler (
		MitgliedsNr int UNIQUE NOT NULL ,
		PassNr SERIAL UNIQUE NOT NULL
	);

	CREATE TABLE Ansetzungen (
		Ansetzer_AusweisNr int,
		Sr_AusweisNr int NOT NULL ,
		SpielID int  NOT NULL ,
		Funktion funktion NOT NULL
	);
	CREATE TABLE Schiedsrichter (
		MitgliedsNr int UNIQUE,
		AusweisNr SERIAL UNIQUE NOT NULL,
		Lehrgemeinschaft char(30) NOT NULL ,
		Jahresprüfung date NOT NULL ,
		HöchsteSpielklasseLeitung spielklasse NOT NULL ,
		HöchsteAltersklasseLeitung altersklasse NOT NULL,
		AkIDLeitung int,
		aktiv boolean NOT NULL DEFAULT true
	);

	CREATE TABLE Ansetzer (
		AusweisNr int UNIQUE NOT NULL,
		höchsteSpielklasseAnsetzung spielklasse NOT NULL,
		höchsteAltersklasseAnsetzung altersklasse NOT NULL,
		AkIDAnsetzung int NOT NULL
	);

	CREATE TABLE Favoriten (
		HauptSr_AusweisNr int NOT NULL ,
		AssistentSr_AusweisNr int NOT NULL,
		PRIMARY KEY (HauptSr_AusweisNr, AssistentSr_AusweisNr)
	);
	CREATE TABLE Freitermine (
		Sr_AusweisNr int NOT NULL ,
		Datum date NOT NULL ,
		Startzeit time  DEFAULT '00:00' ,
		Endzeit time DEFAULT '23:59'
	);

	CREATE TABLE Ansetzungskreise (
		AkID SERIAL PRIMARY KEY ,
		Name char(30) UNIQUE NOT NULL
	);
	CREATE TABLE PLZ (
		PLZ char(5) PRIMARY KEY ,
		AkID int ,
		Ort char(30)  NOT NULL
	);
	"""