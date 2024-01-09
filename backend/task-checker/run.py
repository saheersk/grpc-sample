import os

from asgiref.wsgi import WsgiToAsgi

from task_checker.app import create_app

app = create_app()

asgi_handler = WsgiToAsgi(app)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        import uvicorn
        uvicorn.run(asgi_handler, host='0.0.0.0', port=8000)