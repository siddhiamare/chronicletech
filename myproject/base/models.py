from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    badge_color = models.CharField(max_length=30, default='blue', help_text="Color variant: blue, purple, emerald, amber")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    author = models.CharField(max_length=100, default='NextGen Editorial')
    short_desc = models.CharField(
        max_length=400,
        blank=True,
        help_text="Concise lead-in summary for cards and search snippets"
    )
    content = models.TextField()
    image_path = models.CharField(
        max_length=255,
        default='img/digital memory.jpg',
        help_text="Path under static/ (e.g. 'img/digital memory.jpg')"
    )
    read_time = models.PositiveIntegerField(
        default=4,
        help_text="Estimated reading time in minutes"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in hero / spotlight banner on homepage"
    )
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.short_desc and self.content:
            first_sentence = self.content.split('.')[0]
            self.short_desc = (first_sentence[:340] + '...') if len(first_sentence) > 340 else first_sentence

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('read', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count = models.F('views_count') + 1
        self.save(update_fields=['views_count'])

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    date_str = models.CharField(max_length=100, help_text="e.g. Jan 6-9, 2026")
    location = models.CharField(max_length=200, help_text="e.g. Las Vegas, USA")
    description = models.TextField()
    category_tag = models.CharField(max_length=60, default='Tech Summit')
    is_featured = models.BooleanField(default=False)
    external_link = models.URLField(blank=True, default='#')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.location})"
