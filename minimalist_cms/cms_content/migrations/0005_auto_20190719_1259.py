# Generated by Django 2.1.10 on 2019-07-19 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_content', '0004_auto_20190719_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='container',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms_content.Container', verbose_name='Container'),
        ),
        migrations.AlterField(
            model_name='element',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='Content type'),
        ),
        migrations.AlterField(
            model_name='element',
            name='parent_element',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='element_set', to='cms_content.Element', verbose_name='Parent element'),
        ),
    ]
