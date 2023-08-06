# django-simpletask

Django application provides simple task model and admin.


## Install

```
pip install django-simpletask
```

## Usage

**app/models.py**

```
from django_simpletask.models import SimpleTask


class Task(SimpleTask):
    pass
```

**app/admin.py**

```
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]
    readonly_fields = [] + Task.SIMPLE_TASK_FIELDS
```

## Release

### v0.1.0 2020/10/26

- First release.
- Take from django-fastadmin. django-fastadmin should forcus on admin extensions, but NOT abstract models.
