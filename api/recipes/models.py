from django.db import models

import datetime


# section of the grocery store to find a food item
#
class Section(models.Model):
  name = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self):
    return self.name


# a food item
#
class Item(models.Model):
  code    = models.CharField(max_length=20, unique=True, null=False)
  section = models.ForeignKey(Section, on_delete=models.RESTRICT, blank=True, null=True)
  name    = models.CharField(max_length=100)
  
  def __str__(self):
    return f'{self.name} ({self.code})'


# g, ml, cups, tbsp, tsp
class Unit(models.Model):
  code        = models.CharField(max_length=10, unique=True, null=False)
  description = models.CharField(max_length=100)
  
  class Meta:
    constraints = [ models.UniqueConstraint(name='unit_code_unique',
                                            fields=['code']) ]

  def __str__(self):
    return self.code


class Recipe(models.Model):
  code     = models.CharField(max_length=40)
  name     = models.CharField(max_length=100, blank=False, null=False)
  extended = models.CharField(max_length=100, blank=True, null=True)
  source   = models.CharField(max_length=1000, blank=True)

  class Meta:
    constraints = [ models.UniqueConstraint(name='recipe_code_unique',
                                            fields=['code']) ]

  def __str__(self):
    if self.extended:
      return f'{self.name} {self.extended} ({self.code})'
    else:
      return f'{self.name} ({self.code})'


class Ingredient(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  item   = models.ForeignKey(Item, on_delete=models.RESTRICT)
  amount = models.FloatField(null=False)
  units  = models.ForeignKey(Unit, on_delete=models.RESTRICT)

  def __str__(self):
    return f'{self.amount} {self.units.code} - {self.item.name}'


# a grocery store or market
#
class Source(models.Model):
  name   = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self):
    return self.name


# a trip to the store/market. all incoming Supplies link to a Trip
#
class Trip(models.Model):
  source   = models.ForeignKey(Source, on_delete=models.RESTRICT)
  when     = models.DateTimeField(null=False)
  comments = models.CharField(max_length=500, null=True, blank=True)

  def __str__(self):
    return f'{self.source.name} on {self.when.strftime("%b %d")}'


# an amount of something we added to our inventory, with expiry date
#
class Supply(models.Model):
  trip    = models.ForeignKey(Trip, on_delete=models.CASCADE)
  item    = models.ForeignKey(Item, on_delete=models.RESTRICT)
  amount  = models.FloatField(null=False)
  units   = models.ForeignKey(Unit, on_delete=models.RESTRICT)
  expires = models.DateField(null=True)
  price   = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0)

  def __str__(self):
    return f'{self.amount} {self.units.code} {self.item.name} bought {self.trip.when.strftime("%x")}'


# a reduction in an on-hand ingredient, through usage or expiry
#
class Usage(models.Model):
  supply  = models.ForeignKey(Supply, on_delete=models.CASCADE)
  when    = models.DateTimeField(null=False, auto_now_add=True)
  amount  = models.FloatField(null=False)

  # usage method, did we use it or throw it away
  EXPIRED = 'E'
  USED_IN_COOKING = 'U'

  SHRINK_METHOD = [
    (EXPIRED        , 'Expired'),
    (USED_IN_COOKING, 'Used in cooking'),
  ]
  
  method  = models.CharField(max_length=1, choices=SHRINK_METHOD, default=USED_IN_COOKING)

  def __str__(self):
    return str(self.amount) + ' of ' + self.supply.__str__()

