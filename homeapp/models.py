from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)

    class Meta:

        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('prod_cat', args=[self.slug])


    def __str__(self):
        return '{}'.format(self.name)

class product(models.Model):
    name=models.CharField(max_length=100,unique=True)
    img=models.ImageField(upload_to='picture')
    desc=models.TextField()
    price=models.IntegerField()
    slug=models.SlugField(max_length=100,unique=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    stock=models.IntegerField()
    available = models.BooleanField(default=True)
    

    def get_url(self):
        return reverse('details', args=[self.category.slug,self.slug])

    def __str__(self):
        return self.name