# Generated by Django 2.1.10 on 2019-07-19 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_content', '0002_auto_20190719_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ['container', 'parent_element', 'position'], 'verbose_name': 'Element', 'verbose_name_plural': 'Element'},
        ),
    ]
