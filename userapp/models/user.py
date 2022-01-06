from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=400)
    password = models.CharField(max_length=8)

    def register(self):
        self.save()

    def isExists(self):
        if User.objects.filter(email=self.email):
            return True

        return False

    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False
    def get_user_info(user):
        return User.objects.get(pk = user)
