# Telescoop Auth

## Quick start

1. Add "Telescop Auth" to your INSTALLED_APPS setting like this::
```python
INSTALLED_APPS = [
    ...
    'telescoop_auth',
]
```

2. Include the Telescop Auth URLconf in your project urls.py like this::

    path('auth/', include('telescoop_auth.urls')),

3. Run ``python manage.py migrate`` to create the auth models.
