from django.db import models
from django.utils.text import slugify

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

class Gator(TrackingModel):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, default=None, blank=True, null=True)

    def unique_slugify(self, name):
        
        name = '-'.join(name.lower().split(' ')[:2])
        gators = Gator.objects.filter(slug=name)
        if len(gators) > 0:
            unique_slug = name + "-"+ str(len(gators)+1)
            return unique_slug.lower()
        else:
            return name.lower()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = self.unique_slugify(self.name)
        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        return self.name
        
class Response(TrackingModel):

    class Value(models.IntegerChoices):
        AWFUL = 1
        BAD = 2
        MEH = 3
        GOOD = 4
        EXCELLENT = 5
    
    value = models.IntegerField(choices=Value.choices)
    gator = models.ForeignKey(Gator, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value)

class Comment(TrackingModel):
    text = models.TextField(max_length=200)
    rating = models.ForeignKey(Response, on_delete=models.CASCADE)
    agree = models.IntegerField(default=0)
    disagree = models.IntegerField(default=0)
    abuse = models.IntegerField(default=0)

    def __str__(self):
        return self.rating.gator.name

