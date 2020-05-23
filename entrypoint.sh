#!/bin/bash
exec gunicorn -k flask_sockets.worker grid_node.__main__:app \
"$@"
