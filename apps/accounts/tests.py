from django.test import TestCase
from .models import CustomUser

# Create your tests here.


class PaymentUnitTest(TestCase):

    def test_has_paid(self):
        user = CustomUser.objects.create(username='roberto', phone='93949434')

        self.assertFalse(
            user.has_paid(),
            'Usuario inicial tiene un pago vacio'
        )

