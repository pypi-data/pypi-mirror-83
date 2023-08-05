[![PyPI version](https://badge.fury.io/py/connexion-plus.svg)](https://badge.fury.io/py/connexion-plus)![Workflow Status](https://github.com/Sciebo-RDS/connexion-plus/workflows/Publish%20Python%20%F0%9F%90%8D%20distributions%20%F0%9F%93%A6%20to%20PyPI%20and%20TestPyPI/badge.svg)

[Connexion](https://github.com/zalando/connexion) with benefits for microservices.

# Connexion Plus

If you want to use [Connexion](https://github.com/zalando/connexion) for your microservice, you have to add an [opentracing](https://opentracing.io/) or [prometheus](https://prometheus.io/) client on your own. With this library, you instantiate everything before your connexion app starts and this library will take care to put it all together, so you get everything fine.

> Currently this library works only for Flask!

This library give you a new class `App`, which you have to use instead of the connexion FlaskApp, to get everything working. The App inheritates from connexion app, so you can use it with your old code, but replace your import with `from connexion_plus import App`.

If you want to know more about the used libraries, please go to the corresponding documentaries.

## Dependencies

- [Connexion](https://github.com/zalando/connexion)
- [opentracing-python-instrumentation](https://github.com/uber-common/opentracing-python-instrumentation)
- [Flask-Opentracing](https://github.com/opentracing-contrib/python-flask)
- [jaeger-client](https://pypi.org/project/jaeger-client/)
- [requests](https://pypi.org/project/requests/)
- [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/)

## Importing

```python
from connexion_plus import App
```

## OpenTracing / Jaeger-Client

Currently, all opentracing implementation (e.g. [jaeger-client](https://pypi.org/project/jaeger-client/)) are supported for tracing. But this library use a third party function, that only supports Flask. If you want to use it, you have to initialize the client before you start your connexion app and give it via the `tracer`-parameter to the `connexion_plus` App, where the magic happens.

If you want to use a default tracer, you can use `use_tracer=True` simply.

The following example uses jaeger-client (`pip install jaeger-client`) implementation. (Currently installs with connexion-plus per default)

```python
from connexion_plus import App
from jaeger_client import Config as jConfig

config = jConfig(
        config={
            'logging': True,
        },
    )
jaeger_tracer = config.initialize_tracer()

app = App(__name__, use_tracer=jaeger_tracer)
```

If you use the tracer, you get also a TracingHandler in your logging module under the empty name, so your logging message can be logged with opentracing.

```python
logging.getLogger('')
```

You can edit the logging-level with the `use_logging_level`-parameter of the addServices-method. DEBUG is the default level, so you get everything from the log within a route in your opentracing-ui. (As long as there are a span while you write a logging message, you will see the logging message in your span)
```python
import logging
from connexion_plus import App

app = App(app, use_tracer=config.initialize_tracer(), use_logging_level=logging.DEBUG)
```

It improve the performance slightly, when you set the log-level to a higher level (INFO, WARNING).

## Prometheus / Metrics

Currently, it is only the [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/) supported for connexion, so only for flask connexion. You only have to set the `metrics`-parameter to `True`

```python
from connexion_plus import App

app = App(__name__, use_metric=True)
```

## Use a default error handler

For a faster implementation, you can use a default error handler. Set the parameter `use_default_handler` to True for use a simple default handler. Otherwise give a function / method to this parameter, which handles your exceptions.

## Complete example

If you want to use `tracer` and `metrics` together, see here a complete example. This currently works only with flask (see prometheus)

```python
from connexion_plus import App
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
import logging

config = jConfig(
        config={
            'logging': True,
        },
        # use this, if you want to track your tracing itself with prometheus
        metrics_factory = PrometheusMetricsFactory(namespace=name),
    )
jaeger_tracer = config.initialize_tracer()

app = App(name, use_tracer=config.initialize_tracer(), use_metric=True, use_optimizer=True, use_cors=True, use_logging_level=logging.DEBUG)
app.add_api('openapi.yaml', resolver=RestyResolver('api'))
```

If you add the line `metrics_factory=PrometheusMetricsFactory(namespace='yourAppName')` to your jaeger-client-config, you get the metrics out of jaeger into your flask app to track all metrics at once `/metrics`.

## More features

If you want to get the current tracing object in a request context, you can use [FlaskTracing](https://github.com/opentracing-contrib/python-flask#accessing-spans-manually)

```python
import Flasktracing
FlaskTracing.get_span(request)
```

If you get a collision of your view-functions, you can use `from connexion-plus.MultipleResourceResolver import MultipleResourceResolver` as a replacement for RestyResolver to get better control of multi resource path e.g. /resource1/{id1}/resource2/{id2} tries to find the classes *Resource1Resource2* or *resource1resource2* in the given "api" folder.

## Use of optimizer

If you want to use the optimizer or use custom configs for single routes, you can use the FlaskOptimize class `from connexion_plus import FlaskOptimize`.
This class has the methods `do_not_minify` (the decorated route will not minified before send), `do_not_compress` (the decorated route will not compressed before send) and `set_cache_timeout(seconds)` (default 24h) (the response from the decorated route will be cached until `seconds`).

Currently it is only be possible to deactivate the global config `use_optimizer` and not activate single routes with e.g. `minify`. This could be your first contributation to this project. :)

### Importing Multiple Resources

If you want to make usage of multiple resource in a single URL (e.g. /Res1/{Para1}/Res2), you can use the `from connexion-plus import MultiResourceResolver` as your connexion resolver. This resolves the example: `/Res1/{Para1}/Res2 resolves in Res1.Res2` and as a convenient function, it resolves also `/Res1/{Para1}/Res2 resolves in Res1Res2`, so you can choose both. The first one searches for folders and at last a file `Res1/Res2.py`. The second searches a file with this name `Res1Res2.py`. Currently no classes inside the files are supported.

If you want to add Methods to a resource (e.g. Res1 should answer for GET and POST), you have to add an `__init__.py` to the folder and import there your resource-file `from .Res1 import *`. If you use the second method, you don't have a folder and a file with the name `Res1`, so you don't need this workaround.

## Examples

You can find more examples in the [repo](https://github.com/Heiss/connexion-plus/tree/master/examples). *Tutorial1* is a simple small (without bonuscode) script without an openapi definition.
Please use *Tutorial2* if you want a complete usage example.

## Research data services

This library is under development for the project [research data services](http://research-data-services.info), a microservice ecosystem.
