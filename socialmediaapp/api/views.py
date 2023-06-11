from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import CreatePost, User
from . serializers import CreatePostSerializer, UserSerializer
from django.http import Http404
from django.core.cache import cache
from ipware import get_client_ip
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': '/api/posts'},
        {'GET': '/api/posts/id'},
        {'GET': '/api/users'},
    ]

    return Response(routes)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

"""
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_x_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].stripe()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
"""

#@cache_page(CACHE_TTL)
def rate_limit(request):
    current_ip = get_client_ip(request)

    if cache.get(current_ip):
        print('123')
        total_calls = cache.get(current_ip)
        
        if total_calls > 5:
            return JsonResponse({'status': 501, 'message': 'You have exhaused the free version limit.', 'time': f'You can try after {cache.ttl(current_ip)}'})
        else:
            cache.set(current_ip, total_calls+1)
            return JsonResponse({'status': 201})

    print("345")
    cache.set(current_ip, 1, timeout=60)
    return JsonResponse({'status': 200, 'ip': get_client_ip(request)})


@api_view(['GET'])
def get_posts(request):
    current_ip = get_client_ip(request)

    if cache.get(current_ip):
        total_calls = cache.get(current_ip)
        posts = CreatePost.objects.all()
        serializer = CreatePostSerializer(posts, many=True)

        if total_calls < 5:
            cache.set(current_ip, total_calls+1)
            return Response(serializer.data)
        else:
            return JsonResponse({'status': 501, 'message': 'You have exhaused the free version limit.', 'time': f'You can try after {cache.ttl(current_ip)} sec.'})

    
    cache.set(current_ip, 1, timeout=60)
    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, pk):
    post = CreatePost.objects.get(id=pk)
   
    serialzer = CreatePostSerializer(post, many=False)
    return Response(serialzer.data)
#    return Http404

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
