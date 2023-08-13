from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        """Мы переопределили этот метод, чтобы сформировать QuerySet
        фильтрующий посты по их статусу PUBLISHED"""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Модель данных для постов блога."""

    objects = models.Manager()  # менеджер применяемый по умолчанию
    # Наш менеджер (класс с переопределенным методом с фильтрацией).
    published = PublishedManager()

    class Status(models.TextChoices):
        """
        Класс для статуса опубликованного/черновичного поста.
        """
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=250)  # Заголовок поста.
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')  # Короткое слаг-поле.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()  # Тело поста.
    publish = models.DateTimeField(
        default=timezone.now  # timezone.now == datetime.now
    )  # Дата добавления поста.
    created = models.DateTimeField(
        # Дата будет сохраняться автоматически во время создания объекта.
        auto_now_add=True
    )  # Дата создания.
    updated = models.DateTimeField(
        # Дата будет обновляться автоматически во время сохранения объекта.
        auto_now=True
    )  # Дата обновления.
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        """
        Метаданные модели.

        По умолчанию посты будут возвращаться в обратном хронологическом порядке,
        если в запросе не указан иной порядок.

        Также здесь определен индекс БД по полю publish. Индекс повысит
        производительность запросов.
        """
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        """Возвращает заголовок поста в формате str."""
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug,
                       ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self) -> str:
        return f'Комментарий от {self.name} в {self.post}'
