# Generated by Django 2.1.1 on 2018-09-15 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False, verbose_name='Twitter User Active')),
                ('verified', models.BooleanField(default=False, verbose_name='Twitter User Verified')),
                ('username', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Twitter Username')),
                ('user_id', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Twitter User Id')),
                ('password', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Twitter Password')),
                ('email', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Twitter Email')),
                ('phone_number', models.CharField(blank=True, default=None, max_length=2000, null=True, verbose_name='Twitter Phone Number')),
                ('hashtags', models.CharField(blank=True, default=None, max_length=3000, null=True, verbose_name='Twitter Hashtags')),
                ('follow_accounts', models.CharField(blank=True, default=None, max_length=3000, null=True, verbose_name='Twitter Accounts to Follow')),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.BigIntegerField(default=0, verbose_name='Twitter User Followers')),
                ('followings', models.BigIntegerField(default=0, verbose_name='Twitter User Followings')),
                ('likes', models.BigIntegerField(default=0, verbose_name='Twitter User Likes')),
                ('tweets', models.BigIntegerField(default=0, verbose_name='Twitter User Tweets')),
                ('updated_timestamp', models.DateTimeField(auto_now=True, null=True, verbose_name='Stat Last Updated On')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Stat Saved On')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twengage.Account')),
            ],
        ),
    ]
