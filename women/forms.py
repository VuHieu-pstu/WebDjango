from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

'''
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255,
                            min_length=5,
                            label="Заголовок",
                            validators=[
                                RussianValidator(),
                            ],
                            error_messages={
                                'min_length': 'requirement minimum 5 letter!',
                            })
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10}),
                              required=False,
                              label="Контент",
                              validators=[
                                  MinLengthValidator(5, message="toi thieu 5 ky tu"),
                                  MaxLengthValidator(3000, message="toi da 3000 ky tu")
                              ]
                              )
    is_published = forms.BooleanField(label="Статус", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),required=False,empty_label="Категория не выбран", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(),required=False,empty_label="Не замужем", label="Муж")
'''

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Категория не выбран", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label="Муж")
    class Meta:
        model = Women
        fields = '__all__'
        #fields = ['title', 'content', 'slug', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 120, 'rows': 10}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
    # chi cho upload file co dinh dang image, khi do can phai cai them thu vien pillow
    #file = forms.ImageField(label="Файл")

