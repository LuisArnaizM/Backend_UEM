from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, MovimientoViewSet, MovimientoProductoAPIView


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
        path('api/movimientos/producto/<int:producto_id>/', MovimientoProductoAPIView.as_view(), name='movimiento_producto'),

]

