"""
Tests.
"""
import os ; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza_shop.settings")
import django ; django.setup()


from .models import Customer, Pizza



class TestOrder:
    """
    Class that contain all tests.
    """

    def setup_method(self):
        """
        Init attributes for the tests.
        :return:
        """
        self.customer = Customer.objects.get(username='usertest')
        self.customer.save()

    def test_ordering_pizza(self):
        """
        Test the pizza's ordering.
        :return:
        """
        pizza = Pizza.objects.filter(type='Salami').first()
        new_order = self.customer.order_pizza(**{'type': pizza.type, 'size': 'Large'})
        assert new_order is not None

    def test_get_order(self):
        """
        Test the order's displaying.
        :return:
        """
        assert len(self.customer.get_orders()) > 0 #all orders
        assert len(self.customer.get_orders(mine=True)) > 0 #order's usertest
        assert len(self.customer.get_orders(mine=False, filter_orders={
            "criteria": 'email',
            "key_word": 'test@gmail.com'
        })) > 0 #orders filtered

    def test_delete_order(self):
        """
        test the deleting of orders.
        :return:
        """
        self.customer.clean_orders()
        assert len(self.customer.get_orders(mine=True)) == 0
