from django.db import models
import datetime
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from authemail.models import EmailUserManager, EmailAbstractUser
# Create your models here.
class CustomAccountManager(EmailUserManager):
    def create_user(self, **other_fields):
        '''if not email:
            raise ValueError(_('Missing email'))
        email= self.normalize_email(email)
        user.set_password(password)'''
        user= self.model(**other_fields)
        user.save()
        return user

class RegisteredUser(EmailAbstractUser):
    occupation= models.TextField(max_length=20, default='Developer')
    img= models.ImageField(upload_to='../images')
    objects= CustomAccountManager()
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['first_name','last_name','password','occupation']

class Project(models.Model):
    #the tasks field will be handled by a two way many to one in Tasks model
    class DevelopmentModels(models.TextChoices):
        AGILE= 'AGL', _('AGILE')
        WATERFALL= 'WRF', _('WATERFALL')
        INCREMENTAL= 'INC', _('INCREMENTAL')
        RAD= 'RAD', _('RAD')
        ITERATIVE= 'ITR', _('ITR')
        SPIRAL= 'SPR', _('SPIRAL')
    sdm= models.CharField(max_length= 3, 
        choices= DevelopmentModels.choices,
        default= DevelopmentModels.INCREMENTAL,
    )
    name= models.CharField(max_length= 200, blank= True)
    manager= models.ForeignKey(RegisteredUser, on_delete= models.CASCADE)
    created= models.DateField(_("Date"), default=datetime.date.today)
    #the methods will be handled in views class bacause they are api end point
    
class Task(models.Model):
    url= models.CharField(max_length=200)
    project= models.ForeignKey(Project, on_delete= models.CASCADE, related_name='tasks')
    dev= models.ForeignKey(RegisteredUser, on_delete= models.CASCADE)
    instruction= models.CharField(max_length=500)
    class TaskStatus(models.TextChoices):
        COMPLETED= 'CMP', _('COMPLETED')
        SUBMITTED= 'SUB', _('SUBMITTED')
        PENDING= 'PEN', _('PENDING')
        DOING= 'DOI', _('DOING')
        REJECTED= 'REJ', _('REJECTED')
    status= models.CharField(
        max_length= 3, 
        choices= TaskStatus.choices,
        default= TaskStatus.PENDING,
    )
    due= models.DateField()
    assigned= models.DateField(_("Date"), default=datetime.date.today)

class Role(models.Model):
    user= models.ForeignKey(RegisteredUser, on_delete= models.CASCADE)
    class UserRole(models.TextChoices):
        DEVELOPER= 'DEV', _('DEVELOPER')
        MANAGER= 'MGR', _('MANAGER')
        NONE= 'NON', _('UNASSIGNED')
    role= models.TextField(max_length= 3, 
        choices= UserRole.choices,
        default= UserRole.NONE,
    )
    project= models.ForeignKey(Project, on_delete= models.CASCADE, related_name='projs')


