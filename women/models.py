from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# ham nay de tu dong them slug bang tieng Nga
def traslit_to_eng(s:str) -> str:
	d={'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'ie','ж':'zh','з':'z','и':'i','й':'i',
	   'к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u',
	   'ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'','ы':'ui','ъ':'','э':'e',
	   'ю':'iu','я':'ia'}
	return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d",blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Загалок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug')
    photo = models.ImageField(upload_to="photo/%Y/%m/%d", default=None,
                              blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name='контент')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    husband = models.OneToOneField('Husband',on_delete=models.SET_NULL, blank=True,null=True,related_name='wife', verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    def __str__(self):
        return self.title

    # de khong xu ly theo kieu link lien ket nua ma theo kieu lay duong dan tuyet doi
    def get_absolute_url(self):
        return reverse('post',kwargs={'post_slug':self.slug})

    #de tu dong tao slug tron trang chinh sua
    # def save(self,*args,**kwargs):
    #     #self.slug=slugify(traslit_to_eng(self.title))  #de tao slug tu tieu de tieng nga
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        # verbose_name="dan ba"
        # verbose_name_plural="dan_bas"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

class Husband(models.Model):
    objects = None
    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField(null=True, db_index=True)
    n_count = models.IntegerField(blank=True,default=0) # so lan ket hon Количество женитьбу

    def __str__(self):
        return self.name

class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category',kwargs={'cat_slug':self.slug}) # обратите внимание 'category' является маршрут url

    class Meta:
        # verbose_name = "The loai"
        # verbose_name_plural = "The loai"
        pass
class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag',kwargs={'tag_slug':self.slug})

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')