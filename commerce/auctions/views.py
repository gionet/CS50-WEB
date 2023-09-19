from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Max, F, Func
from django.db.models.functions import Round
from decimal import Decimal
from django.contrib import messages

from .models import User, auction, comments, watchlist, bid, itemStatus
from .forms import CustomerForm

def index(request):
    open_listings = auction.objects.filter(itemStatus_item__item_status=True).order_by('-created')
    highest_bids = open_listings.annotate(max_bid=Max('bid_items__bidding'))
    
    combined_data = zip(open_listings, highest_bids)
    
    item_list_details = []
    for auctions, highest_bids in combined_data:
        item_details = {
        'id': auctions.id,
        'item': auctions.item,
        'max_bid': highest_bids.max_bid,
        'price': auctions.starting_bid,
        'created': auctions.created,
        'image': auctions.image,
        'description': auctions.description,
        'category': auctions.category,
        'open_listing': auctions
    }
        item_list_details.append(item_details)
        
    return render(request, "auctions/index.html", {
        "auctions": item_list_details
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    form = CustomerForm() 
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                new_auction = form.save(commit=False)
                new_auction.user = request.user
                new_auction.save()
                
                item_status = itemStatus.objects.create(item_status=True, item=new_auction, user=request.user)
                item_status.save()
                
            except Exception as debug:
                print(debug)
        
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "GET":
        return render(request, 'auctions/create.html', {
            'form': form
        })
        
def items(request, auction_id):
    if request.method == "GET":
        items = auction.objects.get(pk=auction_id)
        comment = comments.objects.filter(auction=items)
        highest_bid = bid.objects.filter(item=items).order_by('-bidding').first()
        total_bids = bid.objects.filter(item=items).count()
        item_listing_status = itemStatus.objects.get(item=items)
        #Watchlist Status
        
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # User is logged in, check the watchlist status
            try:
                watchlist_status = watchlist.objects.get(item=items, user=request.user)
                watchlist_status = True         
            except watchlist.DoesNotExist:
                watchlist_status = False
            
            try:
                item_status = itemStatus.objects.get(item=items, user=request.user)   
            except itemStatus.DoesNotExist:
                item_status = False
            
            if item_listing_status.item_status == False:

                if highest_bid is not None:
                    if highest_bid.user == request.user:
                        messages.success(request, "Congratulations, you have won the bid!", extra_tags='success')                   
                    else:
                        messages.error(request, "Auction has ended. Thank you for showing interest, do check out other auction items!", extra_tags='danger')
                else:
                    messages.success(request, "1Auction has ended. Thank you for showing interest, do check out other auction items!", extra_tags='success')
            
        else:
            # User is anonymous, set watchlist_status to False
            watchlist_status = False
            item_status = False

        return render(request, "auctions/items.html", {
            "auction": items,
            "comments": comment,
            "watchlist_status": watchlist_status,
            "bidding": highest_bid,
            "total_bids": total_bids,
            "item_status": item_status,
            "item_listing_status": item_listing_status.item_status,
        })
        
def comment(request, auction_id):
    if request.method == "POST":
            comment = request.POST["comment"]
            auction_obj = auction.objects.get(pk=auction_id)
            comments.objects.create(comments=comment, auction=auction_obj, user=request.user)
    return redirect("items", auction_id=auction_id)

@login_required
def watchlist_func(request, auction_id):  
    if request.method == "POST":    
        add_watchlist = request.POST.get("addwatchlist")
        del_watchlist = request.POST.get("delwatchlist")
        
        if add_watchlist:
            # If 'addwatchlist' button was pressed
            watchlist_obj, created = watchlist.objects.get_or_create(item_id=auction_id, user=request.user)
            watchlist_obj.watchlist = True
            watchlist_obj.save()
        elif del_watchlist:
            # If 'delwatchlist' button was pressed
            try:
                watchlist_obj = watchlist.objects.get(item_id=auction_id, user=request.user)
                watchlist_obj.delete()
            except watchlist.DoesNotExist:
                pass 
        
        return HttpResponseRedirect(reverse("items", args=[auction_id]))
    
@login_required
def watchlistList(request):
    watchlists = watchlist.objects.filter(user=request.user)
    auctions = auction.objects.filter(id__in=watchlists.values_list('item_id', flat=True))
    open_listings = auction.objects.filter(itemStatus_item__item_status=True)
    print(open_listings)
    if request.method == "GET":
        
        highest_bids = auctions.annotate(max_bid=Max('bid_items__bidding'))
        
        combined_data = zip(auctions, highest_bids)

        item_list_details = []
        for auctions, highest_bids in combined_data:
            item_details = {
            'id': auctions.id,
            'item': auctions.item,
            'max_bid': highest_bids.max_bid,
            'price': auctions.starting_bid,
            'created': auctions.created,
            'image': auctions.image,
        }
            item_list_details.append(item_details)
        return render(request, "auctions/watchlist.html", {
        "auctions": item_list_details,
        "watchlists": watchlists
    
        })
    
    
@login_required
def bidding(request, auction_id):
    if request.method == "POST":
        add_bidding = request.POST.get("bidding")

        # Check if the bidding amount is higher than the current bid amount
        highest_bid = bid.objects.filter(item_id=auction_id).aggregate(max_bid=Max('bidding'))
        highest_bid_value = highest_bid.get('max_bid')
        starting_bid = Decimal(auction.objects.get(pk=auction_id).starting_bid)
        
        if highest_bid_value is None:    
            current_price = starting_bid
        else:
            current_price = highest_bid_value
        
        if add_bidding:
            # Create a new bid
            if Decimal(add_bidding) > Decimal(current_price):
                bid.objects.create(bidding=add_bidding, item_id=auction_id, user=request.user)
                messages.success(request, "Your bid has been placed successfully.", extra_tags='success')
                return redirect('items', auction_id=auction_id)
                
            else:
                messages.error(request, "Error: Your bid must be higher than the current price.", extra_tags='danger')
                return HttpResponseRedirect(reverse("items", args=[auction_id]))

        else:
            messages.error(request, "Error: No bidding amount has been entered.", extra_tags='danger')
            return redirect('items', auction_id=auction_id)

        
@login_required
def closeListing(request, auction_id):
    if request.method == "POST":
        items = auction.objects.get(pk=auction_id)
        remove_watchlist_item = watchlist.objects.filter(item=items, watchlist=True)
        print(remove_watchlist_item)
        closeListing = request.POST.get('closeListing')
        
        if closeListing:
            try:
                item_status = itemStatus.objects.get(item=items, user=request.user)      
                item_status.item_status = False
                item_status.save()
                
                remove_watchlist_item.delete()            
                 
            except itemStatus.DoesNotExist:
                return HttpResponseRedirect(reverse("items", args=[auction_id]))
            
        return HttpResponseRedirect(reverse("items", args=[auction_id]))
    
def categorylist(request):
    if request.method == "GET":
        category_names_all = [(category_code, category_name) for category_code, category_name in auction.ITEM_CATEGORIES]
        return render(request, "auctions/categorylist.html", {
        "categories": category_names_all,
        })
        
def category(request, category_itemlist):
    if request.method == "GET":
        category_code = next((code for code, name in auction.ITEM_CATEGORIES if name == category_itemlist), None)

        category = auction.objects.filter(category=category_code, itemStatus_item__item_status=True).order_by('-created')
        
        if category.exists():
            highest_bids = category.annotate(max_bid=Max('bid_items__bidding'))
            combined_data = zip(category, highest_bids)

            item_list_details = []
            for category, highest_bids in combined_data:
                item_details = {
                'id': category.id,
                'item': category.item,
                'max_bid': highest_bids.max_bid,
                'price': category.starting_bid,
                'created': category.created,
                'image': category.image,
            }
                item_list_details.append(item_details)
            
        else:
            item_list_details = None
    
        return render(request, "auctions/category_itemlist.html", {
            "auctions": item_list_details,
            "category_itemlist": category_itemlist
        })
        