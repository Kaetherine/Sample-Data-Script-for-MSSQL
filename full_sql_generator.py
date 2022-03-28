from faker import Faker

fake = Faker(['de_DE'])

setup_script = open('database_setup.sql', 'w')

create_db = '''
     USE master
     GO
     IF NOT EXISTS (
     SELECT name
     FROM sys.databases
     WHERE name = N'Trainings Camp'
     )
     CREATE DATABASE [Trainings Camp]
     GO
     '''
setup_script.write(create_db)
setup_script.write('\n')

create_tables = '''
     USE [Trainings Camp]
     GO

     CREATE TABLE dbo.Members(
     member_id		          INT                 NOT NULL   PRIMARY KEY,
     firstname			     [NVARCHAR](50)      NOT NULL,
     surname			     [NVARCHAR](50)      NOT NULL,
     birthday  	          DATE			     NOT NULL,
     phone			     [NVARCHAR](50)      NOT NULL,
     street			     [NVARCHAR](50)      NOT NULL,
     number			     [NVARCHAR](5)	     NOT NULL,
     zip				     [NVARCHAR](5)	     NOT NULL
     );

     CREATE TABLE dbo.Activities(
     activity_id		     INT				NOT NULL   PRIMARY KEY,
     activity_name	          [NVARCHAR](50)      NOT NULL,
     provider_id		     [NVARCHAR](10)      NOT NULL
     );

     CREATE TABLE dbo.Bookings(
     booking_id		     INT			     NOT NULL   PRIMARY KEY,
     activity_id		     [NVARCHAR](10)      NOT NULL,
     date_			     DATE			     NOT NULL,
     time_			     TIME			     NOT NULL
     );

     CREATE TABLE dbo.Providers(
     provider_id		     INT				NOT NULL   PRIMARY KEY,
     session_price	          [NVARCHAR](50)      NOT NULL,
     provider			     [NVARCHAR](100)     NOT NULL,
     tax_vat_no		     [NVARCHAR](50)	     NOT NULL,
     phone			     [NVARCHAR](50)      NOT NULL,
     street			     [NVARCHAR](50)      NOT NULL,
     number			     [NVARCHAR](5)	     NOT NULL,
     zip				     [NVARCHAR](5)	     NOT NULL
     );

     '''
setup_script.write(create_tables)
setup_script.write('\n')

for i in range(1, 25):
     member_id = i
     firstname = fake.first_name_female()
     surname = fake.last_name()
     year = fake.random_int(min = 1992, max = 2000)
     month = fake.random_int(min = 1, max = 12)
     day = fake.random_int(min = 1, max = 29)
     birthday = f'{year}-{month}-{day}'
     phone = fake.phone_number()
     street = fake.street_name()
     number = fake.random_int(min = 1, max = 150)
     zip = fake.postcode()

     insert_member = f'''
          INSERT INTO dbo.Members(
               [member_id],[firstname],[surname],[birthday],
               [phone], [street], [number], [zip]
               )
          VALUES(
               {member_id}, '{firstname}', '{surname}', '{birthday}',
               '{phone}', '{street}', '{number}', '{zip}'
               )
          GO
          '''
     setup_script.write(insert_member)
setup_script.write('\n')

for i in range(1, 6):
     provider_id = i
     session_price = fake.pyfloat(min_value = 300, max_value = 600, right_digits = 2)      
     provider = fake.company()	     		     
     tax_vat_no = fake.vat_id()
     phone = fake.phone_number() 
     street = fake.street_name()   
     number = fake.random_int(min = 1, max = 150)
     zip = fake.postcode()

     insert_provider = f'''
          INSERT INTO dbo.Providers(
               [provider_id],[session_price],[provider],[tax_vat_no],
               [phone], [street], [number], [zip]
               )
          VALUES(
               {provider_id}, '{session_price}', '{provider}',
               '{tax_vat_no}', '{phone}', '{street}', {number}, '{zip}'
               )
          GO
          '''
     setup_script.write(insert_provider)
setup_script.write('\n')

activities = [
     'Pilates', 'Jivamukti Yoga', 'Vinyasa Yoga', 'Rope Skipping',
     'Physio Therapie', 'Massage', 'Meditation', 'Rudern',
     'Rudern am Kabelzug', 'Schwimmen']
activity_id = 0
for activity in activities:
     activity_id += 1
     provider_id = fake.random_int(min = 1, max = 5)
     insert_activities = f'''
          INSERT INTO dbo.Activities(
               [activity_id],[activity_name],[provider_id]
               )
          VALUES(
               {activity_id}, '{activity}', '{provider_id}'
               )
          GO
          '''
     setup_script.write(insert_activities)
setup_script.write('\n')

for i in range(1, 38):
     booking_id = i
     activity_id = fake.random_int(min = 1, max = len(activities))
     day = fake.random_int(min = 7, max = 30)
     date_ = f'2023-06-{day}'
     hour = fake.random_int(min = 9, max = 19)
     time_ = f"'{hour}:00'"

     insert_bookings = f'''
          INSERT INTO dbo.Bookings(
               [booking_id],[activity_id],[date_], [time_]
               )
          VALUES(
               {i}, '{activity_id}', '{date_}', {time_}
               )
          GO
          '''

     setup_script.write(insert_bookings)
setup_script.write('\n')

setup_script.close()