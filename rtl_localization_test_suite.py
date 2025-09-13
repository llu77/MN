"""
نصوص اختبار RTL والتوطين العربي لنظام BarberTrack
مطور: RTL & Localization Testing Specialist
"""

import asyncio
import json
import logging
import re
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime
import unicodedata
from pathlib import Path

class RTLLocalizationTestSuite:
    """مجموعة اختبارات RTL والتوطين العربي"""

    def __init__(self, base_url: str = "http://localhost:9002"):
        self.base_url = base_url
        self.results = {
            'page_direction': {},
            'text_direction': {},
            'arabic_fonts': {},
            'arabic_numbers': {},
            'layout_alignment': {},
            'form_inputs': {},
            'navigation': {},
            'content_localization': {},
            'accessibility': {},
            'cultural_adaptation': {}
        }
        self.localization_issues = []
        self.rtl_score = 100
        self.test_timestamp = datetime.now()

        # إعداد التسجيل
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rtl_localization_test_results.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        # أنماط النصوص العربية
        self.arabic_patterns = {
            'basic': re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+'),
            'numbers': re.compile(r'[\u0660-\u0669]+'),
            'punctuation': re.compile(r'[\u0600-\u06FF]+[\u061B\u061F\u0621\u0640]+'),
            'diacritics': re.compile(r'[\u064B-\u065F]+')
        }

        # قائمة الكلمات العربية الشائعة في النظام
        self.arabic_keywords = [
            'الرئيسية', 'الإيرادات', 'المصروفات', 'البونص', 'الطلبات', 'تقارير',
            'رواتب', 'مخزون', 'إعدادات', 'موظفين', 'فرع', 'لعبان', 'طويق',
            'نظام', 'صالون', 'إدارة', 'مالية', 'حساب', 'بحث', 'طباعة',
            'تصدير', 'إضافة', 'تعديل', 'حذف', 'موافق', 'رفض', 'إلغاء',
            'تسجيل', 'دخول', 'خروج', 'بريد', 'كلمة', 'مرور', 'ملف',
            'شخصي', 'بيانات', 'تحميل', 'حفظ', 'إرسال', 'استلام'
        ]

    # ===========================
    # 1. اختبارات اتجاه الصفحة
    # ===========================

    async def test_page_direction(self, page: Page) -> Dict[str, Any]:
        """اختبار اتجاه الصفحة (RTL)"""
        print("📐 اختبار اتجاه الصفحة (RTL)...")

        direction_results = {
            'html_direction': False,
            'body_direction': False,
            'document_locale': False,
            'meta_tags': {},
            'css_direction': {},
            'inconsistencies': []
        }

        try:
            # اختبار جميع الصفحات الرئيسية
            pages_to_test = [
                {'name': 'الرئيسية', 'path': '/'},
                {'name': 'الإيرادات', 'path': '/revenue'},
                {'name': 'المصروفات', 'path': '/expenses'},
                {'name': 'البونص', 'path': '/bonuses'},
                {'name': 'الطلبات', 'path': '/requests'},
                {'name': 'تقارير', 'path': '/reports'},
                {'name': 'رواتب', 'path': '/payroll'},
                {'name': 'إعدادات', 'path': '/admin/settings'}
            ]

            page_directions = {}

            for page_info in pages_to_test:
                try:
                    await page.goto(f"{self.base_url}{page_info['path']}")
                    await page.wait_for_load_state("networkidle")

                    # التحقق من اتجاه HTML
                    html_dir = await page.evaluate("() => document.documentElement.dir")
                    body_dir = await page.evaluate("() => document.body.dir")

                    # التحقق من اللغة
                    html_lang = await page.evaluate("() => document.documentElement.lang")
                    meta_charset = await page.evaluate("""
                        () => {
                            const meta = document.querySelector('meta[charset]');
                            return meta ? meta.getAttribute('charset') : '';
                        }
                    """)

                    # التحقق من CSS direction
                    css_direction = await page.evaluate("""
                        () => {
                            const style = window.getComputedStyle(document.body);
                            return style.direction;
                        }
                    """)

                    page_result = {
                        'html_dir': html_dir,
                        'body_dir': body_dir,
                        'html_lang': html_lang,
                        'meta_charset': meta_charset,
                        'css_direction': css_direction,
                        'rtl_compliant': html_dir == 'rtl' and body_dir in ['rtl', '']
                    }

                    page_directions[page_info['name']] = page_result

                    # التحقق من التطابق
                    if not page_result['rtl_compliant']:
                        direction_results['inconsistencies'].append(
                            f"صفحة {page_info['name']}: اتجاه غير صحيح"
                        )

                except Exception as e:
                    direction_results['inconsistencies'].append(
                        f"خطأ في اختبار صفحة {page_info['name']}: {str(e)}"
                    )

            direction_results['page_directions'] = page_directions

            # حساب النتائج الإجمالية
            rtl_pages = sum(1 for page in page_directions.values() if page['rtl_compliant'])
            total_pages = len(page_directions)

            direction_results['html_direction'] = rtl_pages == total_pages
            direction_results['total_pages'] = total_pages
            direction_results['rtl_pages'] = rtl_pages

        except Exception as e:
            logging.error(f"Error testing page direction: {str(e)}")

        self.results['page_direction'] = direction_results
        return direction_results

    # ===========================
    # 2. اختبارات اتجاه النصوص
    # ===========================

    async def test_text_direction(self, page: Page) -> Dict[str, Any]:
        """اختبار اتجاه النصوص"""
        print("📝 اختبار اتجاه النصوص...")

        text_results = {
            'headings_rtl': False,
            'paragraphs_rtl': False,
            'labels_rtl': False,
            'buttons_rtl': False,
            'mixed_text_handling': False,
            'text_alignment': {},
            'font_families': {},
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # اختبار عناصر النص المختلفة
            text_elements = await page.evaluate("""
                () => {
                    const elements = {
                        headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')),
                        paragraphs: Array.from(document.querySelectorAll('p')),
                        labels: Array.from(document.querySelectorAll('label')),
                        buttons: Array.from(document.querySelectorAll('button')),
                        links: Array.from(document.querySelectorAll('a'))
                    };

                    const results = {};

                    Object.entries(elements).forEach(([type, elems]) => {
                        results[type] = elems.map(el => {
                            const style = window.getComputedStyle(el);
                            return {
                                text: el.textContent.trim(),
                                direction: style.direction,
                                textAlign: style.textAlign,
                                fontFamily: style.fontFamily,
                                hasArabic: /[\u0600-\u06FF]/.test(el.textContent)
                            };
                        }).filter(item => item.hasArabic);
                    });

                    return results;
                }
            """)

            # تحليل نتائج اتجاه النصوص
            for element_type, elements in text_elements.items():
                rtl_count = sum(1 for elem in elements if elem['direction'] == 'rtl')
                total_count = len(elements)

                if total_count > 0:
                    text_results['text_alignment'][element_type] = {
                        'total': total_count,
                        'rtl': rtl_count,
                        'percentage': (rtl_count / total_count) * 100,
                        'compliant': rtl_count / total_count >= 0.8  # 80% على الأقل
                    }

                    if rtl_count / total_count < 0.8:
                        text_results['issues'].append(
                            f"عناصر {element_type}: {(rtl_count / total_count) * 100:.1f}% RTL فقط"
                        )

            # اختبار التعامل مع النصوص المختلطة
            mixed_text_result = await self._test_mixed_text_handling(page)
            text_results['mixed_text_handling'] = mixed_text_result['passed']
            text_results['issues'].extend(mixed_text_result['issues'])

        except Exception as e:
            text_results['issues'].append(f"Error testing text direction: {str(e)}")
            logging.error(f"Error testing text direction: {str(e)}")

        self.results['text_direction'] = text_results
        return text_results

    async def _test_mixed_text_handling(self, page: Page) -> Dict[str, Any]:
        """اختبار التعامل مع النصوص المختلطة (عربي/إنجليزي)"""
        mixed_result = {
            'passed': True,
            'issues': []
        }

        try:
            # البحث عن نصوص مختلطة
            mixed_texts = await page.evaluate("""
                () => {
                    const allElements = document.querySelectorAll('*');
                    const mixedTexts = [];

                    allElements.forEach(el => {
                        const text = el.textContent.trim();
                        if (text && /[\u0600-\u06FF]/.test(text) && /[a-zA-Z]/.test(text)) {
                            const style = window.getComputedStyle(el);
                            mixedTexts.push({
                                text: text.substring(0, 50) + '...',
                                direction: style.direction,
                                textAlign: style.textAlign
                            });
                        }
                    });

                    return mixedTexts;
                }
            """)

            for text_info in mixed_texts:
                if text_info['direction'] != 'rtl':
                    mixed_result['passed'] = False
                    mixed_result['issues'].append(
                        f"نص مختلط غير RTL: {text_info['text']}"
                    )

        except Exception as e:
            mixed_result['issues'].append(f"Error testing mixed text: {str(e)}")

        return mixed_result

    # ===========================
    # 3. اختبارات الخطوط العربية
    # ===========================

    async def test_arabic_fonts(self, page: Page) -> Dict[str, Any]:
        """اختبار دعم الخطوط العربية"""
        print("🎨 اختبار دعم الخطوط العربية...")

        font_results = {
            'system_fonts': {},
            'web_fonts': {},
            'font_fallback': False,
            'rendering_quality': {},
            'character_coverage': {},
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # تحليل الخطوط المستخدمة
            font_analysis = await page.evaluate("""
                () => {
                    const allElements = document.querySelectorAll('*');
                    const fontUsage = {};
                    const arabicElements = [];

                    allElements.forEach(el => {
                        const text = el.textContent.trim();
                        if (text && /[\u0600-\u06FF]/.test(text)) {
                            const style = window.getComputedStyle(el);
                            const fontFamily = style.fontFamily;

                            if (!fontUsage[fontFamily]) {
                                fontUsage[fontFamily] = 0;
                            }
                            fontUsage[fontFamily]++;

                            arabicElements.push({
                                element: el.tagName,
                                fontFamily: fontFamily,
                                fontSize: style.fontSize,
                                fontWeight: style.fontWeight,
                                text: text.substring(0, 30)
                            });
                        }
                    });

                    return { fontUsage, arabicElements };
                }
            """)

            font_results['system_fonts'] = font_analysis['fontUsage']
            font_results['sample_elements'] = font_analysis['arabicElements']

            # التحقق من دعم الخطوط العربية
            for font_family, usage_count in font_analysis['fontUsage'].items():
                font_support = self._check_arabic_font_support(font_family)
                font_results['rendering_quality'][font_family] = {
                    'usage_count': usage_count,
                    'arabic_support': font_support['supported'],
                    'support_level': font_support['level']
                }

                if not font_support['supported']:
                    font_results['issues'].append(
                        f"الخط '{font_family}' لا يدعم العربية بشكل جيد"
                    )

            # اختبار تغطية الأحرف العربية
            char_coverage = await self._test_arabic_character_coverage(page)
            font_results['character_coverage'] = char_coverage

        except Exception as e:
            font_results['issues'].append(f"Error testing Arabic fonts: {str(e)}")
            logging.error(f"Error testing Arabic fonts: {str(e)}")

        self.results['arabic_fonts'] = font_results
        return font_results

    def _check_arabic_font_support(self, font_family: str) -> Dict[str, Any]:
        """التحقق من دعم الخط للأحرف العربية"""
        # قائمة الخطوط المعروفة بدعمها للعربية
        arabic_supporting_fonts = [
            'Tahoma', 'Arial Unicode MS', 'Times New Roman', 'Courier New',
            'Verdana', 'Georgia', 'Comic Sans MS', 'Impact', 'Lucida Console',
            'Trebuchet MS', 'Palatino Linotype', 'Garamond', 'Bookman Old Style',
            'Arial Black', 'Century Gothic'
        ]

        web_fonts_arabic = [
            'Amiri', 'Noto Sans Arabic', 'Noto Naskh Arabic', 'Droid Arabic',
            'GE SS Two', 'Helvetica Neue Arabic', 'Dubai', 'Cairo',
            'Kufam', 'Markazi Text', 'Harmattan', 'Scheherazade'
        ]

        font_lower = font_family.lower()

        support_level = 'none'
        if any(arabic_font.lower() in font_lower for arabic_font in arabic_supporting_fonts):
            support_level = 'basic'
        if any(arabic_font.lower() in font_lower for arabic_font in web_fonts_arabic):
            support_level = 'good'

        return {
            'supported': support_level != 'none',
            'level': support_level
        }

    async def _test_arabic_character_coverage(self, page: Page) -> Dict[str, Any]:
        """اختبار تغطية الأحرف العربية"""
        try:
            # جمع النصوص العربية من الصفحة
            arabic_text = await page.evaluate("""
                () => {
                    const allElements = document.querySelectorAll('*');
                    let arabicText = '';

                    allElements.forEach(el => {
                        const text = el.textContent;
                        if (text && /[\u0600-\u06FF]/.test(text)) {
                            arabicText += text + ' ';
                        }
                    });

                    return arabicText;
                }
            """)

            # تحليل الأحرف المستخدمة
            arabic_chars = set()
            for char in arabic_text:
                if '\u0600' <= char <= '\u06FF':
                    arabic_chars.add(char)

            # الأحرف العربية الأساسية المطلوبة
            required_chars = {
                'أ', 'إ', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س',
                'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن',
                'ه', 'و', 'ي', 'ى', 'ة', 'ء', 'آ', 'ؤ', 'ئ'
            }

            missing_chars = required_chars - arabic_chars

            return {
                'total_arabic_chars': len(arabic_chars),
                'required_chars': len(required_chars),
                'missing_chars': list(missing_chars),
                'coverage_percentage': (len(required_chars - missing_chars) / len(required_chars)) * 100
            }

        except Exception as e:
            return {'error': str(e)}

    # ===========================
    # 4. اختبارات الأرقام العربية
    # ===========================

    async def test_arabic_numbers(self, page: Page) -> Dict[str, Any]:
        """اختبار الأرقام العربية"""
        print("🔢 اختبار الأرقام العربية...")

        numbers_results = {
            'arabic_numerals_used': False,
            'western_numerals_used': False,
            'consistency': False,
            'currency_formatting': {},
            'number_formatting': {},
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # البحث عن الأرقام في الصفحة
            number_analysis = await page.evaluate("""
                () => {
                    const allElements = document.querySelectorAll('*');
                    const numbers = {
                        arabic: [],
                        western: [],
                        currency: [],
                        mixed: []
                    };

                    allElements.forEach(el => {
                        const text = el.textContent.trim();
                        if (text) {
                            // الأرقام العربية
                            const arabicMatches = text.match(/[\u0660-\u0669]+/g);
                            if (arabicMatches) {
                                numbers.arabic.push(...arabicMatches);
                            }

                            // الأرقام الغربية
                            const westernMatches = text.match(/\d+/g);
                            if (westernMatches) {
                                numbers.western.push(...westernMatches);
                            }

                            // العملة
                            const currencyMatches = text.match(/ر\.س\s*\d+/g);
                            if (currencyMatches) {
                                numbers.currency.push(...currencyMatches);
                            }
                        }
                    });

                    return numbers;
                }
            """)

            numbers_results['arabic_numerals_used'] = len(number_analysis['arabic']) > 0
            numbers_results['western_numerals_used'] = len(number_analysis['western']) > 0

            # التحقق من الاتساق
            if numbers_results['arabic_numerals_used'] and numbers_results['western_numerals_used']:
                numbers_results['consistency'] = False
                numbers_results['issues'].append(
                    "خلط بين الأرقام العربية والغربية في نفس الصفحة"
                )
            else:
                numbers_results['consistency'] = True

            # تحليل تنسيق العملة
            for currency in number_analysis['currency']:
                if not re.match(r'ر\.س\s*\d+', currency):
                    numbers_results['issues'].append(
                        f"تنسيق عملة غير صحيح: {currency}"
                    )

        except Exception as e:
            numbers_results['issues'].append(f"Error testing Arabic numbers: {str(e)}")
            logging.error(f"Error testing Arabic numbers: {str(e)}")

        self.results['arabic_numbers'] = numbers_results
        return numbers_results

    # ===========================
    # 5. اختبارات محاذاة التخطيط
    # ===========================

    async def test_layout_alignment(self, page: Page) -> Dict[str, Any]:
        """اختبار محاذاة التخطيط"""
        print("📏 اختبار محاذاة التخطيط...")

        layout_results = {
            'navigation_position': False,
            'sidebar_position': False,
            'content_alignment': False,
            'table_alignment': False,
            'form_alignment': False,
            'button_positions': {},
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # اختبار موقف التنقل
            nav_position = await page.evaluate("""
                () => {
                    const nav = document.querySelector('nav, [role="navigation"]');
                    if (!nav) return 'not_found';

                    const rect = nav.getBoundingClientRect();
                    const parentRect = nav.parentElement.getBoundingClientRect();
                    const isRightAligned = rect.left > parentRect.width / 2;

                    return {
                        position: isRightAligned ? 'right' : 'left',
                        element: nav.tagName,
                        hasArabic: /[\u0600-\u06FF]/.test(nav.textContent)
                    };
                }
            """)

            if nav_position['hasArabic'] and nav_position['position'] == 'right':
                layout_results['navigation_position'] = True
            elif nav_position['hasArabic']:
                layout_results['issues'].append(
                    f"التنقل {nav_position['element']} يجب أن يكون على اليمين"
                )

            # اختبار محاذاة الجداول
            table_alignment = await self._test_table_alignment(page)
            layout_results['table_alignment'] = table_alignment['aligned']
            layout_results['issues'].extend(table_alignment['issues'])

            # اختبار محاذاة النماذج
            form_alignment = await self._test_form_alignment(page)
            layout_results['form_alignment'] = form_alignment['aligned']
            layout_results['issues'].extend(form_alignment['issues'])

        except Exception as e:
            layout_results['issues'].append(f"Error testing layout alignment: {str(e)}")
            logging.error(f"Error testing layout alignment: {str(e)}")

        self.results['layout_alignment'] = layout_results
        return layout_results

    async def _test_table_alignment(self, page: Page) -> Dict[str, Any]:
        """اختبار محاذاة الجداول"""
        alignment_result = {
            'aligned': True,
            'issues': []
        }

        try:
            tables = await page.query_selector_all('table')

            for table in tables:
                table_analysis = await table.evaluate("""
                    (table) => {
                        const headers = table.querySelectorAll('th');
                        const rows = table.querySelectorAll('tr');

                        const hasArabicHeaders = Array.from(headers).some(th =>
                            /[\u0600-\u06FF]/.test(th.textContent)
                        );

                        if (!hasArabicHeaders) return { hasArabic: false };

                        // التحقق من اتجاه الجدول
                        const tableDir = table.dir || window.getComputedStyle(table).direction;

                        return {
                            hasArabic: true,
                            direction: tableDir,
                            headersCount: headers.length,
                            rowsCount: rows.length
                        };
                    }
                """)

                if table_analysis['hasArabic'] and table_analysis['direction'] != 'rtl':
                    alignment_result['aligned'] = False
                    alignment_result['issues'].append(
                        f"جدول عربي بدون اتجاه RTL"
                    )

        except Exception as e:
            alignment_result['issues'].append(f"Error testing table alignment: {str(e)}")

        return alignment_result

    async def _test_form_alignment(self, page: Page) -> Dict[str, Any]:
        """اختبار محاذاة النماذج"""
        alignment_result = {
            'aligned': True,
            'issues': []
        }

        try:
            forms = await page.query_selector_all('form')

            for form in forms:
                form_analysis = await form.evaluate("""
                    (form) => {
                        const labels = form.querySelectorAll('label');
                        const inputs = form.querySelectorAll('input, textarea, select');

                        const hasArabicLabels = Array.from(labels).some(label =>
                            /[\u0600-\u06FF]/.test(label.textContent)
                        );

                        if (!hasArabicLabels) return { hasArabic: false };

                        const formDir = form.dir || window.getComputedStyle(form).direction;

                        return {
                            hasArabic: true,
                            direction: formDir,
                            labelsCount: labels.length,
                            inputsCount: inputs.length
                        };
                    }
                """)

                if form_analysis['hasArabic'] and form_analysis['direction'] != 'rtl':
                    alignment_result['aligned'] = False
                    alignment_result['issues'].append(
                        f"نموذج عربي بدون اتجاه RTL"
                    )

        except Exception as e:
            alignment_result['issues'].append(f"Error testing form alignment: {str(e)}")

        return alignment_result

    # ===========================
    # 6. اختبارات التوطين المحتوى
    # ===========================

    async def test_content_localization(self, page: Page) -> Dict[str, Any]:
        """اختبار توطين المحتوى"""
        print("🌍 اختبار توطين المحتوى...")

        localization_results = {
            'arabic_content_percentage': 0,
            'key_terms_localized': False,
            'date_format_localized': False,
            'currency_format_localized': False,
            'error_messages_localized': False,
            'missing_translations': [],
            'quality_issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # تحليل المحتوى العربي
            content_analysis = await self._analyze_arabic_content(page)
            localization_results['arabic_content_percentage'] = content_analysis['percentage']

            # التحقق من توطين المصطلحات الرئيسية
            key_terms_result = await self._check_key_terms_localization(page)
            localization_results['key_terms_localized'] = key_terms_result['localized']
            localization_results['missing_translations'] = key_terms_result['missing']

            # اختبار تنسيق التواريخ
            date_format_result = await self._test_date_format_localization(page)
            localization_results['date_format_localized'] = date_format_result['localized']

            # اختبار تنسيق العملة
            currency_format_result = await self._test_currency_format_localization(page)
            localization_results['currency_format_localized'] = currency_format_result['localized']

        except Exception as e:
            localization_results['quality_issues'].append(f"Error testing content localization: {str(e)}")
            logging.error(f"Error testing content localization: {str(e)}")

        self.results['content_localization'] = localization_results
        return localization_results

    async def _analyze_arabic_content(self, page: Page) -> Dict[str, Any]:
        """تحليل المحتوى العربي"""
        try:
            content_analysis = await page.evaluate("""
                () => {
                    const allText = document.body.textContent;
                    const arabicText = allText.match(/[\u0600-\u06FF\s]+/g) || [];
                    const totalText = allText.length;
                    const arabicLength = arabicText.join('').length;

                    return {
                        totalText,
                        arabicLength,
                        percentage: totalText > 0 ? (arabicLength / totalText) * 100 : 0
                    };
                }
            """)

            return content_analysis

        except Exception as e:
            return {'error': str(e)}

    async def _check_key_terms_localization(self, page: Page) -> Dict[str, Any]:
        """التحقق من توطين المصطلحات الرئيسية"""
        missing_terms = []

        try:
            page_text = await page.evaluate("""
                () => document.body.textContent.toLowerCase()
            """)

            for term in self.arabic_keywords:
                if term not in page_text:
                    missing_terms.append(term)

            return {
                'localized': len(missing_terms) < len(self.arabic_keywords) * 0.2,  # 80% على الأقل
                'missing': missing_terms,
                'total_terms': len(self.arabic_keywords),
                'found_terms': len(self.arabic_keywords) - len(missing_terms)
            }

        except Exception as e:
            return {'error': str(e)}

    async def _test_date_format_localization(self, page: Page) -> Dict[str, Any]:
        """اختبار تنسيق التواريخ المحلي"""
        try:
            date_elements = await page.query_selector_all('[datetime], [data-date], .date, .time')

            localized_dates = 0
            total_dates = len(date_elements)

            for element in date_elements:
                date_text = await element.inner_text()
                # التحقق من استخدام تنسيق تاريخ عربي
                if any(arabic_month in date_text for arabic_month in ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']):
                    localized_dates += 1

            return {
                'localized': total_dates > 0 and localized_dates / total_dates >= 0.5,
                'localized_dates': localized_dates,
                'total_dates': total_dates
            }

        except Exception as e:
            return {'error': str(e)}

    async def _test_currency_format_localization(self, page: Page) -> Dict[str, Any]:
        """اختبار تنسيق العملة المحلي"""
        try:
            page_text = await page.evaluate("""
                () => document.body.textContent
            """)

            # البحث عن تنسيقات العملة السعودية
            riyal_formats = re.findall(r'ر\.س\s*\d+', page_text)
            sar_formats = re.findall(r'SAR\s*\d+', page_text)

            return {
                'localized': len(riyal_formats) > len(sar_formats),
                'riyal_formats': len(riyal_formats),
                'sar_formats': len(sar_formats)
            }

        except Exception as e:
            return {'error': str(e)}

    # ===========================
    # 7. اختبارات إمكانية الوصول
    # ===========================

    async def test_accessibility(self, page: Page) -> Dict[str, Any]:
        """اختبار إمكانية الوصول RTL"""
        print("♿ اختبار إمكانية الوصول RTL...")

        accessibility_results = {
            'aria_attributes': False,
            'keyboard_navigation': False,
            'screen_reader_compatibility': False,
            'color_contrast': False,
            'focus_management': False,
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            # اختبار خصائص ARIA
            aria_test = await self._test_aria_attributes(page)
            accessibility_results['aria_attributes'] = aria_test['passed']
            accessibility_results['issues'].extend(aria_test['issues'])

            # اختبار التنقل باللوحة المفاتيح
            keyboard_test = await self._test_keyboard_navigation(page)
            accessibility_results['keyboard_navigation'] = keyboard_test['passed']
            accessibility_results['issues'].extend(keyboard_test['issues'])

        except Exception as e:
            accessibility_results['issues'].append(f"Error testing accessibility: {str(e)}")
            logging.error(f"Error testing accessibility: {str(e)}")

        self.results['accessibility'] = accessibility_results
        return accessibility_results

    async def _test_aria_attributes(self, page: Page) -> Dict[str, Any]:
        """اختبار خصائص ARIA"""
        aria_result = {
            'passed': True,
            'issues': []
        }

        try:
            # التحقق من وجود ARIA labels للغة
            aria_elements = await page.query_selector_all('[aria-label], [aria-labelledby]')

            for element in aria_elements:
                aria_label = await element.get_attribute('aria-label')
                aria_labelledby = await element.get_attribute('aria-labelledby')

                if aria_label and not self.arabic_patterns['basic'].search(aria_label):
                    aria_result['issues'].append(
                        f"ARIA label غير عربي: {aria_label}"
                    )

        except Exception as e:
            aria_result['issues'].append(f"Error testing ARIA attributes: {str(e)}")

        return aria_result

    async def _test_keyboard_navigation(self, page: Page) -> Dict[str, Any]:
        """اختبار التنقل باللوحة المفاتيح"""
        keyboard_result = {
            'passed': True,
            'issues': []
        }

        try:
            # اختبار التركيز على العناصر القابلة للتركيز
            focusable_elements = await page.query_selector_all(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            )

            for i, element in enumerate(focusable_elements[:10]):  # اختبار أول 10 عناصر
                await element.focus()
                await page.wait_for_timeout(100)

                # التحقق من وجود تركيز
                is_focused = await element.evaluate("el => el === document.activeElement")
                if not is_focused:
                    keyboard_result['issues'].append(
                        f"العنصر {i+1} لا يقبل التركيز باللوحة المفاتيح"
                    )

        except Exception as e:
            keyboard_result['issues'].append(f"Error testing keyboard navigation: {str(e)}")

        return keyboard_result

    # ===========================
    # 8. اختبارات التكيف الثقافي
    # ===========================

    async def test_cultural_adaptation(self, page: Page) -> Dict[str, Any]:
        """اختبار التكيف الثقافي"""
        print("🏛️ اختبار التكيف الثقافي...")

        cultural_results = {
            'islamic_calendar': False,
            'prayer_times': False,
            'hijri_dates': False,
            'cultural_symbols': False,
            'local_business_terms': False,
            'issues': []
        }

        try:
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")

            page_text = await page.evaluate("""
                () => document.body.textContent
            """)

            # التحقق من المصطلحات الثقافية السعودية
            saudi_terms = ['السعودية', 'الرياض', 'جدة', 'مكة', 'المدينة', 'الدمام', 'الخبر']
            cultural_results['local_business_terms'] = any(term in page_text for term in saudi_terms)

            # التحقق من الأيام العربية
            arabic_days = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
            cultural_results['islamic_calendar'] = any(day in page_text for day in arabic_days)

        except Exception as e:
            cultural_results['issues'].append(f"Error testing cultural adaptation: {str(e)}")
            logging.error(f"Error testing cultural adaptation: {str(e)}")

        self.results['cultural_adaptation'] = cultural_results
        return cultural_results

    # ===========================
    # حساب النتيجة النهائية
    # ===========================

    def calculate_rtl_score(self) -> float:
        """حساب درجة RTL والتوطين"""
        score = 100
        penalties = 0

        # تقييم اتجاه الصفحة
        page_dir = self.results.get('page_direction', {})
        if not page_dir.get('html_direction', False):
            penalties += 25

        # تقييم اتجاه النصوص
        text_dir = self.results.get('text_direction', {})
        text_alignment = text_dir.get('text_alignment', {})
        for element_type, alignment_data in text_alignment.items():
            if alignment_data.get('compliant', False) == False:
                penalties += 5

        # تقييم الخطوط العربية
        arabic_fonts = self.results.get('arabic_fonts', {})
        rendering_quality = arabic_fonts.get('rendering_quality', {})
        for font, quality in rendering_quality.items():
            if not quality.get('arabic_support', False):
                penalties += 8

        # تقييم محاذاة التخطيط
        layout = self.results.get('layout_alignment', {})
        if not layout.get('navigation_position', False):
            penalties += 10
        if not layout.get('table_alignment', False):
            penalties += 8
        if not layout.get('form_alignment', False):
            penalties += 8

        # تقييم توطين المحتوى
        content = self.results.get('content_localization', {})
        if content.get('arabic_content_percentage', 0) < 80:
            penalties += 15
        if not content.get('key_terms_localized', False):
            penalties += 12
        if not content.get('currency_format_localized', False):
            penalties += 5

        # تقييم إمكانية الوصول
        accessibility = self.results.get('accessibility', {})
        if not accessibility.get('aria_attributes', False):
            penalties += 5
        if not accessibility.get('keyboard_navigation', False):
            penalties += 5

        self.rtl_score = max(0, score - penalties)
        return self.rtl_score

    # ===========================
    # تنفيذ الاختبارات الكاملة
    # ===========================

    async def run_rtl_localization_tests(self) -> Dict[str, Any]:
        """تنفيذ جميع اختبارات RTL والتوطين"""
        print("🚀 بدء اختبارات RTL والتوطين العربي...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            try:
                # 1. اختبارات اتجاه الصفحة
                await self.test_page_direction(page)

                # 2. اختبارات اتجاه النصوص
                await self.test_text_direction(page)

                # 3. اختبارات الخطوط العربية
                await self.test_arabic_fonts(page)

                # 4. اختبارات الأرقام العربية
                await self.test_arabic_numbers(page)

                # 5. اختبارات محاذاة التخطيط
                await self.test_layout_alignment(page)

                # 6. اختبارات توطين المحتوى
                await self.test_content_localization(page)

                # 7. اختبارات إمكانية الوصول
                await self.test_accessibility(page)

                # 8. اختبارات التكيف الثقافي
                await self.test_cultural_adaptation(page)

            finally:
                await browser.close()

        # حساب النتيجة النهائية
        final_score = self.calculate_rtl_score()

        # جمع جميع القضايا
        all_issues = []
        for category, results in self.results.items():
            if isinstance(results, dict) and 'issues' in results:
                all_issues.extend(results['issues'])

        self.localization_issues = all_issues

        # إنشاء تقرير RTL والتوطين
        rtl_report = self.generate_rtl_localization_report(final_score)

        return {
            'score': final_score,
            'results': self.results,
            'issues': all_issues,
            'report': rtl_report
        }

    def generate_rtl_localization_report(self, score: float) -> str:
        """إنشاء تقرير RTL والتوطين"""
        report = f"""
================================================================================
                       BARBERTRACK RTL & LOCALIZATION TEST REPORT
================================================================================
تاريخ الاختبار: {self.test_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
النظام: BarberTrack - نظام إدارة الصالونات متعددة الفروع
الهدف: تقييم دعم RTL والتوطين العربي

RTL & LOCALIZATION SCORE SUMMARY
─────────────────────────────────────────────────────────────────────────────
درجة التوطين: {score:.1f}/100
حالة التوطين: {'✅ ممتاز' if score >= 90 else '🟡 جيد' if score >= 70 else '🔴 يحتاج تحسين'}
عدد القضايا المكتشفة: {len(self.localization_issues)}

PAGE DIRECTION & LAYOUT
─────────────────────────────────────────────────────────────────────────────
"""

        page_dir = self.results.get('page_direction', {})
        report += f"""
HTML Direction (RTL): {'✅' if page_dir.get('html_direction', False) else '❌'}
Pages Tested: {page_dir.get('total_pages', 0)}
RTL Compliant Pages: {page_dir.get('rtl_pages', 0)}
"""

        layout = self.results.get('layout_alignment', {})
        report += f"""
Navigation Position (Right): {'✅' if layout.get('navigation_position', False) else '❌'}
Table Alignment (RTL): {'✅' if layout.get('table_alignment', False) else '❌'}
Form Alignment (RTL): {'✅' if layout.get('form_alignment', False) else '❌'}
"""

        report += f"""

TEXT & FONTS
─────────────────────────────────────────────────────────────────────────────
"""

        text_dir = self.results.get('text_direction', {})
        arabic_fonts = self.results.get('arabic_fonts', {})
        arabic_numbers = self.results.get('arabic_numbers', {})

        report += f"""
Text Direction (RTL): {'✅' if text_dir.get('headings_rtl', False) else '❌'}
Arabic Fonts Support: {'✅' if arabic_fonts else '❌'}
Arabic Numbers Used: {'✅' if arabic_numbers.get('arabic_numerals_used', False) else '❌'}
Consistent Number Format: {'✅' if arabic_numbers.get('consistency', False) else '❌'}
"""

        report += f"""

CONTENT LOCALIZATION
─────────────────────────────────────────────────────────────────────────────
"""

        content = self.results.get('content_localization', {})
        report += f"""
Arabic Content Percentage: {content.get('arabic_content_percentage', 0):.1f}%
Key Terms Localized: {'✅' if content.get('key_terms_localized', False) else '❌'}
Currency Format (ر.س): {'✅' if content.get('currency_format_localized', False) else '❌'}
Date Format Localized: {'✅' if content.get('date_format_localized', False) else '❌'}
"""

        report += f"""

ACCESSIBILITY & USABILITY
─────────────────────────────────────────────────────────────────────────────
"""

        accessibility = self.results.get('accessibility', {})
        cultural = self.results.get('cultural_adaptation', {})

        report += f"""
ARIA Attributes: {'✅' if accessibility.get('aria_attributes', False) else '❌'}
Keyboard Navigation: {'✅' if accessibility.get('keyboard_navigation', False) else '❌'}
Cultural Adaptation: {'✅' if cultural.get('local_business_terms', False) else '❌'}
Islamic Calendar Support: {'✅' if cultural.get('islamic_calendar', False) else '❌'}
"""

        report += f"""

DETAILED ISSUES
─────────────────────────────────────────────────────────────────────────────
"""

        if self.localization_issues:
            for i, issue in enumerate(self.localization_issues[:20], 1):  # أول 20 قضية
                report += f"{i:2d}. ⚠️ {issue}\n"
            if len(self.localization_issues) > 20:
                report += f"... و {len(self.localization_issues) - 20} قضية أخرى\n"
        else:
            report += "✅ لا توجد قضايا توطين\n"

        report += f"""

RTL & LOCALIZATION RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────

🎯 HIGH PRIORITY (48 ساعة)
"""

        high_priority = []
        if score < 70:
            high_priority.append("إصلاح اتجاه الصفحة الرئيسي (HTML dir='rtl')")
        if not page_dir.get('html_direction', False):
            high_priority.append("تعيين dir='rtl' لجميع صفحات النظام")
        if not arabic_numbers.get('consistency', False):
            high_priority.append("توحيد تنسيق الأرقام في جميع الصفحات")

        for rec in high_priority:
            report += f"   • {rec}\n"

        report += f"""

📈 MEDIUM PRIORITY (أسبوع)
"""
        medium_priority = [
            "تحسين دعم الخطوط العربية",
            "إضافة المزيد من خصائص ARIA للغة العربية",
            "تحسين محاذاة الجداول والنماذج",
            "توحيد تنسيق التواريخ والعملة"
        ]

        for rec in medium_priority:
            report += f"   • {rec}\n"

        report += f"""

🔧 LOW PRIORITY (شهر)
"""
        low_priority = [
            "إضافة دعم التقويم الهجري",
            "تحسين التكيف الثقافي السعودي",
            "إضافة المزيد من لغات واجهة المستخدم",
            "تحسين إمكانية الوصول للغة العربية"
        ]

        for rec in low_priority:
            report += f"   • {rec}\n"

        report += f"""

CONCLUSION
─────────────────────────────────────────────────────────────────────────────
{'✅ دعم RTL والتوطين ممتاز' if score >= 90 else '⚠️ الدعم جيد مع تحسينات طفيفة' if score >= 70 else '❌ يحتاج إلى تحسينات كبيرة'}

توصية النشر: {'النظام جاهز للنشر مع دعم RTL كامل' if score >= 85 else 'يجب تحسين دعم RTL قبل النشر'}

ملاحظة: تأكد من اختبار النظام على متصفحات مختلفة واجهات مختلفة
================================================================================
        """

        # حفظ التقرير
        report_path = 'test_results/rtl_localization_test_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

# نقطة الدخول الرئيسية
async def main():
    """نقطة الدخول الرئيسية"""
    print("🌐 نظام اختبار RTL والتوطين العربي لـ BarberTrack")
    print("=" * 50)

    rtl_tester = RTLLocalizationTestSuite()

    try:
        results = await rtl_tester.run_rtl_localization_tests()

        print(f"\n📊 درجة RTL والتوطين: {results['score']:.1f}/100")
        print(f"🌍 حالة التوطين: {'ممتاز' if results['score'] >= 90 else 'جيد' if results['score'] >= 70 else 'يحتاج تحسين'}")
        print(f"⚠️ عدد القضايا: {len(results['issues'])}")

        print(f"\n📋 التقرير الكامل متوفر في: test_results/rtl_localization_test_report.txt")

    except Exception as e:
        print(f"❌ خطأ في تنفيذ اختبارات RTL والتوطين: {str(e)}")
        logging.error(f"RTL localization test execution failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())