from django.urls import path
from .views import home,RegisterView,predict_price,Prediction
from django.contrib.auth import views as auth_views
from .views import CustomLoginView,custom_logout 
from .forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.site.site_header = 'House Price Prediction Admin Page'
admin.site.site_title = 'House Price Prediction Admin Dashboard'

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='HOUSE_ML/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', custom_logout, name='logout'), 

    # path('predict-price/',PredictionView.as_view(),name='predict-price')
    path('predict-price/',predict_price,name='predict-price'),
    path('get_location_names/', Prediction.as_view(), name='get_location_names'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


