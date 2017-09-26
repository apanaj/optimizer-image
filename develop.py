#!/usr/bin/env python

from project.app import create_app
from project.config import DevelopmentConfig

application = create_app(DevelopmentConfig, 'image-optimizer')

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
