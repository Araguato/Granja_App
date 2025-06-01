from django.http import HttpResponse

def test_view(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Test Page</h1>
        <p>If you can see this, Django is working!</p>
        <p><a href="/admin/">Go to Admin</a></p>
    </body>
    </html>
    ''')
