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
    voter_count = models.IntegerField() 

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.birth_date} | {self.party_affiliation}) '
    
    def isDemocrat(self):
        if 'D' in self.party_affiliation:
            return True
        return False
    
    def isRepublican(self):
        if 'R' in self.party_affiliation:
            return True
        return False
        

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = 'C:/Users/newton_voters.csv'
    f = open(filename)
    f.readline() 
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            vc = 0
            v20 = False
            v21t = False
            v21p = False
            v22 = False
            v23 = False

            if (fields[11] == "TRUE"):
                v20 = True
                vc += 1
            if (fields[12] == "TRUE"):
                v21t = True
                vc += 1
            if (fields[13] == "TRUE"):
                v21p = True
                vc += 1
            if (fields[14] == "TRUE"):
                v22 = True
                vc += 1 
            if (fields[15] == "TRUE"):
                v23 = True
                vc += 1

            ln = ''
            if (not(fields[1] == '')):
                ln = fields[1][0] + fields[1][1:].lower()
            fn = fields[2][0] + fields[2][1:].lower()
            result = Voter(last_name=ln,
                            first_name=fn,

                            street_number= int(fields[3]),
                            street_name = fields[4],
                            apartment_number = fields[5], # may be null
                            zip_code = int(fields[6]),
                            
                            birth_date = datetime.strptime(fields[7], "%Y-%m-%d"),
                            registration_date = datetime.strptime(fields[8], "%Y-%m-%d"),
                            party_affiliation = fields[9],
                            precinct_number = fields[10],
                        
                            v20state = v20,
                            v21town = v21t,
                            v21primary = v21p,
                            v22general = v22,
                            v23town = v23,
                            voter_count = vc 
                        )
        
            result.save() # commit to database
            
        except:
            print(f"Skipped: {fields}")
            
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')