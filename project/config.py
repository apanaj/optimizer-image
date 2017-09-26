
class DevelopmentConfig(object):
    DEBUG = True
    MEDIA_FOLDER = '/home/majid/media/'
    SOURCE_FOLDER = MEDIA_FOLDER + 'source/'
    CONVERT_FOLDER = MEDIA_FOLDER + 'convert/'
    OPTIMIZED_FOLDER = MEDIA_FOLDER + 'optimized/'
    MOZJPEG_FOLDER = '/home/majid/mozjpeg/'


class DeploymentConfig(object):
    DEBUG = False
    MEDIA_FOLDER = '/home/majid/media/'
    SOURCE_FOLDER = MEDIA_FOLDER + 'source/'
    CONVERT_FOLDER = MEDIA_FOLDER + 'convert/'
    OPTIMIZED_FOLDER = MEDIA_FOLDER + 'optimized/'
    MOZJPEG_FOLDER = '/home/majid/mozjpeg/'
