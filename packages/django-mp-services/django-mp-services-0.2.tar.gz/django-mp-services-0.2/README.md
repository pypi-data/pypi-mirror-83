
Install with pip:

```
pip install django-mp-services
```

Settings:
```
INSTALLED_APPS = [
    ...,
    'services'
]
```

Urls:
```
path('services/', include('services.urls')),
```

Admin:
```
ParentItem(
    _('Service items'),
    icon='fa fa-th-list',
    children=[
        ChildItem(
            label=_('Service list'),
            url='admin:services_serviceitem_changelist'
        ),
        ChildItem(
            label=_('Print services'),
            url='services:print-service-items'
        )
    ]
),
```
