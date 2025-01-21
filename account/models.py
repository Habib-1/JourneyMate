from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

# Manager of Custom User Model
class MyAccountManager(BaseUserManager):
    # create normal user
    def create_user(self,username,first_name,last_name,email,phone_number,password=None):
        if not email:
            raise ValueError("Email address is required")
        if not username:
            raise ValueError("Username is required")
        
        user=self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Create SuperUser
    def create_superuser(self,username,first_name,last_name,email,phone_number,password=None):
        user=self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            password=password,

        )
        user.is_active=True
        user.is_staff=True
        user.is_admin=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

# Custom User Model
class Account(AbstractBaseUser):
    username=models.CharField(max_length=30,unique=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=21,blank=True)

    # required field for any User Model
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True) #pore email verifiaction add kore eta false kore dibo
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number',]
   
    objects=MyAccountManager()
    
    def __str__(self):
        return self.email
    
    # two mandatory method for use CustomUserModel
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    