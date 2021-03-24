from django import forms
from .models import *

#Create forms here

class RegistrationForm(forms.ModelForm):

   class Meta:
        model = User
        fields = ('first_name','middle_name','last_name','username','email','password')

class RequestForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ('description','request_type')

class AdministratorForm(forms.ModelForm):

        class Meta:
                model = Administrator
                fields = ('admin',)

class EventCreationForm(forms.ModelForm):

        class Meta:
                model = Event
                fields = ('event_name', 'event_description', 'event_type', 'start_date', 'end_date',
                'start_time', 'end_time')

class ReviewCreationForm(forms.ModelForm):

        class Meta:
                model = Review
                fields = ('title', 'content', 'rating')