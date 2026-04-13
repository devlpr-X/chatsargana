import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# ─────────────────────────────────────────────────────────────
#  Site-wide editable text content  (key → value)
# ─────────────────────────────────────────────────────────────
class SiteContent(models.Model):
    key = models.CharField(max_length=120, unique=True, verbose_name="Түлхүүр")
    value = models.TextField(verbose_name="Утга")
    label = models.CharField(max_length=255, blank=True, verbose_name="Тайлбар (admin харуулах нэр)")

    class Meta:
        verbose_name = "Сайтын текст"
        verbose_name_plural = "Сайтын текстүүд"
        ordering = ['key']

    def __str__(self):
        return self.label or self.key


# ─────────────────────────────────────────────────────────────
#  Homepage — Hero stats  (7+, 190×, 100%)
# ─────────────────────────────────────────────────────────────
class HeroStat(models.Model):
    num = models.CharField(max_length=20, verbose_name="Тоо / утга")
    label = models.CharField(max_length=120, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Hero статистик"
        verbose_name_plural = "Hero статистикууд"
        ordering = ['order']

    def __str__(self):
        return f"{self.num} — {self.label}"


# ─────────────────────────────────────────────────────────────
#  Homepage — Features strip  (С витамин, Омега, …)
# ─────────────────────────────────────────────────────────────
class Feature(models.Model):
    icon = models.CharField(max_length=10, default='◈', verbose_name="Дүрс")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    description = models.CharField(max_length=255, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Онцлог (features strip)"
        verbose_name_plural = "Онцлогууд (features strip)"
        ordering = ['order']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
#  Homepage — About teaser cards  (190×, 🌿, Ω)
# ─────────────────────────────────────────────────────────────
class AboutCard(models.Model):
    TYPE_NUM  = 'num'
    TYPE_ICON = 'icon'
    TYPE_CHOICES = [(TYPE_NUM, 'Тоо'), (TYPE_ICON, 'Emoji дүрс')]

    card_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_NUM, verbose_name="Төрөл")
    value = models.CharField(max_length=20, verbose_name="Тоо эсвэл emoji")
    label = models.CharField(max_length=120, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "About тизер карт"
        verbose_name_plural = "About тизер картууд"
        ordering = ['order']

    def __str__(self):
        return f"{self.value} — {self.label}"


# ─────────────────────────────────────────────────────────────
#  Homepage — Benefits teaser  (4 small cards)
# ─────────────────────────────────────────────────────────────
class BenefitTeaser(models.Model):
    icon = models.CharField(max_length=10, verbose_name="Emoji дүрс")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    description = models.TextField(verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Ашиг тусын товч (нүүр хуудас)"
        verbose_name_plural = "Ашиг тусын товч картууд (нүүр хуудас)"
        ordering = ['order']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
#  Products
# ─────────────────────────────────────────────────────────────
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Нэр")
    slug = models.SlugField(unique=True, verbose_name="Slug (filter-д ашиглана)")

    class Meta:
        verbose_name = "Бүтээгдэхүүний ангилал"
        verbose_name_plural = "Бүтээгдэхүүний ангилалууд"

    def __str__(self):
        return self.name


class Product(models.Model):
    BADGE_CHOICES = [
        ('', 'Байхгүй'),
        ('bestseller', 'Bestseller'),
        ('premium', 'Premium'),
        ('new', 'Шинэ'),
    ]

    name = models.CharField(max_length=200, verbose_name="Нэр")
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Ангилал"
    )
    description = models.TextField(verbose_name="Тайлбар")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Үнэ (₮)")
    unit = models.CharField(max_length=50, verbose_name="Хэмжих нэгж (500мл, 50г …)")
    image = models.ImageField(upload_to='products/', verbose_name="Зураг")
    badge = models.CharField(
        max_length=20, choices=BADGE_CHOICES, blank=True, default='',
        verbose_name="Badge"
    )
    badge_icon = models.CharField(
        max_length=10, blank=True, verbose_name="Badge emoji (🏆, ⭐ …)"
    )
    nutrients = models.CharField(
        max_length=500, blank=True,
        verbose_name="Шим тэжээл (таслалаар тусгаарлана: С Витамин, Омега 3…)"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Онцлох бүтээгдэхүүн")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")
    is_active = models.BooleanField(default=True, verbose_name="Идэвхтэй")

    class Meta:
        verbose_name = "Бүтээгдэхүүн"
        verbose_name_plural = "Бүтээгдэхүүнүүд"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_nutrients_list(self):
        return [n.strip() for n in self.nutrients.split(',') if n.strip()]


# ─────────────────────────────────────────────────────────────
#  Info page — Nutrition cards
# ─────────────────────────────────────────────────────────────
class NutrientCard(models.Model):
    letter = models.CharField(max_length=5, verbose_name="Үсэг / тэмдэг (С, Е, Ω …)")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    value_text = models.CharField(max_length=120, verbose_name="Утга (695 мг/100г …)")
    note = models.CharField(max_length=255, verbose_name="Тэмдэглэл")
    bar_pct = models.PositiveSmallIntegerField(default=80, verbose_name="Мөрийн % (0-100)")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Шим тэжээлийн карт (Танилцуулга хуудас)"
        verbose_name_plural = "Шим тэжээлийн картууд"
        ordering = ['order']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
#  Info page — Usage cards
# ─────────────────────────────────────────────────────────────
class UsageCard(models.Model):
    icon = models.CharField(max_length=10, verbose_name="Emoji дүрс")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    description = models.CharField(max_length=255, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Хэрэглэх арга (Танилцуулга хуудас)"
        verbose_name_plural = "Хэрэглэх аргууд"
        ordering = ['order']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
#  Angiinfo page — Key numbers
# ─────────────────────────────────────────────────────────────
class KeyNumber(models.Model):
    num = models.CharField(max_length=20, verbose_name="Тоо / утга (190×, 70+ …)")
    label = models.CharField(max_length=120, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Түлхүүр тоо (Ашиг тус хуудас)"
        verbose_name_plural = "Түлхүүр тоонууд"
        ordering = ['order']

    def __str__(self):
        return f"{self.num} — {self.label}"


# ─────────────────────────────────────────────────────────────
#  Angiinfo page — Detailed benefit rows
# ─────────────────────────────────────────────────────────────
class BenefitDetail(models.Model):
    icon = models.CharField(max_length=10, verbose_name="Emoji дүрс")
    number = models.CharField(max_length=5, verbose_name="Дугаар (01, 02 …)")
    title = models.CharField(max_length=200, verbose_name="Гарчиг")
    description = models.TextField(verbose_name="Тайлбар")
    tags = models.CharField(
        max_length=500, blank=True,
        verbose_name="Тэгүүд (таслалаар: С Витамин, Иммун систем …)"
    )
    is_reverse = models.BooleanField(default=False, verbose_name="Байрлал урвуу (тийм = зураг баруун талд)")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Дэлгэрэнгүй ашиг тус (Ашиг тус хуудас)"
        verbose_name_plural = "Дэлгэрэнгүй ашиг тусууд"
        ordering = ['order']

    def __str__(self):
        return f"{self.number}. {self.title}"

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


# ─────────────────────────────────────────────────────────────
#  Orders
# ─────────────────────────────────────────────────────────────
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Хүлээгдэж буй'),
        ('confirmed', 'Баталгаажсан'),
        ('shipped',   'Хүргэлтэнд'),
        ('delivered', 'Хүргэгдсэн'),
        ('cancelled', 'Цуцлагдсан'),
    ]
    STATUS_COLORS = {
        'pending':   '#f59e0b',
        'confirmed': '#3b82f6',
        'shipped':   '#8b5cf6',
        'delivered': '#22c55e',
        'cancelled': '#ef4444',
    }

    user           = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Хэрэглэгч")
    session_key    = models.CharField(max_length=40, blank=True, verbose_name="Сессийн түлхүүр")
    customer_name  = models.CharField(max_length=200, verbose_name="Нэр")
    customer_phone = models.CharField(max_length=20, verbose_name="Утасны дугаар")
    customer_email = models.EmailField(blank=True, verbose_name="И-мэйл")
    address        = models.TextField(verbose_name="Хаяг")
    latitude       = models.FloatField(null=True, blank=True, verbose_name="Өргөрөг")
    longitude      = models.FloatField(null=True, blank=True, verbose_name="Уртраг")
    note           = models.TextField(blank=True, verbose_name="Нэмэлт тайлбар")
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Төлөв")
    total_price    = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Нийт үнэ (₮)")
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name="Огноо")
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Захиалга"
        verbose_name_plural = "Захиалгууд"
        ordering            = ['-created_at']

    def __str__(self):
        return f"#{self.pk} — {self.customer_name} ({self.get_status_display()})"

    def status_color(self):
        return self.STATUS_COLORS.get(self.status, '#6b7280')


# ─────────────────────────────────────────────────────────────
#  Password reset tokens
# ─────────────────────────────────────────────────────────────
class PasswordResetToken(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Хэрэглэгч")
    token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used       = models.BooleanField(default=False)

    class Meta:
        verbose_name        = "Нууц үг сэргээх токен"
        verbose_name_plural = "Нууц үг сэргээх токенүүд"

    def __str__(self):
        return f"{self.user.email} — {'ашигласан' if self.used else 'хүчинтэй'}"

    def is_valid(self):
        return not self.used and (timezone.now() - self.created_at) < timedelta(hours=1)


class OrderItem(models.Model):
    order        = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Бүтээгдэхүүн")
    product_name = models.CharField(max_length=200, verbose_name="Нэр")
    quantity     = models.PositiveIntegerField(default=1, verbose_name="Тоо ширхэг")
    price        = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Нэгжийн үнэ (₮)")

    class Meta:
        verbose_name        = "Захиалгын зүйл"
        verbose_name_plural = "Захиалгын зүйлс"

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity


# ─────────────────────────────────────────────────────────────
#  About page — Mission values
# ─────────────────────────────────────────────────────────────
class MissionValue(models.Model):
    icon = models.CharField(max_length=10, verbose_name="Emoji дүрс")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    description = models.CharField(max_length=255, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Эрхэм зорилгын утга (Бидний тухай)"
        verbose_name_plural = "Эрхэм зорилгын утгууд"
        ordering = ['order']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
#  About page — Production process steps
# ─────────────────────────────────────────────────────────────
class ProcessStep(models.Model):
    number = models.CharField(max_length=5, verbose_name="Дугаар (01, 02 …)")
    icon = models.CharField(max_length=10, verbose_name="Emoji дүрс")
    title = models.CharField(max_length=120, verbose_name="Гарчиг")
    description = models.CharField(max_length=255, verbose_name="Тайлбар")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Дараалал")

    class Meta:
        verbose_name = "Үйлдвэрлэлийн алхам (Бидний тухай)"
        verbose_name_plural = "Үйлдвэрлэлийн алхамууд"
        ordering = ['order']

    def __str__(self):
        return f"{self.number}. {self.title}"
