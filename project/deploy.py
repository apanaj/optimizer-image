#!/usr/bin/env python

from app import create_app
from config import DeploymentConfig

application = create_app(DeploymentConfig, 'image-optimizer')
application.run(debug=True, host='0.0.0.0')
