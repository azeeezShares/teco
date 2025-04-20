from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.views import APIView
from django.utils import timezone
from blog.models import Post

from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

class SiteMap(APIView):
    def get(self, request):
        base_url = request.build_absolute_uri("/")[:-1] 
        blog_slugs = Post.objects.values_list('slug', flat=True)

        blog_urls = [
            f"{base_url}/es/blog/{slug}/" for slug in blog_slugs
        ] + [
            f"{base_url}/en/blog/{slug}/" for slug in blog_slugs
        ]

        product_urls = [
            # f"{base_url}/product/{slug}" for slug in product_slugs
        ] + [
            # f"{base_url}/en/product/{slug}" for slug in product_slugs
        ]

        # Statik sahifalar
        static_pages = ['#services', '#locations', '#reviews', 'blog']
        static_urls = [
            f"{base_url}/es/{page}" for page in static_pages
        ] + [
            f"{base_url}/en/{page}" for page in static_pages
        ]

        # Barcha URL'larni birlashtirish
        all_urls = [f"{base_url}/en/", f"{base_url}/es/"] + blog_urls + product_urls + static_urls

        # XML yaratish
        xml_content = self.generate_sitemap_xml(all_urls)

        return HttpResponse(xml_content, content_type="application/xml")

    def generate_sitemap_xml(self, urls):
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for url in urls:
            xml.append('<url>')
            xml.append(f'<loc>{url}</loc>')
            xml.append(f'<lastmod>{timezone.now().strftime("%Y-%m-%d")}</lastmod>')
            xml.append('<changefreq>daily</changefreq>')
            xml.append('<priority>0.5</priority>')
            xml.append('</url>')

        xml.append('</urlset>')

        return '\n'.join(xml)



from django.http import FileResponse
import os

def robots_txt(request):
    # Fayl yo'lini aniqlash
    robots_file_path = os.path.join(os.path.dirname(__file__), 'robots.txt')

    # Faylni ochish va response sifatida yuborish
    try:
        return FileResponse(open(robots_file_path, 'rb'), content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse("Fayl topilmadi", status=404)