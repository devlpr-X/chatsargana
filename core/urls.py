from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ── Public pages ──────────────────────────────────────────
    path('',          views.index,    name='index'),
    path('info/',     views.info,     name='info'),
    path('products/', views.products, name='products'),
    path('benefits/', views.benefits, name='benefits'),
    path('about/',    views.about,    name='about'),

    # ── Cart ──────────────────────────────────────────────────
    path('cart/',                         views.cart_view,   name='cart'),
    path('cart/add/<int:product_id>/',    views.cart_add,    name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),

    # ── User auth ─────────────────────────────────────────────
    path('login/',                      views.user_login,             name='login'),
    path('logout/',                     views.user_logout,            name='logout'),
    path('register/',                   views.user_register,          name='register'),
    path('reset-password/',             views.password_reset_request, name='password_reset_request'),
    path('reset-password/confirm/',     views.password_reset_confirm, name='password_reset_confirm'),

    # ── Orders ────────────────────────────────────────────────
    path('checkout/',                     views.checkout,      name='checkout'),
    path('order/<int:order_id>/',         views.order_confirm, name='order_confirm'),
    path('my-orders/',                    views.my_orders,     name='my_orders'),

    # ── Admin panel ───────────────────────────────────────────
    path('panel/login/',                           views.panel_login_view,   name='panel_login'),
    path('panel/logout/',                          views.panel_logout_view,  name='panel_logout'),
    path('panel/',                                 views.panel_dashboard,    name='panel_dashboard'),
    path('panel/orders/',                          views.panel_orders,       name='panel_orders'),
    path('panel/orders/<int:order_id>/',           views.panel_order_detail, name='panel_order_detail'),

    # ── Inline edit API ───────────────────────────────────────
    path('panel/api/inline/',                      views.inline_edit,        name='inline_edit'),
]
