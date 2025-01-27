from django.db import models
from django.utils import timezone


class PublishedPostsQuerySet(models.QuerySet):
    def published(self):
        """
        Фильтрует опубликованные посты, относящиеся к опуликованным
        категориям до текущего времени
        """
        return self.select_related("category", "location", "author").filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return PublishedPostsQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
