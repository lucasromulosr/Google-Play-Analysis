from django.db import models
from django.core.validators import MinValueValidator

# connect db
# define dicts
# ver se vai ficar aqui msm ou em outro lugar

# Create your models here.

class Application(models.Model):

    _id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    star = models.DecimalField(max_digits=2, decimal_places=1)
    num_reviews = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self._id


class comment():
    pass