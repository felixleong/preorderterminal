from voluptuous import (
    Boolean,
    Coerce,
    Optional,
    Required,
    Schema,
    REMOVE_EXTRA)


# Email section schema
_EMAIL_SCHEMA = Schema({
    Required('host'): str,
    Optional('port', default=25): Coerce(int),
    Optional('login'): str,
    Optional('password'): str,
    Optional('tls', default=False): Boolean(),
}, extra=REMOVE_EXTRA)

# Full configuration schema
CONFIG_SCHEMA = Schema({
    Optional('email'): _EMAIL_SCHEMA,
}, extra=REMOVE_EXTRA)
