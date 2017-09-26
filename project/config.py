
class DefaultConfig(object):
    SECRET_KEY = 'EBk^qa7j[fLH[o0?&/kTuN6'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    MEDIA_FOLDER = '/home/majid/media/'
    SOURCE_FOLDER = MEDIA_FOLDER + 'source/'
    CONVERT_FOLDER = MEDIA_FOLDER + 'convert/'
    OPTIMIZED_FOLDER = MEDIA_FOLDER + 'optimized/'
    MOZJPEG_FOLDER = '/home/majid/mozjpeg/'


class DeploymentConfig(DefaultConfig):
    DEBUG = False
    MEDIA_FOLDER = '/home/majid/media/'
    SOURCE_FOLDER = MEDIA_FOLDER + 'source/'
    CONVERT_FOLDER = MEDIA_FOLDER + 'convert/'
    OPTIMIZED_FOLDER = MEDIA_FOLDER + 'optimized/'
    MOZJPEG_FOLDER = '/home/majid/mozjpeg/'
