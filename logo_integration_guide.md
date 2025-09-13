# دليل تكامل شعار سهل

## نظرة عامة
هذا الدليل يشرح كيفية استخدام شعار سهل في جميع واجهات المشروع.

## رابط الشعار
الرابط الأساسي للشعار: https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing

## متغيرات الشعار
- Header: 180 × 54 بكسل
- Sidebar: 150 × 45 بكسل
- Footer: 120 × 36 بكسل
- Mobile: 140 × 42 بكسل
- Print: 200 × 60 بكسل

## طريقة الاستخدام في HTML
```html
<!-- شعار الرأسية -->
<img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
     alt="سهل Logo"
     width="180" height="54"
     class="logo-header"
     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
<div class="logo-fallback" style="display: none;">
    <svg width="180" height="54" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
        <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">BARBERTRACK</text>
    </svg>
</div>
```

## طريقة الاستخدام في React
```jsx
import سهلLogo from './components/logo/سهلLogo';

// في الصفحة الرئيسية
<سهلLogo variant="header" />

// في الشريط الجانبي
<سهلLogo variant="sidebar" />

// في التذييل
<سهلLogo variant="footer" />
```

## الألوان التجارية
- Primary: #1E3DA8
- Secondary: #FF6B6B
- Accent: #4ECDC4
- Dark: #2C3E50
- Light: #ECF0F1

## دعم RTL
المكونات تدعم اتجاه RTL بشكل كامل.

## اختبار الشعار
افتح ملف logo_test_page.html في المتصفح لاختبار جميع متغيرات الشعار.

## ملاحظات هامة
1. استخدم دائماً نص بديل (alt text) للشعار
2. تأكد من وجود Fallback في حال فشل تحميل الصورة
3. اختبر الشعار على جميع الأجهزة والمتصفحات
4. استخدم الأحجام المناسبة لكل مكان في الواجهة
