# Generated by Django 4.2.3 on 2023-08-07 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid_delete_bids_auction_user_alter_comments_auction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='itemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_status', models.BooleanField(default=True)),
                ('closed', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemStatus_item', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemStatus_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
