from django.db import models


class Transaction(models.Model):
    """ TODO : Table Normalization """
    date = models.DateField(db_index=True)
    transaction_type = models.CharField(max_length=250)
    country = models.CharField(max_length=100, db_index=True)
    currency = models.CharField(max_length=100)
    net = models.FloatField()
    vat = models.FloatField()


class Uploads(models.Model):
    file = models.FileField(upload_to='uploads/')
