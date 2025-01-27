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

    def recent_posts(self, limit=None):
        """
        Сортирует по дате публикации в убывающем порядке.
        Ограничивает количество записей до значения limit
        """
        return self.published()[:limit]
