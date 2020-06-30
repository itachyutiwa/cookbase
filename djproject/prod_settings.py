from .settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()
DEBUG = False
TEMPLATE_DEBUG =False
ALLOWED_HOSTS = ['cookbases.herokuapp.com','127.0.0.1']
SECRET_KEY = 'zr+d1p99knhoevd2f-gz3p0dl=h-)()bar_e!8lo6zdbdrlqx9'