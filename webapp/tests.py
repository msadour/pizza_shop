from django.test import TestCase
from .models import Customer, Pizza

# Create your tests here.
class TestOrder(TestCase):
    """
    Class that contain all tests.
    """

    def setUp(self):
        self.customer = Customer(username='usertest', name='test', email='test@gmail.com', telephone='015555555')

    def test_ordering_pizza(self):
        pizza = Pizza.objects.get(type='Salami')
        size = 'Large'
        new_order = self.customer.order_pizza(**{'pizza': pizza, 'size': size})
        assert new_order is not None

    def test_geting_order(self):
        assert len(self.customer.get_orders()) > 0 #all orders
        assert len(self.customer.get_orders(mine=True)) > 0 #order's usertest
        assert len(self.customer.get_orders(mine=False, filter={"email": 'test@gmail.com'})) > 0 #orders filtered
        assert len(self.customer.get_orders(mine=True, filter={"email": 'test@gmail.com'})) == 0