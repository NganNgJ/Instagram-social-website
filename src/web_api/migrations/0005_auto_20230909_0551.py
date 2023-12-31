# Generated by Django 3.1 on 2023-09-09 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_api', '0004_auto_20230909_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=None)),
                ('updated_at', models.DateTimeField(default=None)),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_files', to='web_api.uploadfile')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_files', to='web_api.post')),
            ],
            options={
                'db_table': 'posts_files',
            },
        ),
    ]
