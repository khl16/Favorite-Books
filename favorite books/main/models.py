from django.db import models
from datetime import datetime
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if len(postData['email']) == 0:
            errors['register_email'] = "You must enter an email"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['register_email'] = "Invalid email address"
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['register_email'] = "That email already exists"
        if len(postData['password']) < 8:
            errors['register_password'] = "Password should be at least 8 characters"
        elif (postData['password']) != (postData['confirm_password']):
            errors['register_password'] = "Passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])

        if len(existing_user) != 1:
            errors['login_email'] = "User does not exist"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['login_password'] = "Email and Password do not match"
        if len(postData['email']) == 0:
            errors['login_email'] = "Email must be entered"
        if len(postData['password']) < 8:
            errors['login_password'] = "Password should be at least 8 characters"
        return errors
        

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}

        if len(postData['title']) == 0:
            errors['title'] = "Title is required"
        if len(postData['description']) < 5:
            errors['description'] = "Description should be at least 5 characters"
        return errors

    def update_validator(self, postData):
        errors = {}

        if len(postData['description']) < 5:
            errors ['update_description'] = "Description should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
