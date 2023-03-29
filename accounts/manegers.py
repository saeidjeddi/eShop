from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def creat_user(self, phone_number, username, email, password, full_name):
        if not phone_number:
            raise ValueError('user mast have phone number')
        if not email:
            raise ValueError('user mast have email ')
        if not full_name:
            raise ValueError('user mast have  full name')

        user = self.model(phone_number=phone_number, username=username, email=self.normalize_email(email), full_name=full_name)
        if password:
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, phone_number, username, email, password, full_name):
        user = self.creat_user(phone_number, username, email, password, full_name)
        user.is_admin = True
        user.save(using=self._db)
        return user
