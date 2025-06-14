# Generated by Django 5.2.1 on 2025-06-14 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='MessageHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_content', models.TextField()),
                ('edited_at', models.DateTimeField(auto_now_add=True)),
                ('edited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='messaging.message')),
            ],
            options={
                'verbose_name_plural': 'Message Histories',
                'ordering': ['-edited_at'],
            },
        ),
    ]
