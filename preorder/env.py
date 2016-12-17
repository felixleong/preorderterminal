from jinja2 import Environment, PackageLoader

tmpl_env = Environment(loader=PackageLoader('preorder', 'templates'))
