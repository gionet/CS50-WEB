# Generated by Django 4.2.3 on 2023-08-01 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_price_auction_starting_bid_auction_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='auction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.auction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='comments',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='data_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
