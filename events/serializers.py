from rest_framework import serializers
from .models import Event,Attendee
from django.utils.timezone import now
from django.contrib.auth.models import User
import re

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    
    #custom validations
    def validate_event_date(self,value):
        if value < now():
            raise serializers.ValidationError("Event Date can not be in the past.")
        return value
    
    def validate_title(slef,value):
        if len(value) < 5 or len(value) > 100:
            raise serializers.ValidationError("Title must be between 5 aqnd 100 characters")
        return value
    
    def validate_location(self,value):
        if len(value) < 5:
            raise serializers.ValidationError("Location must be at least 5 character long.")
        return value
    
    # restricting editing to the organizer
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user != instance.organizer:
            raise serializers.ValidationError("Only the event Organizer can edit this event")
        return super().update(instance, validated_data)

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'

    #validate Name length
    def validate_name(self,value):
        if len(value) < 3 or len(value) > 5:
            raise serializers.ValidationError("Name Must be betweent 3 and 50 characters")
        return value
    #validate Email
    def validate_email(self,value):
        event_id = self.initial_data.get('event')
        if Attendee.objects.filter(event_id = event_id, email=value).exists():
            raise serializers.ValidationError("This Email is Already registered for this Event.")
        return value
    #validateing the contact number
    def validate_contact_number(self,value):
        if not re.match(r'^\d{10}$',value):
            raise serializers.ValidationError("Contact Number must be exactly 10 digists.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]