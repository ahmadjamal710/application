from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    """Simple User model matching the required database schema"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        
    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        """Check if provided password matches stored password"""
        return check_password(raw_password, self.password)
        
    def __str__(self):
        return self.username
