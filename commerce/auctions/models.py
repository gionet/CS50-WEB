from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class auction(models.Model):
    item = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_user")
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(max_length=200, null = True)
    
    CNCE = 'CNCE'
    ANA = 'ANA'
    FNHF = 'FNHF'
    HNB = 'HNB'
    ANP = 'ANP'
    FNB = 'FNB'
    TNH = 'TNH'
    BMV = 'BMV'
    PP = 'PP'
    OTH = 'OTH'
    ITEM_CATEGORIES = [
        (CNCE, "Consumer Electronics"),
        (ANA, "Apparel and Accessories"),
        (FNHF, "Furniture and Home Furnishings"),
        (HNB, "Health and Beauty"),
        (ANP, "Auto and Parts"),
        (FNB, "Food and Beverage"),
        (TNH, "Toys and Hobby"),
        (BMV, "Books-Music-Video"),
        (PP, "Pet products"),
        (OTH, "Other")
    ]
    category = models.CharField(max_length=10, choices=ITEM_CATEGORIES, default=OTH)
    
    def __str__(self):
        return f'{self.id}: {self.item}'
    
class comments(models.Model):
    comments = models.CharField(max_length=255, null=True)
    auction = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="comments_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    data_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}: {self.comments}"
    
class watchlist(models.Model):
    watchlist = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    item = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="watchlist_items")
    
    def __str__(self):
        return f"{self.item}: {self.watchlist}: {self.user}" 
    
class bid(models.Model):
    bidding = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="bid_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    
    def __str__(self):
        return f"{self.item}: {self.bidding} : {self.user}"
    
class itemStatus(models.Model):
    item_status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itemStatus_user")
    item = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="itemStatus_item")
    closed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.item}: {self.item_status}"