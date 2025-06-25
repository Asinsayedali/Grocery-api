from django.db import models

class Grocerydb(models.Model):
    userid = models.CharField(max_length=100)
    input = models.TextField()  
    output = models.JSONField()

    def __str__(self):
        return f"DataRecord {self.id} for {self.userid}"
