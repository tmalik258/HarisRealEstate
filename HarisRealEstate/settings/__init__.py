from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if DEBUG:
   from .local import *
else:
   from .production import *