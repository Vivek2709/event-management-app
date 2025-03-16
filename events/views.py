from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from .models import Event,Attendee
from .serializers import EventSerializer,AttendeeSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response


def home(request):
    return HttpResponse("Welcome to the Home Page!")


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #Filtering and Searching
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['event_date']

    def get_queryset(self):
        queryset = Event.objects.all()
        organizer = self.request.query_params.get('organizer') 
        event_date = self.request.query_params.get('event_date')
        if organizer:
            queryset = queryset.filter(organizer__username=organizer)
        if event_date:
            queryset = queryset.filter(event_date=event_date)
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Ensure event details include the list of attendees."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Include attendees in response
        attendees = Attendee.objects.filter(event=instance)
        data["attendees"] = AttendeeSerializer(attendees, many=True).data

        return Response(data)

class AtttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class =AttendeeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Attendee.objects.all()
        event_id = self.request.query_params.get('event') 
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset
    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        if not event_id:
            return Response({"error": "Event ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # ✅ Return success response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # ✅ Return validation errors status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Use the serializermission_classes
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Event
# from .serializers import EventSerializer

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def event_list(request):
#     if request.method == 'GET':
#         # Filtering and searching
#         queryset = Event.objects.all()
#         organizer = request.query_params.get('organizer')
#         event_date = request.query_params.get('event_date')
#         search = request.query_params.get('search')

#         if organizer:
#             queryset = queryset.filter(organizer__username=organizer)
#         if event_date:
#             queryset = queryset.filter(event_date=event_date)
#         if search:
#             queryset = queryset.filter(title__icontains=search)

#         serializer = EventSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def event_detail(request, id):
#     try:
#         event = Event.objects.get(id=id)
#     except Event.DoesNotExist:
#         return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = EventSerializer(event)
#         return Response(serializer.data)

#     elif request.method == 'PATCH':
#         serializer = EventSerializer(event, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         event.delete()
#         return Response({"message": "Event deleted"}, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def attendee_list(request):
#     if request.method == 'GET':
#         queryset = Attendee.objects.all()
#         event_id = request.query_params.get('event')
#         if event_id:
#             queryset = queryset.filter(event_id=event_id)

#         serializer = AttendeeSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = AttendeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def attendee_detail(request, id):
#     try:
#         attendee = Attendee.objects.get(id=id)
#     except Attendee.DoesNotExist:
#         return Response({"error": "Attendee not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = AttendeeSerializer(attendee)
#         return Response(serializer.data)

#     elif request.method == 'PATCH':
#         serializer = AttendeeSerializer(attendee, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         attendee.delete()
#         return Response({"message": "Attendee deleted"}, status=status.HTTP_204_NO_CONTENT)



