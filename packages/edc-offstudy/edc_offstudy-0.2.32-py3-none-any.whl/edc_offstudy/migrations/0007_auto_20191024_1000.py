# Generated by Django 2.2.6 on 2019-10-24 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("edc_offstudy", "0006_auto_20190922_0439")]

    operations = [
        migrations.AlterField(
            model_name="subjectoffstudy",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.Site",
            ),
        )
    ]
