from jinja2 import Environment, PackageLoader
import markdown
import preorder.config
import yagmail


# Jinja2 templating
tmpl_env = Environment(loader=PackageLoader('preorder', 'templates'))
tmpl_env.filters['markdown'] = markdown.markdown

# Email configuration
if preorder.config.EMAIL:
    mailer = yagmail.SMTP(**preorder.config.EMAIL)
else:
    mailer = None
