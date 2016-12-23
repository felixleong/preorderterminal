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
    Optional('username'): str,
    Optional('password'): str,
}, extra=REMOVE_EXTRA)

_MAILCHIMP_SCHEMA = Schema({
    Required('user'): str,
    Required('api_key'): str,
    Required('mailing_list_id'): str,
}, extra=REMOVE_EXTRA)

_JINJA2_SCHEMA = Schema({
    Optional('markdown_extensions', default=''): str,
}, extra=REMOVE_EXTRA)

_RECEIPT_SCHEMA = Schema({
    Required('email'): Email(),
    Optional('sender_name'): str,
    Optional('subject'): str,
}, extra=REMOVE_EXTRA)

_DATA_SCHEMA = Schema({
    Required('spreadsheet_id'): str,
    Required('sheet_name'): str,
}, extra=REMOVE_EXTRA)

# Full configuration schema
CONFIG_SCHEMA = Schema({
    Required('data'): _DATA_SCHEMA,
    Optional('email'): _EMAIL_SCHEMA,
    Optional('mailchimp'): _MAILCHIMP_SCHEMA,
    Optional('receipt'): _RECEIPT_SCHEMA,
    Optional('jinja2'): _JINJA2_SCHEMA,
    Optional('users'): {str: str},
}, extra=REMOVE_EXTRA)
