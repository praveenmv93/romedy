from django.shortcuts import render

def dating_request(request):
    """
    Renders the interactive Coffee Date request page.
    """
    return render(request, 'dating_request.html')
