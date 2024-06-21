#!/bin/bash
FLASK_APP=api.v1.app flask db init
FLASK_APP=api.v1.app flask db migrate -m "$(date)"
FLASK_APP=api.v1.app flask db upgrade
