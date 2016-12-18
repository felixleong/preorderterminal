from jinja2 import Environment, PackageLoader
import markdown
import preorder.config
import yagmail


# Markdown configuration
def markdown_filter(text):
    return markdown.markdown(
        text,
        extensions=preorder.config.JINJA2['markdown_extensions'].split(','))


# Jinja2 templating
tmpl_env = Environment(loader=PackageLoader('preorder', 'templates'))
tmpl_env.filters['markdown'] = markdown_filter

# Email configuration
if preorder.config.EMAIL:
    mailer = yagmail.SMTP(**preorder.config.EMAIL)
else:
    mailer = None
