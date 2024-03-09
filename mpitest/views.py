from django.views.generic import TemplateView

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = 'home.html'
    
# @method_decorator(csrf_exempt, name='dispatch')
# class SavePoll(APIView):
    