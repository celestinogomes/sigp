from django.contrib import admin
from payment.models import Payment, PaymentHistory

admin.site.register(Payment)
admin.site.register(PaymentHistory)
