# Django-istio-opentracing
Django opentracing middleware works with k8s and istio

install:


```
pip install django-istio-opentracing
```


example:

add a middle ware to your Django middleware

```python
MIDDLEWARE += [
    'django_istio_opentracing.middleware.Middleware'
]]
```

and if you using requests
jusing using the patch in your __init__.py file
hint: make sure the patch line before your code

```python
from django_istio_opentracing import monkey
monkey.patch_requests()
```

then use requests whatever you want
every request you make will carry the b3 code in header

if you want to use in view:

```python
from django_istio_opentracing import get_opentracing_span_headers
def index(request):
    print(get_opentracing_span_headers())
    return HttpResponse('ok')
```
