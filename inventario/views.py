from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Producto, Movimiento
from .serializers import ProductoSerializer, MovimientoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Producto, Movimiento
from .serializers import MovimientoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]
class MovimientoProductoAPIView(APIView):
    """
    Vista para obtener los movimientos de un producto específico y actualizar
    las existencias del producto.
    """

    def get(self, request, producto_id):
        """
        Obtener todos los movimientos de un producto específico.
        """
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise NotFound("Producto no encontrado")

        # Obtener los movimientos de ese producto
        movimientos = Movimiento.objects.filter(producto=producto)
        serializer = MovimientoSerializer(movimientos, many=True)
        return Response(serializer.data)

    def post(self, request, producto_id):
        """
        Crear un nuevo movimiento para un producto y actualizar el inventario.
        """
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise NotFound("Producto no encontrado")

        # Deserializar los datos de la solicitud
        serializer = MovimientoSerializer(data=request.data)
        if serializer.is_valid():
            # Crear el movimiento
            movimiento = serializer.save(producto=producto)

            # Actualizar las existencias del producto
            if movimiento.tipo == 'entrada':
                producto.precio += movimiento.cantidad 
            elif movimiento.tipo == 'salida':
                if producto.precio - movimiento.cantidad >= 0:  # Evitar inventario negativo
                    producto.precio -= movimiento.cantidad
                else:
                    return Response({"detail": "Cantidad insuficiente en inventario."}, status=status.HTTP_400_BAD_REQUEST)

            producto.save()  # Guardamos el producto con el inventario actualizado

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)