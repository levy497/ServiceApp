from init import db

class Funkcje(db.Model):
    __tablename__ = 'funkcje'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255), nullable=False)
    uzytkownicy = db.relationship('Uzytkownicy', backref='funkcje', lazy=True)

class Uzytkownicy(db.Model):
    __tablename__ = 'uzytkownicy'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    nazwisko = db.Column(db.String(255), nullable=False)
    funkcje_id = db.Column(db.Integer, db.ForeignKey('funkcje.id'))
    telefon = db.Column(db.String(20))
    haslo = db.Column(db.String(255), nullable=False)
    logowania = db.relationship('Logowanie', backref='uzytkownicy', lazy=True)
    usterki = db.relationship('Usterki', backref='uzytkownicy', lazy=True)
    czlonkowie_zespolow = db.relationship('CzlonkowieZespolow', backref='uzytkownicy', lazy=True)

class Logowanie(db.Model):
    __tablename__ = 'logowanie'
    uzytkownicy_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'), unique=True)
    login = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    haslo = db.Column(db.String(255), nullable=False)

class Modele(db.Model):
    __tablename__ = 'modele'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255), nullable=False)
    parametry_techniczne = db.Column(db.Text)
    pojazdy = db.relationship('Pojazdy', backref='modele', lazy=True)

class Pojazdy(db.Model):
    __tablename__ = 'pojazdy'
    id = db.Column(db.Integer, primary_key=True)
    rejestracja = db.Column(db.String(15), nullable=False)
    modele_id = db.Column(db.Integer, db.ForeignKey('modele.id'))
    rocznik = db.Column(db.Integer)
    uwagi = db.Column(db.Text)
    usterki = db.relationship('Usterki', backref='pojazdy', lazy=True)

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255), nullable=False)
    usterki = db.relationship('Usterki', backref='status', lazy=True)

class Usterki(db.Model):
    __tablename__ = 'usterki'
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer, db.ForeignKey('pojazdy.id'))
    uzytkownicy_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    priorytet = db.Column(db.Boolean)
    opis = db.Column(db.String(255))
    komentarz_serwisanta = db.Column(db.Text)  # Nowe pole dla komentarza serwisanta
    usterki_na_zespoly = db.relationship('UsterkiNaZespoly', backref='usterka', lazy=True)

class UsterkiNaZespoly(db.Model):
    __tablename__ = 'usterki_na_zespoly'
    usterki_id = db.Column(db.Integer, db.ForeignKey('usterki.id'), primary_key=True)
    zespoly_id = db.Column(db.Integer, db.ForeignKey('zespoly.id'), primary_key=True)

class Zespoly(db.Model):
    __tablename__ = 'zespoly'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255), nullable=False)
    usterki_na_zespoly = db.relationship('UsterkiNaZespoly', backref='zespoly', lazy=True)
    czlonkowie_zespolow = db.relationship('CzlonkowieZespolow', backref='zespoly', lazy=True)

class CzlonkowieZespolow(db.Model):
    __tablename__ = 'czlonkowie_zespolow'
    uzytkownicy_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'), primary_key=True)
    zespoly_id = db.Column(db.Integer, db.ForeignKey('zespoly.id'), primary_key=True)
