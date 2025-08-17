from django.urls import path, include
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, initiate_payment, verify_payment
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path("initiate-payment/", initiate_payment, name="initiate-payment"),
    path("verify-payment/", verify_payment, name="verify-payment")
]