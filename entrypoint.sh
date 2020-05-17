#!/bin/bash
exec gunicorn -k flask_sockets.worker node.app:create_app() \
"$@"
