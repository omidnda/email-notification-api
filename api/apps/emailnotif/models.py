from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
#========================================================

class CustomUserManager(BaseUserManager): 
    def create_user(self, email, name="", family="",password=None,):
        if not email:
            raise ValueError("Email is required")
        user= self.model(
            email = self.normalize_email(email),
            name=name,
            family=family,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,email, name, family,password=None,):
        user=self.create_user(
            email=email,
            name=name,
            family=family,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

# =====================================================================

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True, max_length=200,)
    name = models.CharField(max_length=20,blank=True,null=True)
    family = models.CharField(max_length=20,blank=True,null=True)
    register_date = models.DateTimeField(default=timezone.now,)
    active_code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False,)
    is_admin = models.BooleanField(default=False, )
    subscribed_newletter = models.BooleanField(default=False, blank=True, null=True)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile_number", "name", "family"]
    objects = CustomUserManager()
    def __str__(self) -> str:
        return  f"{self.name} {self.family} {self.email}"

    @property
    def is_staff(self):
        return self.is_admin
#========================================================
class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    register_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject}"