# Generated by Django 4.2.3 on 2023-07-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_bids_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='price',
            new_name='starting_bid',
        ),
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('CNCE', 'Consumer Electronics'), ('ANA', 'Apparel and Accessories'), ('FNHF', 'Furniture and Home Furnishings'), ('HNB', 'Health and Beauty'), ('ANP', 'Auto and Parts'), ('FNB', 'Food and Beverage'), ('TNH', 'Toys and Hobby'), ('BMV', 'Books/Music/Video'), ('PP', 'Pet products'), ('OTH', 'Other')], default='OTH', max_length=10),
        ),
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
