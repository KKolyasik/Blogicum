from django.db import models
from django.contrib.auth import get_user_model
from blog.querysets import PublishedPostsQuerySet

TITLE_MAX_LENGTH = 256


class TimeStampedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено")

    class Meta:
        abstract = True


User = get_user_model()


class Category(TimeStampedModel):
    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL; "
        "разрешены символы латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)

    def __str__(self):
        return self.title


class Location(TimeStampedModel):
    name = models.CharField(max_length=TITLE_MAX_LENGTH,
                            verbose_name="Название места",
                            blank=True)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name='author'
    )
    location = models.ForeignKey(
        Location, null=True, on_delete=models.SET_NULL,
        verbose_name="Местоположение"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="posts"
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        blank=True,
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — можно делать "
        "отложенные публикации.",
    )

    objects: PublishedPostsQuerySet = PublishedPostsQuerySet.as_manager()

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class Comments(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-created_at',)
