from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()  # Convierte solo la primera letra en mayúscula
        self.categoria = self.categoria.capitalize()  # Opcional, si también quieres capitalizar la categoría
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *arg, **kwargs):
        self.total = self.producto.precio * self.cantidad
        self.producto.stock -= self.cantidad
        self.producto.save()
        super().save(*arg, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} x {self.producto.nombre} - ${self.total}"
# Create your models here.
