from django.db import models
from datetime import datetime

# Create your models here.
class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()

    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()

    birth_date = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField() 

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.birth_date} | {self.party_affiliation}) '

# def load_data():
#     '''Function to load data records from CSV file into Django model instances.'''
#     filename = 'C:/Users/newton_voters.csv'
#     f = open(filename)
#     f.readline() 
#     for line in f:
#         fields = line.split(',')
       
#         try:
#             # create a new instance of Result object with this record from CSV
#             result = Voter(last_name=fields[1],
#                             first_name=fields[2],

#                             street_number= int(fields[3]),
#                             street_name = fields[4],
#                             apartment_number = fields[5], # may be null
#                             zip_code = int(fields[6]),
                            
#                             birth_date = datetime.strptime(fields[7], "%Y-%m-%d"),
#                             registration_date = datetime.strptime(fields[8], "%Y-%m-%d"),
#                             party_affiliation = fields[9],
#                             precinct_number = fields[10],
                        
#                             v20state = bool(fields[11]),
#                             v21town = bool(fields[12]),
#                             v21primary = bool(fields[13]),
#                             v22general = bool(fields[14]),
#                             v23town = bool(fields[15]),
#                         )
        
#             result.save() # commit to database
            
#         except:
#             ## print(f"Skipped: {fields}
#             ""
    
#     print(f'Done. Created {len(Voter.objects.all())} Results.')