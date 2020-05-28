from django.contrib.auth.models import (BaseUserManager)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, active=True, staff=False, superuser=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_active=active
        user.is_staff=staff
        user.is_superuser=superuser
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
            """
            Creates and saves a staff user with the given email and password.
            """
            user = self.create_user(
                email,
                password=password,
            )
            user.is_staff = True
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user