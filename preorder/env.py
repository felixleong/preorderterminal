from jinja2 import Environment, PackageLoader
from mailchimp3 import MailChimp
from marrow.mailer import Mailer
import markdown
import preorder.config


# Markdown configuration
def markdown_filter(text):
    return markdown.markdown(
        text,
        extensions=preorder.config.JINJA2['markdown_extensions'].split(','))


# Jinja2 templating
tmpl_env = Environment(loader=PackageLoader('preorder', 'templates'))
tmpl_env.filters['markdown'] = markdown_filter


if preorder.config.EMAIL:
    mailer = Mailer({
            'manager.use': 'futures',
            'transport.use': 'smtp',
            'transport.host': preorder.config.EMAIL['host'],
            'transport.tls': 'ssl',
            'transport.username': preorder.config.EMAIL['username'],
            'transport.password': preorder.config.EMAIL['password'],
            'transport.max_messages_per_connection': 5
        })
    mailer.start()
else:
    mailer = None

if preorder.config.MAILCHIMP:
    mailchimp = MailChimp(
        preorder.config.MAILCHIMP['user'],
        preorder.config.MAILCHIMP['api_key'])
else:
    mailchimp = None
