from django.conf import settings
from src.wall.models import Post


class Feed:
    """ Service feeds
    """
    def get_post_list(self, user: settings.AUTH_USER_MODEL):
        return Post.objects.filter(user=user.id).order_by('-create_date')\
                            .prefetch_related('comments')

    def get_single_post(self, pk: int):
        return Post.objects.prefetch_related('comments').get(id=pk)


feed_service = Feed()
