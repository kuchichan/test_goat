from django import forms
from django.db import models
from .models import Item, List
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            _instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return _instances[cls]        

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.fields.TextInput(
                attrs={
                    "placeholder": "Enter a to-do item",
                    "class": "form-control input-lg",
                }
            ),
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

class ShareeForm(forms.Form):
    sharee = forms.EmailField()

    def save(self):
        return self.cleaned_data["sharee"]
    


def instert_sort(array):
    for i in range(1, len(array)):
        elem = array[i]
        j = i - 1
        while j <= 0 and elem < array[j]:
            array[j] = array[j+1]
        array[j] = elem
        
