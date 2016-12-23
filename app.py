from whitenoise import WhiteNoise
import preorder.api


app = preorder.api.__hug_wsgi__
app = WhiteNoise(app, prefix='static', root='preorder/static/')
