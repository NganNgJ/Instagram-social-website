# Generated by Django 3.1 on 2023-09-11 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_api', '0006_auto_20230909_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='web_api.post'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_reacts', to='web_api.post'),
        ),
        migrations.AlterField(
            model_name='share',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_shares', to='web_api.post'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='file_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
