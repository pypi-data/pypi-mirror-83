# ZOG Utils

Utilities to use in my base-api project template. https://github.com/tienhm0202/base-fastapi/

Why ZOG? Because I can't named it as `utils` only, so I have to add a prefix.
ZOG sounds like `joke` and looks like `zoo`. I found that funny enough to use.

# Usage

```bash
$ pip install zogutils
```

## To generate short unique id string

```python
from zogutils import secret

secret.unique_id(8, "ID_")
# return: ID_a7uFg9k0
```

## To shorten package name like Java's Logback

```python
from zogutils import package_name

package_name.shorten("company.scope.modules.Function", 9)
# return: (something like) c.s.m.Function - depends on max length
```

## To init some middlewares

```python
from zogutils import middlewares
from your.app import settings, fastapi_app

middlewares.init_app(fastapi_app, settings)
```

### Configs:

```
# Sentry
SENTRY_DSN: Optional[HttpUrl] = None
SENTRY_INCLUDE: Optional[List[str]] = ["src"]
SENTRY_SAMPLE_RATE: Optional[float] = 0.5

# CSRF
SECURITY_CSRF: bool = False

# Rate limit
RATE_LIMIT: int = 100
RATE_LIMIT_TIME_SPAN: int = 30
RATE_LIMIT_BLOCK_DURATION: int = 300

# Prometheus
PROMETHEUS_ENABLE: bool = True
PROMETHEUS_PATH: str = "/metrics/"

# Cors
BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
```