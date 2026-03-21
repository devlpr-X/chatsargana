# Чацаргана — Вебсайтын бүтэц

## Файлын бүтэц

```
Chatsargana/
│
├── index.html          ← Нүүр хуудас (Home)
├── info.html           ← Танилцуулга хуудас
├── comic.html          ← Бүтээгдэхүүн хуудас
├── angiinfo.html       ← Ашиг тус хуудас
├── about.html          ← Бидний тухай хуудас
│
├── global.css          ← Бүх хуудасны нийтлэг стиль (header, footer, shared)
├── style.css           ← index.html-ийн стиль (hero, products preview, etc.)
├── info.css            ← info.html-ийн стиль
├── comic.css           ← comic.html-ийн стиль
├── angiinfo.css        ← angiinfo.html-ийн стиль
├── about.css           ← about.html-ийн стиль
│
├── main.js             ← Бүх хуудасны нийтлэг JS
│                          (header scroll, mobile nav, reveal animations)
├── comic.js            ← Бүтээгдэхүүн шүүлтийн JS (filter by category)
│
└── images/             ← Зурагны хавтас (хуучнаас хэвлэнэ)
    ├── product1.png    — Цэвэр шүүс
    ├── product2.png    — Сироп
    ├── product3.png    — Тос ⭐ (Hero-д ашигладаг)
    ├── product4.png    — Цай
    ├── product5.png    — Чанамал
    ├── chatsargana1.jpg — Капсул
    └── chatsargana2.jpg — Арьс арчилгаа
```

## Дизайн системийн өнгийн палитр

| Хувьсагч        | Утга        | Хэрэглээ                    |
|-----------------|-------------|------------------------------|
| `--forest`      | `#0a1a0a`   | Ерөнхий дэвсгэр             |
| `--forest-mid`  | `#122612`   | Карт, талбайн дэвсгэр       |
| `--leaf`        | `#1e4020`   | Hover, идэвхтэй элемент     |
| `--sage`        | `#4a7c59`   | Tag, badge, дэд өнгө        |
| `--amber`       | `#e87c0c`   | Үндсэн акцент өнгө          |
| `--amber-lt`    | `#f5a73b`   | Italic текст, тоо           |
| `--gold`        | `#c8921a`   | Тусгай элемент              |
| `--cream`       | `#fdf6ec`   | Үндсэн текст                |

## Хуудас бүрийн тайлбар

### index.html (Нүүр)
- Immersive hero with 3D floating product orbit
- Features strip (С витамин, Омега, etc.)
- About teaser with animated cards
- 4-column products preview grid
- Benefits teaser section
- Full footer

### info.html (Танилцуулга)
- Page hero with large title
- Story section with image frame
- Nutrition grid (6 nutrient cards with animated progress bars)
- Usage section (4 ways to use)
- CTA to products

### comic.html (Бүтээгдэхүүн)
- Page hero
- Filter tabs (Бүгд / Ундаа / Тос / Арьс арчилгаа / Нэмэлт)
- 2-column product grid with:
  - Featured product (spans full width)
  - Category tags, nutrient badges
  - Favorite button
- Quality assurance banner

### angiinfo.html (Ашиг тус)
- Full-height hero with dot pattern
- Key numbers strip (190×, 70+, 4, 100%)
- 6 benefit rows with alternating layout
- Each benefit: icon, number, title, description, tags
- CTA section

### about.html (Бидний тухай)
- Large typographic hero
- Mission section with values
- Production process (5 steps)
- Contact grid (4 cards)
- Footer

## Техникийн онцлог

- **Фонт**: Cormorant Garamond (display) + DM Sans (body)
- **CSS Variables**: global.css-д тодорхойлсон, бүх хуудас ашиглана
- **Animations**: CSS keyframes + IntersectionObserver
- **Responsive**: 1400px / 1024px / 768px / 480px breakpoints
- **Scroll reveal**: `.reveal` class + `visible` toggle
- **Mobile nav**: Hamburger menu with full-screen overlay
- **Scroll progress**: Amber-colored thin bar at top

## Хэрхэн ажиллуулах

1. `images/` хавтаст зурагнуудаа оруулна
2. Хөтөч дээр `index.html` нээнэ
3. Тусгай сервер шаардахгүй — зүгээр HTML/CSS/JS

## Хуучин файлуудтай ялгаа

| Хуучин              | Шинэ                          |
|---------------------|-------------------------------|
| `1.css`             | `info.css` болж нэрлэгдсэн   |
| `comic.css`         | Бүрэн дахин бичсэн           |
| `about.css`         | Бүрэн дахин бичсэн           |
| `angiinfo.css`      | Бүрэн дахин бичсэн           |
| `info.js`           | `main.js` + `comic.js`-д нэгтгэгдсэн |
| _(байхгүй)_         | `global.css` нэмэгдсэн       |
| _(байхгүй)_         | `main.js` нэмэгдсэн          |
