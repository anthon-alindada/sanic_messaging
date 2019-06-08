# -*- coding: utf-8
from app import create_app


if __name__ == '__main__':
    # Create sanic application
    app = create_app()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
