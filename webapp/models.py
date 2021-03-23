from django.db import models
from datetime import datetime
from django.utils import timezone

class Notification(models.Model):
	notif_title = models.CharField(max_length=50)
	notif_date = models.DateField(default = datetime.now)
	notif_content = models.CharField(max_length=250)
	notif_type = models.CharField(max_length=50)

	class Meta:
		db_table = "notification"

class Review(models.Model):
	title = models.CharField(max_length=50)
	content = models.CharField(max_length=255)
	rating = models.FloatField(default = 0)
	date_created = models.DateField(default = datetime.now)

	class Meta:
		db_table = "review"

class User(models.Model):
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=50)
	register_date = models.DateField(default = datetime.now)
	status = models.BooleanField(default = True)
	notification = models.ManyToManyField(Notification)

	class Meta:
		db_table="user"

class Request(models.Model):
	description = models.CharField(max_length=255)
	date_sent = models.DateField(default = datetime.now)
	time_sent = models.TimeField(default = timezone.now)
	request_type = models.CharField(max_length=50)
	isPending = models.BooleanField(default = True)
	isConfirmed = models.BooleanField(default = False)
	isDeleted = models.BooleanField(default = False)
	sender = models.ForeignKey(User, null = False, default = 1, blank = False, on_delete = models.CASCADE)

	class Meta:
		db_table = "request"

class Organizer(models.Model):
	organizer = models.ForeignKey(User, default = 1, null = False, blank = False, on_delete = models.CASCADE)
	request = models.ManyToManyField(Request)

	class Meta:
		db_table="organizer"

class Event(models.Model):
	event_organizer = models.ForeignKey(Organizer, null = False, default = 1, blank = False, on_delete = models.CASCADE)
	event_name = models.CharField(max_length=50)
	event_description = models.CharField(max_length=50)
	event_type = models.CharField(max_length=50)
	event_fee = models.FloatField(default = 0)
	number_of_reviews = models.IntegerField(default = 0)
	number_of_participants = models.IntegerField(default = 0)
	number_of_upvotes = models.IntegerField(default = 0)
	start_date = models.DateField(default = datetime.now)
	end_date = models.DateField(default = datetime.now)
	start_time = models.TimeField(default = timezone.now)
	end_time = models.TimeField(default = timezone.now)
	reviews = models.ManyToManyField(Review)
	participants = models.ManyToManyField(User)

	class Meta:
		db_table = "event"

class Administrator(models.Model):
	admin = models.ForeignKey(User, default = 1, null = False, blank = False, on_delete = models.CASCADE)

	class Meta:
		db_table = "administrator"