#!/usr/bin/env python

from project.app import create_app
from project.config import DeploymentConfig

application = create_app(DeploymentConfig, 'image-optimizer')
