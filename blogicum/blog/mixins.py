from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from blog.models import Comments, Post


class OnlyAuthorMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostUpdateDeleteMixin(OnlyAuthorMixin):

    def dispatch(self, request, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('blog:post_detail', pk=obj.pk)
        return super().dispatch(request, **kwargs)


class CommentsUpdateDeleteMixin(OnlyAuthorMixin):

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return get_object_or_404(
            Comments,
            id=self.kwargs['comment_id'],
            post=post
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.object.post.id}
        )
