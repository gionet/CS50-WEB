from .models import watchlist

def watchlist_count(request):
    if request.user.is_authenticated:
        count = watchlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'watchlist_count': count}