# Generated by Django 2.0.2 on 2018-03-17 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_ticket_ticketoffer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='show_id',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='ticketoffer',
            name='offer_id',
        ),
        migrations.RemoveField(
            model_name='ticketoffer',
            name='ticket_id',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.DeleteModel(
            name='TicketOffer',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
