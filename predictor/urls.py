from django.urls import path
from . import views

urlpatterns = [
    # HTML Pages
    path('', views.home, name='home'),
    path('train/', views.train_page, name='train'),

    # API Endpoints
    path('api/predict/', views.PredictAPI.as_view(), name='api-predict'),
    path('api/train/', views.TrainAPI.as_view(), name='api-train'),
    path('api/delete/', views.DeleteAPI.as_view(), name='api-delete'),
    path('api/reset/', views.ResetAPI.as_view(), name='api-reset'),
    path('api/delete-all/', views.DeleteAllAPI.as_view(), name='api-delete-all'),
    path('api/training-stats/', views.TrainingStatsAPI.as_view(), name='api-training-stats'),
]
