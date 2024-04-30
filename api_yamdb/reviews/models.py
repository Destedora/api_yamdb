from django.db import models


class Comment(models.Model):
    """Модель комментария к отзыву.

    Связывает автора комментария, отзыв, на который оставлен комментарий,
    текст комментария и дату добавления.
    """
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        """Определяет `related_name`, `verbose_name` и сортировку."""
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращает автора комментария и его текст."""
        return (
            f'Автор комментария: {self.author.username}. '
            f'id отзыва: {self.review.id}. '
            f'Комментарий: {self.text[:30]}'
        )
