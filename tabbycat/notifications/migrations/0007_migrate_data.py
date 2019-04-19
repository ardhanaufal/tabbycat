# Generated by Django 2.0.8 on 2018-10-23 19:44
# Extended manually to create BulkNotification objects and Message-IDs
import email
import itertools
import operator

from django.db import migrations


def create_bulk_notifications(apps, schema_editor):
    SentMessageRecord = apps.get_model("notifications", "SentMessageRecord")  # noqa: N806
    BulkNotification = apps.get_model("notifications", "BulkNotification")    # noqa: N806

    message_queryset = SentMessageRecord.objects.order_by('event', 'round', 'tournament', 'timestamp')
    key_getter = operator.attrgetter('event', 'round', 'tournament')

    for (event, r, t), group in itertools.groupby(message_queryset, key_getter):
        messages = list(group)
        notification = BulkNotification.objects.create(event=event,
                timestamp=messages[0].timestamp, round=r, tournament=t)
        notification_id = notification.id
        for m in messages:
            m.notification_id = notification_id
            m.save()


def get_message_ids(apps, schema_editor):
    SentMessageRecord = apps.get_model("notifications", "SentMessageRecord")  # noqa: N806

    for m in SentMessageRecord.objects.all():
        message = email.message_from_string(m.message)
        m.message_id = message.get('Message-ID')
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_separate_tables'),
    ]

    operations = [
        migrations.RunPython(create_bulk_notifications),
        migrations.RunPython(get_message_ids),
    ]