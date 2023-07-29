from django.urls import path
from .views import initiate_payment, payment_callback, make_charge_request

app_name = 'payment'

urlpatterns = [
    path('<int:course_id>/', initiate_payment, name='initiate-payment'),
    path('callback/', payment_callback, name='payment-callback'),
]