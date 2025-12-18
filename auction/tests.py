from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from .models import Item


class AuctionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="teszt123")

        self.item = Item.objects.create(
            name="Teszt festmény",
            category="festmény",
            starting_price=Decimal("10000"),
            auction_time=timezone.now(),
        )

    def test_items_page_loads(self):
        """A tárgyakat listázó oldal betöltődik."""
        url = reverse("items")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aukcióra meghirdetett műtárgyak")

    def test_bid_requires_login(self):
        """Nem bejelentkezett felhasználó nem tud licitálni (átirányítás loginra)."""
        self.item.is_active = True
        self.item.current_price = self.item.starting_price
        self.item.save()

        url = reverse("bid", args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_valid_bid_updates_price_and_winner(self):
        """Érvényes licit frissíti az árat és beállítja a nyertest."""
        self.item.is_active = True
        self.item.current_price = self.item.starting_price
        self.item.save()

        self.client.login(username="user1", password="teszt123")

        url = reverse("bid", args=[self.item.id])
        response = self.client.post(url, {"amount": "15000"})
        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()
        self.assertEqual(self.item.current_price, Decimal("15000"))
        self.assertEqual(self.item.winner, self.user)
