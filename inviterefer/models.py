from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

role_list = ( ('FOUNDERS', 'Founders'), ('ADMIN', 'Admin') ,
			('MENTORS', 'Mentors') , ('ADVISORS', 'Advisors'), 
			('EMPLOYEE', 'Employee'), ('NORMALUSER', 'Normal Users'))

orgs = (('STARTUP', 'Startup'), ('INCUBATOR' ,'Incubator'),
			('ACCELERATOR' , 'Accelerator'))

class Organisation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    typeof = models.CharField(choices=orgs,
								default='STARTUP',max_length=10)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.name


class ExtendedUser(models.Model):
	user = models.OneToOneField(User)
	organisation = models.ForeignKey(Organisation)
	role = models.CharField(choices=role_list,
								default='NORMALUSER',max_length=15)
	refercode = models.CharField(max_length=10)
	referby = models.CharField(max_length=100, blank=True)

class Invite(models.Model):
	user = models.ForeignKey(User)
	owner = models.ForeignKey('auth.User', related_name='invites')
	postoffered = models.CharField(choices=role_list,
										default='NORMALUSER',max_length=15)
	company = models.ForeignKey(Organisation)
	accept = models.BooleanField(default=False)

class InviteNew(models.Model):
	emailid = models.EmailField(max_length=254)
	owner = models.ForeignKey('auth.User', related_name='offeredby')
	postoffered = models.CharField(choices=role_list,
										default='NORMALUSER',max_length=15)
	company = models.ForeignKey(Organisation)


class Refer(models.Model):
	user = models.ForeignKey(User)
	emailid = models.EmailField(max_length=254)