from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + ", " + \
            "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    MICRO = 'Micro'
    SEDAN = 'Sedan'
    CUV ='CUV'
    SUV = 'SUV'
    HATCHBACK = 'Hatchback'
    ROADSTER = 'Roadster'
    PICKUP = 'Pickup'
    VAN = 'Van'
    COUPE = 'Coupe'
    SUPERCAR = 'Supercar'
    CAMPERVAN = 'Campervan'
    MINITRUCK = 'Mini Truck'
    CABRIOLET = 'Cabriolet'
    MINIVAN = 'Minivan'
    TRUCK = 'Truck'
    BIGTRUCK = 'Big Truck'
    WAGON = 'Wagon'
    CAR_TYPE = [
        (MICRO, 'Micro'),
        (SEDAN, 'Sedan'),
        (CUV,'CUV'),
        (SUV, 'SUV'),
        (HATCHBACK,'Hatchback'),
        (ROADSTER,'Roadster'),
        (PICKUP,'Pickup'),
        (VAN,'Van'),
        (COUPE,'Coupe'),
        (SUPERCAR,'Supercar'),
        (CAMPERVAN,'Campervan'),
        (MINITRUCK,'Mini Truck'),
        (CABRIOLET,'Cabriolet'),
        (MINIVAN,'Minivan'),
        (TRUCK,'Truck'),
        (BIGTRUCK,'Big Truck'),
        (WAGON, 'Wagon')
    ]
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerid = models.IntegerField(default=0)
    name = models.CharField(null=False, max_length=30)
    modeltype = models.CharField(max_length=10, choices=CAR_TYPE, default=SEDAN)
    engine = models.CharField(max_length=30)
    year = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + ", " + \
            "Type: " + self.type + ", " + \
            "Engine: " + self.engine + ", " + \
            "Year: " + self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer():


# <HINT> Create a plain Python class `DealerReview` to hold review data
