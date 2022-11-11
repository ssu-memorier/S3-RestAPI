# Generated by Django 3.2 on 2022-11-11 02:11

from django.db import migrations, models

'''
#   모델을 적용할때 사용하는 init 파일입니다.
#   배포 진행후 해당 부분 추가 수정 진행하겠습니다
'''


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=64)),
                ('dir', models.CharField(blank=True, max_length=200)),
                ('key', models.CharField(max_length=100)),
            ],
        ),
    ]
