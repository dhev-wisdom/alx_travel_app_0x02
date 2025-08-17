from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .models import Listing, Booking, Review, Payment
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

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


@api_view(["POST"])
def initiate_payment(request):
    amount = request.data.get('amount')
    email = request.data.get('email')
    booking_id = request.data.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id)

    payment = Payment.objects.create(payer=request.user, amount=amount, booking=booking)

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "amount": str(amount),
        "currency": "USD",
        "email": email,
        "tx_ref": payment.booking_reference,
        "callback_url": "http://127.0.0.1:8000/api/verify-payment/",
    }

    response = requests.post(f"{settings.CHAPA_BASE_URL}/initialize", json=data, headers=headers)
    res_data = response.json()

    if res_data.get("status") == "success":
        payment.transaction_id = res_data["data"]["tx_ref"]
        payment.save()
        return Response({"checkout_url": res_data["data"]["checkout_url"]})
    
    return Response(res_data, status=400)

@api_view(["GET"])
def verify_payment(request):
    tx_ref = request.query_params.get("tx_ref")

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.get(f"{settings.CHAPA_BASE_URL}/verify/{tx_ref}", headers=headers)
    res_data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
    
    if res_data.get("status") == "success" and res_data["data"]["status"] == "success":
        payment.payment_status = "completed"
        payment.save()
        return Response({"message": "Payment verified successfully"})
    else:
        payment.payment_status = "failed"
        payment.save()
        return Response({"message": "Payment failed"}, status=400)