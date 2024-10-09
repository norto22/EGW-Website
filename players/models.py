from django.db import models
from django.utils import timezone

class Player(models.Model):
    discord_username = models.CharField(max_length=100)
    airlinesim_username = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    notes = models.TextField(blank=True)

    def calculate_amount_owed(self):
        total_cost_per_month = 360  # Cost per month is 360 euros
        total_players = Player.objects.count()  # Get total number of players
        if total_players > 0:
            return total_cost_per_month / total_players
        return 0

    def save(self, *args, **kwargs):
        # Calculate the amount owed each time a player is saved
        self.amount_owed = self.calculate_amount_owed()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.discord_username


class Airline(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hub = models.CharField(max_length=100)
    date_formed = models.DateField(null=True, blank=True)  # Date the airline was formed

    def __str__(self):
        return self.name


class Subsidiary(models.Model):
    parent_airline = models.ForeignKey(Airline, related_name='subsidiaries', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hub = models.CharField(max_length=100)
    date_formed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Subsidiary: {self.name} (Parent: {self.parent_airline.name})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES, default='credit')
    description = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Adjust player's balance based on transaction type
        if self.transaction_type == 'credit':
            self.player.balance += self.amount
        elif self.transaction_type == 'debit':
            self.player.balance -= self.amount
        
        if self.player.balance < 0:
            self.player.balance = 0
        
        self.player.save(update_fields=['balance'])

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} by {self.player.discord_username} on {self.payment_date}"
