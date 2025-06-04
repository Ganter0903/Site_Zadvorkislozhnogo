from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, default='', max_length=254, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    surname = models.CharField(max_length=150, verbose_name='Отчество', blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Баланс')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    subscriptions = models.ManyToManyField(
        'self',
        through='Subscription',
        symmetrical=False,
        related_name='subscribers',
        verbose_name='Подписки'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/static/Zadvorkislozhnogo/images/user.png"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

class Subscription(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='От кого')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='Кому')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        unique_together = ('from_user', 'to_user')


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')


class BaseContent(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    views_count = models.PositiveIntegerField(verbose_name='Кол-во просмотров', default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')

    class Meta:
        abstract = True


class Story(BaseContent):
    
    class Meta:
        verbose_name = "Рассказ"
        verbose_name_plural = "Рассказы"


class Poem(BaseContent):
    
    class Meta:
        verbose_name = "Стих"
        verbose_name_plural = "Стихи"


class Audiobook(BaseContent):
    audio_file = models.FileField(upload_to='audiobooks/', verbose_name='Аудиофайл')
    
    class Meta:
        verbose_name = "Аудиокнига"
        verbose_name_plural = "Аудиокниги"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE, verbose_name='Тип контента')
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')