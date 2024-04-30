from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Модель отзыва к произведению.

    Связывает отзыв с произведением, автором ,текстом, оценкой
    и датой публикации отзыва.
    """

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        """Определяет `related_name`, `verbose_name`."""
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        """Возвращает автора отзыва, рейтинг и текст отзыва."""
        return (
            f'Произведение: {self.title} .'
            f'Оценка произведения: {self.score}. '
            f'Отзыв: {self.text[:30]}'
            f'Автор отзыва: {self.author.username}. '
        )
