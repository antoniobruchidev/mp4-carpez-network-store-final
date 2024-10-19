from django import forms
from .models import Brand, Product, Category, Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, HTML

input_css_class = 'form-control'
input_css_class_tags = 'form-select'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'category',
                  'tags', 'brand', 'sku',]

    name = forms.CharField(max_length=254, required=True, label='Name:')
    price = forms.DecimalField(decimal_places=2, required=True, label='Price:')
    image = forms.ImageField(label='Image:', required=True)
    description = forms.CharField(max_length=254, label='Description')
    categories = forms.Select()
    tags = forms.SelectMultiple()
    brands = forms.Select()
    sku = forms.CharField(label='SKU')

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            Fieldset(
                'Add a product',
                'name',
                'description',
                'category',
                'brand',
                'tags',
                'sku',
                'price',
                'image'
            ),
            ButtonHolder(HTML(
                '<button class="btn-reset ml-2" type="reset">Reset</button>'
                '<button class="btn-submit ml-2" type="submit">Submit</button>'),
                css_class='text-end' 
            )
        )
        return helper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        tags = Tag.objects.all()
        _categories = [(c.id, c.get_friendly_name()) for c in categories]
        _tags = [(t.id, t.get_friendly_tag()) for t in tags]
        _brands = [(b.id, b.brand)for b in brands]
        self.fields['category'].choices = _categories
        self.fields['tags'].choices = _tags
        self.fields['brand'].choices = _brands
