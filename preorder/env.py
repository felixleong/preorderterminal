from jinja2 import Environment, PackageLoader
import yagmail
import preorder.config


# Jinja2 templating
tmpl_env = Environment(loader=PackageLoader('preorder', 'templates'))

# Email configuration
if preorder.config.EMAIL:
    print(preorder.config.EMAIL)
    mailer = yagmail.SMTP(**preorder.config.EMAIL)
else:
    mailer = None
