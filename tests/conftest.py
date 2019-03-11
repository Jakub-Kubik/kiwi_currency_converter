# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 11.03.2019

import pytest
from web_api_app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app
