#!/usr/bin/env python

from app import create_app
from config import DeploymentConfig

application = create_app(DeploymentConfig, 'image-optimizer')

