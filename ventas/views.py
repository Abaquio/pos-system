from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto,Venta
from .forms import ProductoForm, VentaForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from django.contrib import messages

#pagina de inicio
def home(request):
    return render(request,'ventas/home.html')

#agregar productos
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            form.save()
            messages.success(request, f'¡Producto <strong>"{producto.nombre}"</strong> agregado con éxito!')
            return redirect("agregar_producto")  # Redirecciona para evitar reenvío del formulario
        else:
            messages.error(request, "Por favor, completa todos los campos correctamente.")
    else:
        form = ProductoForm()
    return render(request, 'ventas/agregar_producto.html', {'form': form})

def registrar_venta(request):
    return render(request, 'ventas/registrar_venta.html')

#registrar venta 1
#def registrar_venta(request):
 #   if request.method == 'POST':
  #     if form.is_valid():
   ####else:
       ## return render(request, 'ventas/registrar_venta.html', {'form':form})
    
#generar boleta
def generar_boleta(request):
    # Obtener todas las ventas registradas
    ventas = Venta.objects.all()

    # Crear la respuesta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleta.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Boleta de Venta")

    p.setFont("Helvetica", 12)
    fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M")
    p.drawString(50, height - 80, f"Fecha: {fecha_actual}")

    # Encabezado de la tabla
    y_position = height - 120
    p.drawString(50, y_position, "Producto")
    p.drawString(250, y_position, "Cantidad")
    p.drawString(350, y_position, "Precio")
    p.drawString(450, y_position, "Subtotal")
    
    y_position -= 20
    p.line(50, y_position, 500, y_position)
    y_position -= 20

    # Agregar los productos vendidos
    total_general = 0
    for venta in ventas:
        p.drawString(50, y_position, venta.producto.nombre)
        p.drawString(250, y_position, str(venta.cantidad))
        p.drawString(350, y_position, f"${venta.producto.precio}")
        p.drawString(450, y_position, f"${venta.total}")
        total_general += venta.total
        y_position -= 20

    # Línea final
    p.line(50, y_position, 500, y_position)
    y_position -= 20

    # Total final
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, f"Total a pagar: ${total_general}")

    # Finalizar el PDF
    p.showPage()
    p.save()
    
    return response

#inventario
def inventario(request):
    productos = Producto.objects.all()

    stock_total = sum(producto.stock for producto in productos)
    return render(request,'ventas/inventario.html',{'productos':productos, 'stock_total':stock_total})

#detalle del producto
def inventario_editar(request,id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request,f'¡Producto <strong>"{producto.nombre}"</strong> actualizado correrctamente!')
            return redirect('inventario_editar', id=id)
    
    else:
        form = ProductoForm(instance=producto)


    return render(request,'ventas/inventario_editar.html',{'form':form,'producto':producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect('inventario')  # Redirige a la lista de productos

    return redirect('inventario')
