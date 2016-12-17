from voluptuous import (
    Coerce,
    Email,
    Optional,
    Required,
    Schema,
    REMOVE_EXTRA)


# Email section schema
_EMAIL_SCHEMA = Schema({
    Required('host'): str,
    Optional('port'): Coerce(int),
    Optional('user'): str,
    Optional('password'): str,
}, extra=REMOVE_EXTRA)

_RECEIPT_SCHEMA = Schema({
    Required('email'): Email,
    Optional('sender_name'): str,
}, extra=REMOVE_EXTRA)

# Full configuration schema
CONFIG_SCHEMA = Schema({
    Optional('email'): _EMAIL_SCHEMA,
    Optional('receipt'): _RECEIPT_SCHEMA,
}, extra=REMOVE_EXTRA)
