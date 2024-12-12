# Home application

It has a single view for the landing page

## Development

### vscode terminal
```python
python manage.py createapp home
```

### '/ecommerce/settings.py'
```python
INSTALLED_APPS = [
    ...
    'home',
    ...
]
```

### '/home/urls.py'
```python
urlpatterns = [
    path('', views.home, name='home')
]
```

### '/ecommerce/urls.py'
```python
urlpatterns = [
    ...
    path('', include('home.urls')),
    ...
]
```

## Usage
Change enviroment variable HOMEPAGE_CAROUSEL_TAG to a tag to show the tagged products in the homepage carousel 

## Testing

Changing environment variable HOMEPAGE_CAROUSEL_TAG to a string not representing any tab would cause a 404 error. This will fix it in the home view.
```python
try:
    tag = Tag.objects.get(tag=settings.HOMEPAGE_CAROUSEL_TAG)
except Tag.DoesNotExist:
    tag = Tag.objects.get(tag="clearance")
```
together with this in the delete_tag view in dashboard views.
```python
if (tag.tag == 'desktop' or tag.tag == 'laptop' or
                tag.tag == 'clearance'):
```
as they should not be deleted or it would cause errors in the navbar with the desktop and laptop buttons and in the homepage in the carousel.
Also I had to remove the products queryset length and pass it empty, otherwise it would cause an error when giving a tag not associated with any product.
