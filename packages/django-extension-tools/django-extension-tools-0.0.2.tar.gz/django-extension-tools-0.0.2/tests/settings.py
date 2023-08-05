SECRET_KEY = 'fake-key'

ALLOWED_ADMIN_IP_LIST = ['xxx.xxx.xxx.xxx', 'xxx.xx.xx.xx']

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware'
]
