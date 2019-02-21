from django.db import models
from django.contrib.auth.models import Permission, User


# Create your models here.

class College(models.Model):
	name=models.CharField(max_length=100)
	def avg_rating(self):
		tot=list(map(lambda x:x.rating,self.review_set.all()))
		avg=0
		for i in range(len(tot)):
			avg+=tot[i]
		avg/=len(tot)
		return(avg)
			
	def __unicode__(self):
		return self.name


class Review(models.Model):
    college=models.ForeignKey(College,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('Review Publishing Date')
    user_name=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    rating=models.FloatField()