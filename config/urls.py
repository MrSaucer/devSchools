from django.contrib import admin
from django.urls import path, include  # 1. IMPORTANTE: Importe o 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. ESSA É A LINHA PRINCIPAL:
    # "Qualquer URL que comece com '' (a raiz do site),
    # inclua o arquivo 'urls.py' do nosso app 'app'."
    path('', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]