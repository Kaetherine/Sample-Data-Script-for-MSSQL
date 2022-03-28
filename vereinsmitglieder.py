import random
from faker import Faker

scheme = ['Mitgliedsnr.', 'Vereins_id', 'Vorname', 'Nachname', 'Geb_Datum', 'Straße', 'Hausnr.', 'PLZ', 'Telefon', 'E-Mail']

fake = Faker(['de_DE'])

def create_vereinsmitgl(mitglnr):

    vereinsmitgl = []
    person = fake.simple_profile()
    anreden = ['Prof', 'B.', 'Ing', 'Dr', 'Univ', 'Dipl', 'MBA', 'Frau', 'Herr']
    name = person['name']
    
    if any(anrede in name for anrede in anreden) or person['sex'] == 'M':
        return None
    else:
        mitglnr = mitglnr
        vereinsnr= random.randint(1,39)

        name = name.split()
        vorname = name[0]
        nachname = name[-1]

        geb = str(person['birthdate'])
        geb.replace('datetime.date(', '').replace(')', '')
  
        strasse = fake.street_name()
        hausnr = random.randint(1,151)
        plz = fake.postcode()
        
        phone = fake.phone_number()
        email = person['mail']

        vereinsmitgl.append(str(mitglnr))
        vereinsmitgl.append(str(vereinsnr))
        vereinsmitgl.append(str(vorname).strip())
        vereinsmitgl.append(str(nachname).strip())
        vereinsmitgl.append(str(geb).strip())
        vereinsmitgl.append(str(strasse).strip().replace(',', ''))
        vereinsmitgl.append(str(hausnr).strip())
        vereinsmitgl.append(str(plz).strip())
        vereinsmitgl.append(str(phone).strip().replace('(', '').replace(')', '').replace(' ', '').replace('"', ''))
        vereinsmitgl.append(str(email).strip())

        return vereinsmitgl