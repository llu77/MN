"""
تكامل شعار سهل في واجهات الاختبار
مطور: Full-stack Testing Engineer
"""

from pathlib import Path

def create_logo_test_page():
    """إنشاء صفحة اختبار الشعار"""

    html_content = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سهل - اختبار الشعار</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; direction: rtl; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #1E3DA8 0%, #2c5aa0 100%); color: white; padding: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header-content { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
        .logo-container { display: flex; align-items: center; gap: 1rem; }
        .logo { height: 54px; width: auto; transition: all 0.3s ease; }
        .logo:hover { transform: scale(1.05); }
        .logo-text { font-size: 1.5rem; font-weight: bold; color: white; }
        .test-section { background: white; margin: 2rem 0; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .section-title { color: #1E3DA8; margin-bottom: 1.5rem; font-size: 1.5rem; border-bottom: 2px solid #1E3DA8; padding-bottom: 0.5rem; }
        .logo-variants { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 2rem 0; }
        .variant-card { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; text-align: center; border: 2px solid transparent; transition: all 0.3s ease; }
        .variant-card:hover { border-color: #1E3DA8; transform: translateY(-2px); }
        .variant-logo { margin-bottom: 1rem; }
        .variant-name { font-weight: bold; color: #2C3E50; margin-bottom: 0.5rem; }
        .variant-size { font-size: 0.9rem; color: #666; }
        .footer { background: #2C3E50; color: white; text-align: center; padding: 2rem 0; margin-top: 3rem; }
        .footer-logo { height: 36px; margin-bottom: 1rem; }
        @media (max-width: 768px) { .header-content { flex-direction: column; gap: 1rem; } .logo-variants { grid-template-columns: 1fr; } .logo { height: 42px; } }
    </style>
</head>
<body>
    <!-- Header with Logo -->
    <header class="header">
        <div class="header-content">
            <div class="logo-container">
                <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
                     alt="سهل Logo"
                     class="logo"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                <div class="logo-fallback" style="display: none;">
                    <svg width="180" height="54" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                        <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">سهل</text>
                    </svg>
                </div>
                <div class="logo-text">نظام إدارة الصالونات متعددة الفروع</div>
            </div>
            <div class="header-nav">
                <nav>اختبار الشعار</nav>
            </div>
        </div>
    </header>

    <div class="container">
        <!-- Logo Variants Test -->
        <div class="test-section">
            <h2 class="section-title">متغيرات الشعار</h2>
            <div class="logo-variants">
                <!-- Header Logo -->
                <div class="variant-card">
                    <div class="variant-logo">
                        <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
                             alt="Header Logo"
                             width="180" height="54"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <div class="logo-fallback" style="display: none;">
                            <svg width="180" height="54" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                                <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">سهل</text>
                            </svg>
                        </div>
                    </div>
                    <div class="variant-name">Header Logo</div>
                    <div class="variant-size">180 × 54</div>
                </div>

                <!-- Sidebar Logo -->
                <div class="variant-card">
                    <div class="variant-logo">
                        <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
                             alt="Sidebar Logo"
                             width="150" height="45"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <div class="logo-fallback" style="display: none;">
                            <svg width="150" height="45" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                                <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">سهل</text>
                            </svg>
                        </div>
                    </div>
                    <div class="variant-name">Sidebar Logo</div>
                    <div class="variant-size">150 × 45</div>
                </div>

                <!-- Footer Logo -->
                <div class="variant-card">
                    <div class="variant-logo">
                        <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
                             alt="Footer Logo"
                             width="120" height="36"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <div class="logo-fallback" style="display: none;">
                            <svg width="120" height="36" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                                <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">سهل</text>
                            </svg>
                        </div>
                    </div>
                    <div class="variant-name">Footer Logo</div>
                    <div class="variant-size">120 × 36</div>
                </div>

                <!-- Mobile Logo -->
                <div class="variant-card">
                    <div class="variant-logo">
                        <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
                             alt="Mobile Logo"
                             width="140" height="42"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <div class="logo-fallback" style="display: none;">
                            <svg width="140" height="42" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                                <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">سهل</text>
                            </svg>
                        </div>
                    </div>
                    <div class="variant-name">Mobile Logo</div>
                    <div class="variant-size">140 × 42</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer with Logo -->
    <footer class="footer">
        <img src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
             alt="سهل Footer Logo"
             class="footer-logo"
             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
        <div class="logo-fallback" style="display: none;">
            <svg width="120" height="36" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="60" rx="10" fill="#1E3DA8"/>
                <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">BARBERTRACK</text>
            </svg>
        </div>
        <p>2024 سهل. نظام إدارة الصالونات متعددة الفروع. جميع الحقوق محفوظة.</p>
    </footer>
</body>
</html>'''

    # Save the test page
    test_page_path = Path("logo_test_page.html")
    with open(test_page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Created logo test page: {test_page_path}")
    return test_page_path

def create_logo_components():
    """إنشاء مكونات الشعار"""

    # Main logo component
    logo_component = '''
import React from 'react';
import './Logo.css';

const سهلLogo = ({ variant = 'header', className = '', ...props }) => {
  const variants = {
    header: { width: 180, height: 54, class: 'logo-header' },
    sidebar: { width: 150, height: 45, class: 'logo-sidebar' },
    footer: { width: 120, height: 36, class: 'logo-footer' },
    mobile: { width: 140, height: 42, class: 'logo-mobile' },
    print: { width: 200, height: 60, class: 'logo-print' }
  };

  const config = variants[variant] || variants.header;

  return (
    <img
      src="https://drive.google.com/file/d/1R3agKnUEBr9WMGrbiiJ0m7Pt92IYL9dq/view?usp=sharing"
      alt="سهل - نظام إدارة الصالونات متعددة الفروع"
      width={config.width}
      height={config.height}
      className={`logo ${config.class} ${className}`}
      {...props}
    />
  );
};

export default سهلLogo;
'''

    # CSS styles
    css_styles = '''
/* سهل Logo Styles */
.logo {
  display: inline-block;
  transition: all 0.3s ease;
  cursor: pointer;
  user-select: none;
}

.logo:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}

.logo-header {
  margin: 0 auto;
  display: block;
}

.logo-sidebar {
  margin-bottom: 2rem;
}

.logo-footer {
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.logo-footer:hover {
  opacity: 1;
}

.logo-mobile {
  max-width: 100%;
  height: auto;
}

.logo-print {
  filter: grayscale(100%);
}

/* Responsive Logo Styles */
@media (max-width: 768px) {
  .logo-header {
    width: 140px !important;
    height: 42px !important;
  }
}

@media (max-width: 480px) {
  .logo-header {
    width: 120px !important;
    height: 36px !important;
  }
}

/* RTL Support */
[dir="rtl"] .logo-with-text {
  flex-direction: row-reverse;
}
'''

    # Create components directory
    components_dir = Path("src/components/logo")
    components_dir.mkdir(parents=True, exist_ok=True)

    # Save logo component
    logo_path = components_dir / "سهلLogo.js"
    with open(logo_path, 'w', encoding='utf-8') as f:
        f.write(logo_component)

    # Save CSS styles
    styles_dir = Path("src/styles")
    styles_dir.mkdir(parents=True, exist_ok=True)
    css_path = styles_dir / "logo.css"
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_styles)

    print(f"Created logo components:")
    print(f"  - {logo_path}")
    print(f"  - {css_path}")

def create_integration_guide():
    """إنشاء دليل التكامل"""

    guide_content = '''# دليل تكامل شعار سهل

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
'''

    guide_path = Path("logo_integration_guide.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"Created integration guide: {guide_path}")

def main():
    """الدالة الرئيسية"""
    print("Starting سهل Logo Integration...")

    # Create test page
    test_page = create_logo_test_page()

    # Create React components
    create_logo_components()

    # Create integration guide
    create_integration_guide()

    print("\nLogo integration completed successfully!")
    print("\nFiles created:")
    print("  - logo_test_page.html (Test page)")
    print("  - src/components/logo/سهلLogo.js (React component)")
    print("  - src/styles/logo.css (Styles)")
    print("  - logo_integration_guide.md (Documentation)")

    print("\nNext steps:")
    print("1. Open logo_test_page.html in your browser to test the logo")
    print("2. Copy the React components to your project")
    print("3. Update all pages to use the سهل logo")
    print("4. Test the logo on different devices and browsers")

if __name__ == "__main__":
    main()