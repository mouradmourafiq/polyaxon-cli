# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.schemas.global_configuration import GlobalConfigurationConfig


class TestGlobalConfigs(TestCase):
    def test_globl_config(self):
        config_dict = {'verbose': True,
                       'host': 'localhost',
                       'working_directory': '.'}
        config = GlobalConfigurationConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
