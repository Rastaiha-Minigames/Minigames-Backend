from django.db import models

class Person(models.Model):
    class TeamChoices(models.TextChoices):
        Komite='کمیته برگزاری'
        Fani='فنی'
        Branding='برندینگ'
        Elmi='علمی'
        Resaneh='رسانه'
        Mosabeghe='مسابقه'
    Name = models.CharField(max_length=50)
    Description=models.TextField()
    Team=models.CharField(choices=TeamChoices.choices,default=TeamChoices.Komite,max_length=50)
    Picture=models.ImageField(upload_to='TeamImages/')

    def __str__(self):
        return f"{self.Name} - {self.Team}" 