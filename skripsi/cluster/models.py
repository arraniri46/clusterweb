from django.db import models

# Create your models here.

class nasabah(models.Model):
    
    no = models.CharField(max_length=200)
    pekerjaan = models.CharField(max_length=200)
    objek = models.CharField(max_length=200)
    harga = models.CharField(max_length=200)
    tenor = models.CharField(max_length=200)
    kolektibilitas = models.CharField(max_length=200) 


    def __str__(self):
        """Unicode representation of MODELNAME."""
        pass

