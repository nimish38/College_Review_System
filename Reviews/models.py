from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class College(models.Model):
	name = models.CharField(max_length=100)

	def avg_rating(self):
		tot = list(map(lambda x:x.rating,self.review_set.all()))
		avg = 0
		for i in range(len(tot)):
			avg+= tot[i]
		avg/= len(tot)
		return avg

	def avg_p_rating(self):
		tot = list(map(lambda x: x.placement_rate, self.review_set.all()))
		avg = 0
		for i in range(len(tot)):
			avg += int(tot[i])
		avg /= len(tot)
		return avg

	def avg_a_rating(self):
		tot = list(map(lambda x: x.academic_rate, self.review_set.all()))
		avg = 0
		for i in range(len(tot)):
			avg += int(tot[i])
		avg /= len(tot)
		return avg

	def avg_i_rating(self):
		tot = list(map(lambda x: x.infra_rate, self.review_set.all()))
		avg = 0
		for i in range(len(tot)):
			avg += int(tot[i])
		avg /= len(tot)
		return avg

	def __str__(self):
		return self.name


feedback = (
	(1, 'Poor'),
	(2, 'Satisfactory'),
	(3, 'Average'),
	(4, 'Good'),
	(5, 'Excellent'),
)


class Review(models.Model):
	college = models.ForeignKey(College,on_delete=models.CASCADE)
	pub_date = models.DateTimeField('Review Publishing Date')
	user_name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	academic_rate = models.IntegerField(choices=feedback, default='Other')
	placement_rate = models.IntegerField(choices=feedback, default='Other')
	infra_rate = models.IntegerField(choices=feedback, default='Other')
	rating = models.FloatField()


class PendingQuery(models.Model):
	college = models.ForeignKey(College,on_delete=models.CASCADE)
	qsn = models.CharField(max_length=10000)


class AnsweredQueries(models.Model):
	college = models.ForeignKey(College,on_delete=models.CASCADE)
	qsn = models.CharField(max_length=10000)
	ans = models.CharField(max_length=10000)


type_choices = (
    ('Active Student', 'Active Student'),
    ('Alumni', 'Alumni'),
)


class StudentUser(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	category = models.CharField(max_length=20, choices=type_choices,default='Other')
	college = models.ForeignKey(College,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username


class IndustryUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	company = models.CharField(max_length=1000)
