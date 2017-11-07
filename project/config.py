class DefaultConfig(object):
    SECRET_KEY = 'EBk^qa7j[fLH[o0?&/kTuN6'
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # MB

    OPTIMIZE_TAGS = {
        'thumb': {
            'out_type': 'crop',
            'size': '400x400',
            'quality': '90'
        }
    }


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    MEDIA_FOLDER = '/tmp/'
    SOURCE_FOLDER = '/tmp/'
    CONVERT_FOLDER = '/tmp/'
    OPTIMIZED_FOLDER = '/tmp/'
    MOZJPEG_FOLDER = '/home/majid/mozjpeg/'


class DeploymentConfig(DefaultConfig):
    DEBUG = False
    MEDIA_FOLDER = '/tmp/'
    SOURCE_FOLDER = '/tmp/'
    CONVERT_FOLDER = '/tmp/'
    OPTIMIZED_FOLDER = '/tmp/'
    MOZJPEG_FOLDER = '/mozjpeg/'
