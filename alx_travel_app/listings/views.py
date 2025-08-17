from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .models import Listing, Booking, Review
from rest_framework import permissions

# Create your views here.
class ListingViewSet(ModelViewSet):
    """view for the Listing model"""
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Listing.objects.all()


class BookingViewSet(ModelViewSet):
    """view for the Booking model"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()


class ReviewViewSet(ModelViewSet):
    """view for the Review model"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

