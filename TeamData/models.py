from django.db import models

class Team(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'
class Person(models.Model):    
    class Meta:
        verbose_name_plural = 'People'

    name = models.CharField(max_length=50)
    description=models.TextField()
    team=models.ManyToManyField(Team)
    position=models.CharField(max_length=50,default='',blank=True)
    picture=models.ImageField(upload_to='TeamImages/')

    def __str__(self):
        return f'{self.name} - {self.team}'
        
