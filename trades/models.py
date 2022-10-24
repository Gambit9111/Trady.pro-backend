# from django.db import models

# from user_profile.models import Account, Trading_System, Symbol

# ACTION_CHOICES = (
#     ('long', 'long'),
#     ('short', 'short'),
# )

# class Trade(models.Model):
#     # Trade information
#     account = models.ForeignKey(Account, related_name="trades", on_delete=models.CASCADE)
#     trading_system = models.ForeignKey(Trading_System, on_delete=models.CASCADE)
#     symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
#     action = models.CharField(choices=ACTION_CHOICES, max_length=10)
#     entry_date = models.DateTimeField()
#     entry_price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)
#     leverage = models.IntegerField()
#     stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     take_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     exit_date = models.DateTimeField(null=True, blank=True)
#     exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     pnl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     trace_closed = models.BooleanField(default=False)
#     trade_hit_tp = models.BooleanField(default=False)
#     trade_hit_sl = models.BooleanField(default=False)
#     trade_info = models.TextField(null=True, blank=True)


# class Note(models.Model):
#     # Note information
#     trade = models.ForeignKey(Trade, related_name="notes", on_delete=models.CASCADE)
#     note = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class Image(models.Model):
#     # Image information
#     trade = models.ForeignKey(Trade, related_name="images", on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/')
#     created_at = models.DateTimeField(auto_now_add=True)