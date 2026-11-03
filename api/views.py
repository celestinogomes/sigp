from django.shortcuts import render
from custom.models import Municipality, AdministrativePost, Village, Aldeia
from django.http import JsonResponse

def load_posts(request):
    municipality_id = request.GET.get('municipality_id')
    posts = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('name')
    
    data = [{'id': post.id, 'name': post.name} for post in posts]
    return JsonResponse(data, safe=False)

def load_villages(request):
    administrative_post_id = request.GET.get('administrative_post_id')
    villages = Village.objects.filter(administrative_post_id=administrative_post_id).order_by('name')
    
    data = [{'id': village.id, 'name': village.name} for village in villages]
    return JsonResponse(data, safe=False)

def load_aldeia(request):
    village_id = request.GET.get('village_id')
    aldeias = Aldeia.objects.filter(village_id=village_id).order_by('name')
    
    data = [{'id': ald.id, 'name': ald.name} for ald in aldeias]
    return JsonResponse(data, safe=False)
      