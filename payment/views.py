from django.shortcuts import redirect
from django.urls import reverse_lazy
from teacher.models import Course, Enrollment
from .models import Payment
import requests
import hashlib
import base64
import json



# prod

BASE_URL = 'https://api-preprod.phonepe.com/apis/hermes'

merchant_id = "UNSTARTONLINE"
salt_key = "80815208-8c48-4c1e-be94-71c22dff882e"  

# pre prod

# BASE_URL = 'https://api-preprod.phonepe.com/apis/hermes'

# merchant_id = "PGTESTPAYUAT"
# salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
salt_index = 1 



CHARGE_ENDPOINT = "/pg/v1/pay" 




def make_base64(json_obj):
    json_str = json.dumps(json_obj, separators=(',', ':'))  # compact encoding
    return base64.urlsafe_b64encode(bytes(json_str, "utf-8")).decode("utf-8")


def make_hash(input_str):
    m = hashlib.sha256()
    m.update(input_str.encode())
    return m.hexdigest()


def make_request_body(base64_payload):
    request_body = {
        "request": base64_payload
    }
    data_json = json.dumps(request_body)
    return data_json


def make_charge_request(request, course_id):
    course = Course.objects.filter(id=course_id).first()

    amount = course.course_price * 100
    request_payload = {
        "merchantId": merchant_id,
        "merchantTransactionId": str(uuid.uuid4()),
        "merchantUserId": str(request.user.id),
        "amount": amount,
        "redirectUrl": str(s2s_callback_url),
        "redirectMode": "POST",
        "callbackUrl": str(s2s_callback_url),
        "mobileNumber": "7396272002",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }

    base64_payload = make_base64(request_payload)
    verification_str = base64_payload + \
        CHARGE_ENDPOINT + salt_key
    X_VERIFY = make_hash(verification_str) + "###" + str(salt_index)

    print(X_VERIFY)

    url = BASE_URL + CHARGE_ENDPOINT
    data = make_request_body(base64_payload)
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "X-VERIFY": X_VERIFY
    }
    print(data)

    response = requests.post(url, json=data, headers=headers)
    print(response.status_code, response.text)
    return None





import uuid  
from phonepe.sdk.pg.payments.models.request_v1.pg_pay_request import PgPayRequest  
from phonepe.sdk.pg.payments.payment_client import PhonePePaymentClient  
from phonepe.sdk.pg.env import Env

# insert your salt index 
env = Env.UAT # Change to Env.PROD when you go live

phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env, should_publish_events=True)

ui_redirect_url = ""  
s2s_callback_url = reverse_lazy('payment:payment-callback')


def initiate_payment(request, course_id):

    course = Course.objects.filter(id=course_id).first()

    merchant_transaction_id = str(uuid.uuid4())  
    amount = course.course_price * 100  # in paise  
    
    id_assigned_to_user_by_merchant = str(request.user.id)

    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
        merchant_transaction_id=merchant_transaction_id,  
        amount=amount,  
        merchant_user_id=id_assigned_to_user_by_merchant,  
        callback_url= str(s2s_callback_url),  
        redirect_url=ui_redirect_url
    )  
    
    pay_page_response = phonepe_client.pay(pay_page_request)  
    print(pay_page_response)

    # payment intiated
    # Payment.objects.create(
    #     student = request.user,
    #     course = course,
    #     merchant_transaction_id = merchant_transaction_id
    # )
    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url

    return redirect(pay_page_url)



def payment_callback(request, *args, **kwargs):




    # if verified as true
    merchant_transaction_id = '' #gets from response
 

    payment = Payment.objects.filter(merchant_transaction_id = merchant_transaction_id).first()
    payment.status = True
    payment.save(update_fields=['status'])

    # create enrollment for that student in that course

    Enrollment.objects.create(
        course=payment.course,
        student = payment.student
    )

    return None



 





