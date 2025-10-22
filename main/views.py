from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Rapat, Menu, Pesanan, PesananItem
import qrcode
from io import BytesIO

# Homepage - List semua rapat
def home(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        if judul:
            rapat = Rapat.objects.create(judul=judul)
            return redirect('rapat_detail', slug=rapat.slug)
    
    rapats = Rapat.objects.all()
    return render(request, 'main/home.html', {'rapats': rapats})

# Detail rapat - List pesanan
def rapat_detail(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    pesanans = rapat.pesanans.all()
    
    # Generate QR code
    url = request.build_absolute_uri(f'/rapat/{slug}/')
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    import base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'main/rapat_detail.html', {
        'rapat': rapat,
        'pesanans': pesanans,
        'qr_code': qr_base64
    })

# Edit rapat
def rapat_edit(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    if request.method == 'POST':
        rapat.judul = request.POST.get('judul')
        rapat.save()
        return redirect('rapat_detail', slug=rapat.slug)
    return render(request, 'main/rapat_edit.html', {'rapat': rapat})

# Delete rapat
def rapat_delete(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    if request.method == 'POST':
        rapat.delete()
        return redirect('home')
    return render(request, 'main/rapat_delete.html', {'rapat': rapat})

# Download QR Code
def rapat_qr(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    url = request.build_absolute_uri(f'/rapat/{slug}/')
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr-{slug}.png"'
    return response

# Form pemesanan
def rapat_pesan(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    menus = rapat.menus.all()
    
    if request.method == 'POST':
        nama_pemesan = request.POST.get('nama_pemesan')
        if nama_pemesan:
            pesanan = Pesanan.objects.create(
                rapat=rapat,
                nama_pemesan=nama_pemesan
            )
            
            # Process menu items
            for menu in menus:
                qty = request.POST.get(f'menu_{menu.id}')
                if qty and int(qty) > 0:
                    PesananItem.objects.create(
                        pesanan=pesanan,
                        menu=menu,
                        quantity=int(qty)
                    )
            
            # Process custom request
            custom = request.POST.get('custom_request')
            custom_qty = request.POST.get('custom_quantity')
            if custom and custom_qty and int(custom_qty) > 0:
                PesananItem.objects.create(
                    pesanan=pesanan,
                    custom_request=custom,
                    quantity=int(custom_qty)
                )
            
            return redirect('rapat_detail', slug=slug)
    
    return render(request, 'main/rapat_pesan.html', {
        'rapat': rapat,
        'menus': menus
    })

# Edit pesanan
def pesanan_edit(request, slug, pesanan_id):
    rapat = get_object_or_404(Rapat, slug=slug)
    pesanan = get_object_or_404(Pesanan, id=pesanan_id, rapat=rapat)
    menus = rapat.menus.all()
    
    if request.method == 'POST':
        pesanan.nama_pemesan = request.POST.get('nama_pemesan')
        pesanan.save()
        
        # Delete old items
        pesanan.items.all().delete()
        
        # Process menu items
        for menu in menus:
            qty = request.POST.get(f'menu_{menu.id}')
            if qty and int(qty) > 0:
                PesananItem.objects.create(
                    pesanan=pesanan,
                    menu=menu,
                    quantity=int(qty)
                )
        
        # Process custom request
        custom = request.POST.get('custom_request')
        custom_qty = request.POST.get('custom_quantity')
        if custom and custom_qty and int(custom_qty) > 0:
            PesananItem.objects.create(
                pesanan=pesanan,
                custom_request=custom,
                quantity=int(custom_qty)
            )
        
        return redirect('rapat_detail', slug=slug)
    
    return render(request, 'main/pesanan_edit.html', {
        'rapat': rapat,
        'pesanan': pesanan,
        'menus': menus
    })

# Delete pesanan
def pesanan_delete(request, slug, pesanan_id):
    rapat = get_object_or_404(Rapat, slug=slug)
    pesanan = get_object_or_404(Pesanan, id=pesanan_id, rapat=rapat)
    
    if request.method == 'POST':
        pesanan.delete()
        return redirect('rapat_detail', slug=slug)
    
    return render(request, 'main/pesanan_delete.html', {
        'rapat': rapat,
        'pesanan': pesanan
    })

# Kelola menu
def menu_kelola(request, slug):
    rapat = get_object_or_404(Rapat, slug=slug)
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            Menu.objects.create(rapat=rapat, nama=nama)
            return redirect('menu_kelola', slug=slug)
    
    menus = rapat.menus.all()
    return render(request, 'main/menu_kelola.html', {
        'rapat': rapat,
        'menus': menus
    })

# Edit menu
def menu_edit(request, slug, menu_id):
    rapat = get_object_or_404(Rapat, slug=slug)
    menu = get_object_or_404(Menu, id=menu_id, rapat=rapat)
    
    if request.method == 'POST':
        menu.nama = request.POST.get('nama')
        menu.save()
        return redirect('menu_kelola', slug=slug)
    
    return render(request, 'main/menu_edit.html', {
        'rapat': rapat,
        'menu': menu
    })

# Delete menu
def menu_delete(request, slug, menu_id):
    rapat = get_object_or_404(Rapat, slug=slug)
    menu = get_object_or_404(Menu, id=menu_id, rapat=rapat)
    
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_kelola', slug=slug)
    
    return render(request, 'main/menu_delete.html', {
        'rapat': rapat,
        'menu': menu
    })
