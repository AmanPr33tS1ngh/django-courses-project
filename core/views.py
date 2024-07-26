from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from appointment.models import Contact

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')
    
class ContactUs(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contact_us.html')
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            return render(request, 'contact_us.html', {'error': 'All fields are required'})
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        return JsonResponse(status=200)
        return render(request, 'contact_us.html', {'success': 'Message sent successfully'})