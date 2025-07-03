import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '2b1e7e2c-8c7e-4e2e-9b7a-1f3e4c5d6a7b')
    
    # Use DATABASE_URL from environment for PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PostgreSQL-specific settings (only for PostgreSQL)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgresql://'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_timeout': 20,
            'pool_recycle': 300,
            'max_overflow': 20,
            'pool_pre_ping': True,
        }
    
    # File upload settings
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    UPLOAD_FOLDER = 'app/static/pdfs'
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Security settings - No session timeout for uptime monitors
    PERMANENT_SESSION_LIFETIME = None  # No session timeout
    WTF_CSRF_TIME_LIMIT = None  # No CSRF token expiry
    
    # Session configuration
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_MAX_AGE = None  # No cookie max age
    SESSION_REFRESH_EACH_REQUEST = False  # Don't refresh on each request
    
    # Flask-Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER') 
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Render-specific settings
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME') 
