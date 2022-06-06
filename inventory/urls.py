from django.urls import path

from inventory import views

app_name = 'inventory'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('plane/list/', views.PlaneListView.as_view(), name='plane_list'),
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    # path('order/', views.OrderCreateView.as_view(), name='order'),
    path('order/<int:pk>/', views.StockOrderView.as_view(), name='order'),
    path(
        'order/<int:pk>/details/', views.OrderDetailView.as_view(),
        name='order_details'
    ),
    path(
        'order/<int:pk>/fill/', views.FillOrderView.as_view(),
        name='fill_order'
    ),
    path(
        'change/<int:pk>/status/', views.ChangePlaneStatusView.as_view(),
        name='change_plane_status'
    ),
    path(
        'order/<int:pk>/download/', views.OrderPDFView.as_view(),
        name='download_order_pdf'
    ),
    path(
        'order/list/download/', views.OrderListPDFView.as_view(),
        name='download_order_list_pdf'
    ),
]
