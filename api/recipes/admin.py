from django.contrib import admin
from .models import Ingredient, Item, Recipe, Section, \
                    Source, Supply, Trip, Unit, Usage

for model in [Ingredient, Item, Recipe, Section, \
              Source, Supply, Trip, Unit, Usage]:

  admin.site.register(model)

