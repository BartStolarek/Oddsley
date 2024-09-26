from django.http import HttpResponse

def home(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to the Oddsley Backend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f4f4f4;
                color: #333;
            }
            h1 {
                color: #007BFF;
            }
            a {
                text-decoration: none;
                color: #007BFF;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Backend!</h1>
        <p>This API does not have a frontend UI.</p>
        <p>You can access the API documentation at:</p>
        <ul>
            <li><a href="/swagger/">Swagger UI</a></li>
            <li><a href="/redoc/">Redoc</a></li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html_content)
