from django.contrib import admin

from .models import auction, comments, watchlist, bid, itemStatus

# Register your models here.
admin.site.register(auction)
admin.site.register(comments)
admin.site.register(watchlist)
admin.site.register(bid)
admin.site.register(itemStatus)