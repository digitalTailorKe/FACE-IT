# import os

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
#     SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
#     REMEMBER_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
#     SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing session cookies
#     SESSION_COOKIE_SAMESITE = 'Lax'  # Prevent CSRF attacks by ensuring cookies are sent only with requests from the same site
