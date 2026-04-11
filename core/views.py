from decimal import Decimal
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.http import require_POST

from .models import (
    SiteContent, HeroStat, Feature, AboutCard, BenefitTeaser,
    ProductCategory, Product,
    NutrientCard, UsageCard,
    KeyNumber, BenefitDetail,
    MissionValue, ProcessStep,
    Order, OrderItem,
)


def sc(key, default=''):
    """Get SiteContent value by key."""
    try:
        return SiteContent.objects.get(key=key).value
    except SiteContent.DoesNotExist:
        return default


# ─────────────────────────────────────────────────────────────
#  Cart helpers
# ─────────────────────────────────────────────────────────────
def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _cart_items(cart):
    items = []
    total = Decimal('0')
    for pid, item in cart.items():
        sub = Decimal(item['price']) * item['qty']
        items.append({
            'id': pid,
            'name': item['name'],
            'price': Decimal(item['price']),
            'qty': item['qty'],
            'unit': item.get('unit', ''),
            'image': item.get('image', ''),
            'subtotal': sub,
        })
        total += sub
    return items, total


# ─────────────────────────────────────────────────────────────
#  Panel decorator
# ─────────────────────────────────────────────────────────────
def panel_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('/panel/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return _wrapped


# ─────────────────────────────────────────────────────────────
#  Public pages
# ─────────────────────────────────────────────────────────────
def index(request):
    context = {
        'hero_badge':       sc('hero_badge', '100% Байгалийн · УВС аймгийн'),
        'hero_title_1':     sc('hero_title_1', 'Байгалийн'),
        'hero_title_2':     sc('hero_title_2', 'алт жимс'),
        'hero_subtitle':    sc('hero_subtitle', 'Увсын тал хээрийн цэвэр агаарт өссөн чацарганы жимснээс гарган авсан шим тэжээлт бүтээгдэхүүнүүд — таны эрүүл мэндийн найдвартай түнш.'),
        'hero_stats':       HeroStat.objects.all(),
        'features':         Feature.objects.all(),
        'about_label':      sc('about_teaser_label', 'Чацаргана гэж юу вэ'),
        'about_title':      sc('about_teaser_title', 'Байгалийн <em>нандин</em><br>жимс'),
        'about_body':       sc('about_teaser_body', 'Чацаргана нь тод улбар шар өнгөтэй, хүчиллэг амттай жимс бөгөөд дэлхийд хамгийн их шим тэжээл агуулдаг жимсний нэгд тооцогддог.'),
        'about_cards':      AboutCard.objects.all(),
        'preview_products': Product.objects.filter(is_active=True).order_by('order')[:4],
        'benefit_teasers':  BenefitTeaser.objects.all(),
        'products_label':   sc('products_label', 'Манай бүтээгдэхүүнүүд'),
        'products_title':   sc('products_title', 'Чацарганы <em>цуглуулга</em>'),
        'benefits_label':   sc('benefits_label', 'Ашиг тус'),
        'benefits_title':   sc('benefits_title', 'Эрүүл мэндэд <em>үзүүлэх нөлөө</em>'),
    }
    return render(request, 'index.html', context)


def info(request):
    context = {
        'hero_subtitle':    sc('info_hero_subtitle', 'Байгалийн хамгийн баялаг шим тэжээлт жимсний нэгийн тухай'),
        'story_label':      sc('info_story_label', 'Гарал үүсэл'),
        'story_title_1':    sc('info_story_title_1', 'Монголын нутгийн'),
        'story_title_2':    sc('info_story_title_2', 'алтан жимс'),
        'story_body_1':     sc('info_story_body_1', 'Чацаргана <em>(Hippophae rhamnoides)</em> нь тод улбар шар өнгөтэй жимс.'),
        'story_body_2':     sc('info_story_body_2', 'УВС аймгийн нутагт ургасан чацаргана нь цэвэр агаарт бойжсон.'),
        'story_body_3':     sc('info_story_body_3', 'Уламжлалт монгол эмнэлэгт олон зуун жилийн турш хэрэглэж ирсэн.'),
        'fact_num':         sc('info_fact_num', '1956'),
        'fact_text':        sc('info_fact_text', 'он — Оросын сансрын аялагчдын хоолонд анх оруулсан'),
        'nutrition_sub':    sc('info_nutrition_sub', '100 грамм чацарганы жимсэнд агуулагдах гол бодисууд'),
        'nutrient_cards':   NutrientCard.objects.all(),
        'usage_cards':      UsageCard.objects.all(),
        'cta_body':         sc('info_cta_body', 'Байгалийн чацарганаас гарган авсан дэлгэрэнгүй бүтээгдэхүүнүүдтэй танилцаарай'),
    }
    return render(request, 'info.html', context)


def products(request):
    categories = ProductCategory.objects.all()
    all_products = Product.objects.filter(is_active=True).select_related('category').order_by('order')
    context = {
        'categories': categories,
        'products':   all_products,
    }
    return render(request, 'products.html', context)


def benefits(request):
    context = {
        'hero_sub':    sc('angiinfo_hero_sub', 'Эрдэм шинжилгээгээр нотлогдсон байгалийн нандин жимсний биед үзүүлэх нөлөө.'),
        'key_numbers': KeyNumber.objects.all(),
        'benefits':    BenefitDetail.objects.all(),
        'cta_body':    sc('angiinfo_cta_body', 'Чацарганы бүтээгдэхүүнүүдтэй танилцаж, өөрийнхөө хэрэгцээнд тохирохыг сонгоорой'),
    }
    return render(request, 'angiinfo.html', context)


def about(request):
    context = {
        'hero_sub':        sc('about_hero_sub', 'Монголын баялаг байгалийг хайрлаж, Увсын тал нутгийн чацарганыг дэлхийд таниулах зорилготой.'),
        'mission_body_1':  sc('about_mission_body_1', 'Бид Увс аймгийн байгалийн нөхцөлд ургасан чацарганыг хиймэл нэмэлтгүй боловсруулан хүргэдэг.'),
        'mission_body_2':  sc('about_mission_body_2', 'Манай бүтээгдэхүүн бүр хатуу чанарын шалгуур давдаг.'),
        'mission_values':  MissionValue.objects.all(),
        'card_big_text':   sc('about_card_big_text', 'УВС аймгийн тал хээрийн байгалиас цуглуулсан чацарганы жимс.'),
        'card_year':       sc('about_card_year', '2025'),
        'process_steps':   ProcessStep.objects.all(),
        'contact_address': sc('contact_address', 'УВС аймаг, Монгол улс'),
        'contact_phone':   sc('contact_phone', '+976 ···· ····'),
        'contact_email':   sc('contact_email', 'info@chatsargana.mn'),
        'contact_social':  sc('contact_social', 'Facebook · Instagram'),
    }
    return render(request, 'about.html', context)


# ─────────────────────────────────────────────────────────────
#  Cart views
# ─────────────────────────────────────────────────────────────
def cart_view(request):
    cart = _get_cart(request)
    items, total = _cart_items(cart)
    return render(request, 'cart.html', {'items': items, 'total': total})


@require_POST
def cart_add(request, product_id):
    try:
        product = Product.objects.get(pk=product_id, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Бүтээгдэхүүн олдсонгүй'}, status=404)

    qty = max(1, int(request.POST.get('qty', 1)))
    cart = _get_cart(request)
    pid = str(product_id)

    if pid in cart:
        cart[pid]['qty'] += qty
    else:
        cart[pid] = {
            'qty':   qty,
            'price': str(product.price),
            'name':  product.name,
            'unit':  product.unit,
            'image': product.image.url if product.image else '',
        }
    _save_cart(request, cart)

    count = sum(i['qty'] for i in cart.values())
    return JsonResponse({'ok': True, 'cart_count': count})


@require_POST
def cart_remove(request, product_id):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)

    count = sum(i['qty'] for i in cart.values())
    total = sum(Decimal(i['price']) * i['qty'] for i in cart.values())
    return JsonResponse({'ok': True, 'cart_count': count, 'cart_total': str(total)})


@require_POST
def cart_update(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get('qty', 1))

    if pid in cart:
        if qty <= 0:
            cart.pop(pid)
        else:
            cart[pid]['qty'] = qty
    _save_cart(request, cart)

    count   = sum(i['qty'] for i in cart.values())
    total   = sum(Decimal(i['price']) * i['qty'] for i in cart.values())
    subtotal = Decimal(cart[pid]['price']) * qty if (pid in cart and qty > 0) else Decimal('0')
    return JsonResponse({
        'ok':         True,
        'cart_count': count,
        'cart_total': str(total),
        'subtotal':   str(subtotal),
    })


# ─────────────────────────────────────────────────────────────
#  Checkout & Orders
# ─────────────────────────────────────────────────────────────
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('core:cart')

    items, total = _cart_items(cart)

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        lat     = request.POST.get('latitude', '').strip()
        lng     = request.POST.get('longitude', '').strip()
        note    = request.POST.get('note', '').strip()

        errors = {}
        if not name:    errors['name']    = 'Нэр оруулна уу'
        if not phone:   errors['phone']   = 'Утасны дугаар оруулна уу'
        if not address: errors['address'] = 'Хаяг оруулна уу'

        if not errors:
            if not request.session.session_key:
                request.session.create()

            order = Order.objects.create(
                user           = request.user if request.user.is_authenticated else None,
                session_key    = request.session.session_key or '',
                customer_name  = name,
                customer_phone = phone,
                customer_email = email,
                address        = address,
                latitude       = float(lat) if lat else None,
                longitude      = float(lng) if lng else None,
                note           = note,
                total_price    = total,
            )
            for pid, item in cart.items():
                product = None
                try:
                    product = Product.objects.get(pk=int(pid))
                except (Product.DoesNotExist, ValueError):
                    pass
                OrderItem.objects.create(
                    order        = order,
                    product      = product,
                    product_name = item['name'],
                    quantity     = item['qty'],
                    price        = Decimal(item['price']),
                )

            _save_cart(request, {})
            return redirect('core:order_confirm', order_id=order.pk)

        return render(request, 'checkout.html', {
            'items':     items,
            'total':     total,
            'errors':    errors,
            'form_data': request.POST,
        })

    form_data = {}
    if request.user.is_authenticated:
        form_data = {
            'name':  request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    return render(request, 'checkout.html', {
        'items':     items,
        'total':     total,
        'form_data': form_data,
    })


def order_confirm(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # Security: only the owner (by user or session) or staff can view
    if not request.user.is_staff:
        if order.user:
            if not request.user.is_authenticated or order.user != request.user:
                return redirect('core:index')
        else:
            if order.session_key != (request.session.session_key or ''):
                return redirect('core:index')
    return render(request, 'order_confirm.html', {'order': order})


@login_required(login_url='/panel/login/')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


# ─────────────────────────────────────────────────────────────
#  Admin Panel
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
#  User auth (login / logout / register)
# ─────────────────────────────────────────────────────────────
def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        error = 'Нэвтрэх нэр эсвэл нууц үг буруу байна'
    return render(request, 'user_login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('core:index')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    errors = {}
    if request.method == 'POST':
        from django.contrib.auth.models import User
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not email:                        errors['email']     = 'И-мэйл оруулна уу'
        elif User.objects.filter(email=email).exists():
                                             errors['email']     = 'Энэ и-мэйл бүртгэлтэй байна'
        if not password1:                    errors['password1'] = 'Нууц үг оруулна уу'
        elif len(password1) < 6:             errors['password1'] = 'Нууц үг хамгийн багадаа 6 тэмдэгт'
        elif password1 != password2:         errors['password2'] = 'Нууц үг таарахгүй байна'

        if not errors:
            username = email.split('@')[0]
            base, i = username, 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{i}'; i += 1
            user = User.objects.create_user(username=username, password=password1, email=email)
            login(request, user)
            return redirect('core:index')
    return render(request, 'user_register.html', {'errors': errors, 'form_data': request.POST})


def panel_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('core:panel_dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', '/panel/'))
        error = 'Нэвтрэх нэр эсвэл нууц үг буруу байна'

    return render(request, 'panel_login.html', {'error': error})


def panel_logout_view(request):
    logout(request)
    return redirect('core:panel_login')


@panel_required
def panel_dashboard(request):
    stats = {s[0]: Order.objects.filter(status=s[0]).count() for s in Order.STATUS_CHOICES}
    total_revenue = Order.objects.filter(
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(t=Sum('total_price'))['t'] or 0
    recent_orders = Order.objects.select_related('user').prefetch_related('items')[:8]

    context = {
        'stats':         stats,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'panel_dashboard.html', context)


@panel_required
def panel_orders(request):
    status_filter = request.GET.get('status', '')
    qs = Order.objects.select_related('user').prefetch_related('items')
    if status_filter:
        qs = qs.filter(status=status_filter)
    context = {
        'orders':         qs,
        'status_filter':  status_filter,
        'status_choices': Order.STATUS_CHOICES,
        'status_colors':  Order.STATUS_COLORS,
    }
    return render(request, 'panel_orders.html', context)


@panel_required
def panel_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Төлөв шинэчлэгдлээ → {order.get_status_display()}')
        return redirect('core:panel_order_detail', order_id=order_id)

    return render(request, 'panel_order_detail.html', {
        'order':          order,
        'status_choices': Order.STATUS_CHOICES,
        'status_colors':  Order.STATUS_COLORS,
    })
