from django.db import models
from django.utils import timezone
from django.db.models import Count


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

    def annotate_comments(self):
        """
        Добавлят аннотацию комментариев к нужной выборке и
        сортирует их по дате добовления
        """
        return self.annotate(
            comment_count=Count('comments')).order_by('-pub_date')
