from django.db import models

# Create your models here.


class FoundItem(models.Model):
    # Basic fields matching your form (title, category)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)

    # Image
    image = models.ImageField(upload_to='found_items/')

    # AI-generated fields (from your JSON response)
    item_type = models.CharField(max_length=100, blank=True)
    primary_color = models.CharField(max_length=50, blank=True)
    secondary_colors = models.JSONField(blank=True, default=list)
    material = models.CharField(max_length=100, blank=True, null=True)
    distinguishing_features = models.JSONField(blank=True, default=list)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)

    # Basic metadata
    date_found = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title:${self.title}, category:${self.category}, item_type:${self.item_type}, primary_color:${self.primary_color}, secondary_colors:${self.secondary_colors}, material:${self.material}, distinguishing_features:${self.distinguishing_features}, brand:${self.brand}, description:${self.description}, date_found:${self.date_found}, image:${self.image}"