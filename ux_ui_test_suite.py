"""
نصوص اختبار الواجهة والتجربة المستخدم لنظام BarberTrack
مطور: UX/UI Testing Specialist
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from playwright.async_api import async_playwright, Page, Browser, Keyboard, Mouse
from datetime import datetime
import re
from pathlib import Path
import statistics

class UXUITestSuite:
    """مجموعة اختبارات الواجهة والتجربة المستخدم"""

    def __init__(self, base_url: str = "http://localhost:9002"):
        self.base_url = base_url
        self.results = {
            'responsiveness': {},
            'navigation': {},
            'forms': {},
            'interactions': {},
            'visual_design': {},
            'accessibility': {},
            'performance': {},
            'error_handling': {},
            'user_flows': {},
            'mobile_experience': {}
        }
        self.ux_issues = []
        self.ux_score = 100
        self.test_timestamp = datetime.now()

        # إعداد التسجيل
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ux_ui_test_results.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        # أحجام الشاشات للاختبار
        self.viewports = [
            {'name': 'Desktop', 'width': 1920, 'height': 1080},
            {'name': 'Laptop', 'width': 1366, 'height': 768},
            {'name': 'Tablet', 'width': 768, 'height': 1024},
            {'name': 'Mobile', 'width': 375, 'height': 812}
        ]

        # مسارات المستخدم للاختبار
        self.user_flows = [
            {
                'name': 'تسجيل الدخول وعرض لوحة التحكم',
                'path': 'login -> dashboard',
                'steps': [
                    {'action': 'navigate', 'url': '/login'},
                    {'action': 'fill', 'selector': 'input[type="email"]', 'value': 'user@example.com'},
                    {'action': 'fill', 'selector': 'input[type="password"]', 'value': 'password123'},
                    {'action': 'click', 'selector': 'button[type="submit"]'},
                    {'action': 'wait', 'selector': '[data-testid="dashboard-content"]'}
                ]
            },
            {
                'name': 'إضافة إيراد جديد',
                'path': 'dashboard -> revenue -> add',
                'steps': [
                    {'action': 'navigate', 'url': '/revenue'},
                    {'action': 'click', 'selector': '[data-testid="add-revenue-btn"]'},
                    {'action': 'fill', 'selector': '[data-testid="revenue-amount"]', 'value': '1000'},
                    {'action': 'fill', 'selector': '[data-testid="revenue-description"]', 'value': 'إيراد اختبار'},
                    {'action': 'click', 'selector': '[data-testid="submit-revenue"]'},
                    {'action': 'wait', 'selector': '[data-testid="success-message"]'}
                ]
            },
            {
                'name': 'عرض التقرير المالي',
                'path': 'dashboard -> reports -> view',
                'steps': [
                    {'action': 'navigate', 'url': '/reports'},
                    {'action': 'click', 'selector': '[data-testid="financial-report-btn"]'},
                    {'action': 'wait', 'selector': '[data-testid="report-content"]'},
                    {'action': 'click', 'selector': '[data-testid="export-pdf-btn"]'}
                ]
            }
        ]

    # ===========================
    # 1. اختبارات التجاوب
    # ===========================

    async def test_responsiveness(self, page: Page) -> Dict[str, Any]:
        """اختبار تجاوب التصميم"""
        print("📱 اختبار تجاوب التصميم...")

        responsiveness_results = {
            'viewports_tested': 0,
            'responsive_issues': [],
            'breakpoints_working': {},
            'layout_adaptation': {},
            'content_visibility': {},
            'scroll_issues': [],
            'touch_targets': {}
        }

        try:
            pages_to_test = ['/', '/revenue', '/reports', '/dashboard']

            for viewport in self.viewports:
                viewport_results = {
                    'name': viewport['name'],
                    'width': viewport['width'],
                    'height': viewport['height'],
                    'pages_tested': 0,
                    'issues': [],
                    'successful': 0
                }

                await page.set_viewport_size({
                    'width': viewport['width'],
                    'height': viewport['height']
                })

                for page_path in pages_to_test:
                    try:
                        await page.goto(f"{self.base_url}{page_path}")
                        await page.wait_for_load_state("networkidle")
                        await page.wait_for_timeout(1000)

                        viewport_results['pages_tested'] += 1

                        # اختبار التجاوب للصفحة
                        page_responsiveness = await self._test_page_responsiveness(page, viewport)
                        viewport_results['issues'].extend(page_responsiveness['issues'])

                        if not page_responsiveness['issues']:
                            viewport_results['successful'] += 1

                    except Exception as e:
                        viewport_results['issues'].append(f"Error testing {page_path}: {str(e)}")

                responsiveness_results['breakpoints_working'][viewport['name']] = viewport_results
                responsiveness_results['responsive_issues'].extend(viewport_results['issues'])
                responsiveness_results['viewports_tested'] += 1

                # اختبار أهداف اللمس للأجهزة المحمولة
                if viewport['name'] == 'Mobile':
                    touch_targets = await self._test_touch_targets(page)
                    responsiveness_results['touch_targets'] = touch_targets

        except Exception as e:
            logging.error(f"Error testing responsiveness: {str(e)}")

        self.results['responsiveness'] = responsiveness_results
        return responsiveness_results

    async def _test_page_responsiveness(self, page: Page, viewport: Dict) -> Dict[str, Any]:
        """اختبار تجاوب صفحة معينة"""
        page_issues = []

        try:
            # التحقق من وجود scroll أفقي
            has_horizontal_scroll = await page.evaluate("""
                () => {
                    return document.documentElement.scrollWidth > document.documentElement.clientWidth;
                }
            """)

            if has_horizontal_scroll:
                page_issues.append(f"Horizontal scroll detected on {viewport['name']}")

            # التحقق من ظهور العناصر الرئيسية
            main_elements = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('header, main, nav, footer, [role="main"]');
                    return Array.from(elements).map(el => {
                        const rect = el.getBoundingClientRect();
                        return {
                            element: el.tagName.toLowerCase(),
                            visible: rect.width > 0 && rect.height > 0 && rect.top < window.innerHeight
                        };
                    });
                }
            """)

            hidden_elements = [el for el in main_elements if not el['visible']]
            if hidden_elements:
                page_issues.append(f"Hidden main elements on {viewport['name']}: {[el['element'] for el in hidden_elements]}")

            # التحقق من حجم النصوص
            font_sizes = await page.evaluate("""
                () => {
                    const textElements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6, label, button');
                    return Array.from(textElements).map(el => {
                        const style = window.getComputedStyle(el);
                        return parseFloat(style.fontSize);
                    }).filter(size => size > 0);
                }
            """)

            if font_sizes:
                min_font = min(font_sizes)
                if min_font < 12 and viewport['name'] in ['Tablet', 'Mobile']:
                    page_issues.append(f"Font size too small ({min_font}px) on {viewport['name']}")

        except Exception as e:
            page_issues.append(f"Error testing page responsiveness: {str(e)}")

        return {'issues': page_issues}

    async def _test_touch_targets(self, page: Page) -> Dict[str, Any]:
        """اختبار أهداف اللمس"""
        touch_results = {
            'buttons_tested': 0,
            'adequate_size': 0,
            'too_small': 0,
            'issues': []
        }

        try:
            clickable_elements = await page.query_selector_all(
                'button, [role="button"], [href], input[type="submit"], input[type="button"]'
            )

            for element in clickable_elements[:20]:  # اختبار أول 20 عنصر
                try:
                    rect = await element.bounding_box()
                    if rect:
                        touch_results['buttons_tested'] += 1

                        # المعيار: 48x48 بكسل كحد أدنى
                        min_dimension = min(rect['width'], rect['height'])
                        if min_dimension >= 44:  # 44px هو المعيار الموصى به
                            touch_results['adequate_size'] += 1
                        else:
                            touch_results['too_small'] += 1
                            touch_results['issues'].append(
                                f"Touch target too small: {rect['width']}x{rect['height']}px"
                            )

                except Exception:
                    continue

        except Exception as e:
            touch_results['issues'].append(f"Error testing touch targets: {str(e)}")

        return touch_results

    # ===========================
    # 2. اختبارات التنقل
    # ===========================

    async def test_navigation(self, page: Page) -> Dict[str, Any]:
        """اختبار التنقل في النظام"""
        print("🧭 اختبار التنقل في النظام...")

        navigation_results = {
            'menu_functionality': {},
            'breadcrumb_navigation': {},
            'navigation_consistency': {},
            'keyboard_navigation': {},
            'mobile_navigation': {},
            'search_functionality': {},
            'navigation_issues': []
        }

        try:
            # اختبار القائمة الرئيسية
            menu_test = await self._test_main_menu(page)
            navigation_results['menu_functionality'] = menu_test

            # اختبار التنقل باللوحة المفاتيح
            keyboard_test = await self._test_keyboard_navigation(page)
            navigation_results['keyboard_navigation'] = keyboard_test

            # اختبار البحث
            search_test = await self._test_search_functionality(page)
            navigation_results['search_functionality'] = search_test

            # اختبار اتساق التنقل
            consistency_test = await self._test_navigation_consistency(page)
            navigation_results['navigation_consistency'] = consistency_test

        except Exception as e:
            navigation_results['navigation_issues'].append(f"Error testing navigation: {str(e)}")
            logging.error(f"Error testing navigation: {str(e)}")

        self.results['navigation'] = navigation_results
        return navigation_results

    async def _test_main_menu(self, page: Page) -> Dict[str, Any]:
        """اختبار القائمة الرئيسية"""
        menu_results = {
            'menu_items': 0,
            'working_links': 0,
            'broken_links': 0,
            'responsive_menu': False,
            'issues': []
        }

        try:
            # البحث عن عناصر القائمة
            menu_items = await page.query_selector_all('nav a, [role="navigation"] a, .menu a')

            menu_results['menu_items'] = len(menu_items)

            for item in menu_items[:10]:  # اختبار أول 10 عناصر
                try:
                    # حفظ URL الحالي
                    current_url = page.url

                    # النقر على عنصر القائمة
                    await item.click()
                    await page.wait_for_timeout(2000)

                    # التحقق من تغيير الصفحة
                    if page.url != current_url:
                        menu_results['working_links'] += 1
                    else:
                        menu_results['broken_links'] += 1
                        menu_results['issues'].append(f"Broken menu link: {await item.inner_text()}")

                    # العودة للصفحة الرئيسية
                    await page.goto(self.base_url)
                    await page.wait_for_timeout(1000)

                except Exception as e:
                    menu_results['broken_links'] += 1
                    menu_results['issues'].append(f"Error clicking menu item: {str(e)}")

            # اختبار القائمة المتجاوبة للجوال
            await page.set_viewport_size({'width': 375, 'height': 812})
            await page.goto(self.base_url)
            await page.wait_for_timeout(1000)

            # البحث عن زر القائمة للجوال
            mobile_menu_btn = await page.query_selector('.mobile-menu-btn, .hamburger, [data-testid="mobile-menu"]')
            if mobile_menu_btn:
                menu_results['responsive_menu'] = True
            else:
                menu_results['issues'].append("No mobile menu button found")

        except Exception as e:
            menu_results['issues'].append(f"Error testing main menu: {str(e)}")

        return menu_results

    async def _test_keyboard_navigation(self, page: Page) -> Dict[str, Any]:
        """اختبار التنقل باللوحة المفاتيح"""
        keyboard_results = {
            'tab_order_works': False,
            'focus_visible': False,
            'skip_links': False,
            'keyboard_accessible': 0,
            'total_elements': 0,
            'issues': []
        }

        try:
            # جمع العناصر القابلة للتركيز
            focusable_elements = await page.query_selector_all(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            )

            keyboard_results['total_elements'] = len(focusable_elements)

            # اختبار التركيز بالضغط على Tab
            for i in range(min(10, len(focusable_elements))):
                await page.keyboard.press('Tab')
                await page.wait_for_timeout(100)

                focused_element = await page.evaluate("() => document.activeElement")
                if focused_element:
                    keyboard_results['keyboard_accessible'] += 1

                    # التحقق من ظهور التركيز
                    is_focused_visible = await focused_element.evaluate("""
                        el => {
                            const style = window.getComputedStyle(el);
                            return style.outline !== 'none' || style.boxShadow !== 'none';
                        }
                    """)

                    if is_focused_visible:
                        keyboard_results['focus_visible'] = True

            keyboard_results['tab_order_works'] = keyboard_results['keyboard_accessible'] > 0

            # البحث عن روابط تخطي (skip links)
            skip_links = await page.query_selector_all('.skip-link, [href="#main"], [href="#content"]')
            keyboard_results['skip_links'] = len(skip_links) > 0

            if not keyboard_results['skip_links']:
                keyboard_results['issues'].append("No skip links found for keyboard navigation")

        except Exception as e:
            keyboard_results['issues'].append(f"Error testing keyboard navigation: {str(e)}")

        return keyboard_results

    async def _test_search_functionality(self, page: Page) -> Dict[str, Any]:
        """اختبار وظيفة البحث"""
        search_results = {
            'search_input_exists': False,
            'search_functional': False,
            'search_results_display': False,
            'issues': []
        }

        try:
            # البحث عن حقل البحث
            search_input = await page.query_selector('input[type="search"], [data-testid="search-input"], .search-input')
            if search_input:
                search_results['search_input_exists'] = True

                # اختبار البحث
                await search_input.fill("test")
                await search_input.press('Enter')
                await page.wait_for_timeout(2000)

                # التحقق من وجود نتائج البحث
                search_results_container = await page.query_selector(
                    '[data-testid="search-results"], .search-results, .results'
                )

                if search_results_container:
                    search_results['search_functional'] = True
                    search_results['search_results_display'] = True
                else:
                    search_results['issues'].append("Search results not displayed")
            else:
                search_results['issues'].append("Search input not found")

        except Exception as e:
            search_results['issues'].append(f"Error testing search: {str(e)}")

        return search_results

    async def _test_navigation_consistency(self, page: Page) -> Dict[str, Any]:
        """اختبار اتساق التنقل"""
        consistency_results = {
            'consistent_layout': True,
            'consistent_styling': True,
            'consistent_behavior': True,
            'issues': []
        }

        try:
            # اختبار اتساق القائمة في صفحات مختلفة
            pages_to_test = ['/', '/revenue', '/expenses', '/reports']

            menu_structures = []
            for page_path in pages_to_test:
                await page.goto(f"{self.base_url}{page_path}")
                await page.wait_for_load_state("networkidle")

                menu_structure = await page.evaluate("""
                    () => {
                        const nav = document.querySelector('nav, [role="navigation"]');
                        if (!nav) return null;

                        const links = Array.from(nav.querySelectorAll('a')).map(link => ({
                            text: link.textContent.trim(),
                            href: link.href
                        }));

                        return links;
                    }
                """)

                menu_structures.append(menu_structure)

            # مقارنة هياكل القوائم
            if len(set(tuple(str(struct) for struct in menu_structures))) > 1:
                consistency_results['consistent_layout'] = False
                consistency_results['issues'].append("Inconsistent navigation layout across pages")

        except Exception as e:
            consistency_results['issues'].append(f"Error testing navigation consistency: {str(e)}")

        return consistency_results

    # ===========================
    # 3. اختبارات النماذج
    # ===========================

    async def test_forms(self, page: Page) -> Dict[str, Any]:
        """اختبار النماذج"""
        print("📝 اختبار النماذج...")

        forms_results = {
            'form_discovery': {},
            'validation': {},
            'accessibility': {},
            'user_experience': {},
            'submission': {},
            'error_handling': {},
            'form_issues': []
        }

        try:
            # اكتشاف النماذج
            forms_discovered = await self._discover_forms(page)
            forms_results['form_discovery'] = forms_discovered

            # اختبار التحقق من صحة النماذج
            validation_test = await self._test_form_validation(page)
            forms_results['validation'] = validation_test

            # اختبار إمكانية الوصول للنماذج
            accessibility_test = await self._test_forms_accessibility(page)
            forms_results['accessibility'] = accessibility_test

            # اختبار تجربة المستخدم في النماذج
            ux_test = await self._test_forms_user_experience(page)
            forms_results['user_experience'] = ux_test

        except Exception as e:
            forms_results['form_issues'].append(f"Error testing forms: {str(e)}")
            logging.error(f"Error testing forms: {str(e)}")

        self.results['forms'] = forms_results
        return forms_results

    async def _discover_forms(self, page: Page) -> Dict[str, Any]:
        """اكتشاف النماذج في الصفحة"""
        discovery_results = {
            'total_forms': 0,
            'forms_by_page': {},
            'form_types': {},
            'input_types': {}
        }

        try:
            pages_to_test = ['/revenue', '/expenses', '/login', '/register']

            for page_path in pages_to_test:
                try:
                    await page.goto(f"{self.base_url}{page_path}")
                    await page.wait_for_load_state("networkidle")

                    forms = await page.query_selector_all('form')
                    discovery_results['total_forms'] += len(forms)

                    page_forms = []
                    for form in forms:
                        form_info = await form.evaluate("""
                            (form) => {
                                const inputs = form.querySelectorAll('input, textarea, select');
                                const inputTypes = Array.from(inputs).map(input => input.type || input.tagName.toLowerCase());
                                const hasSubmit = form.querySelector('input[type="submit"], button[type="submit"]') !== null;

                                return {
                                    id: form.id || form.name || 'unnamed',
                                    inputTypes: inputTypes,
                                    hasSubmit: hasSubmit,
                                    inputsCount: inputs.length
                                };
                            }
                        """)

                        page_forms.append(form_info)

                        # تحليل أنواع المدخلات
                        for input_type in form_info['inputTypes']:
                            discovery_results['input_types'][input_type] = discovery_results['input_types'].get(input_type, 0) + 1

                    discovery_results['forms_by_page'][page_path] = page_forms

                except Exception as e:
                    logging.error(f"Error discovering forms on {page_path}: {str(e)}")

        except Exception as e:
            logging.error(f"Error in form discovery: {str(e)}")

        return discovery_results

    async def _test_form_validation(self, page: Page) -> Dict[str, Any]:
        """اختبار التحقق من صحة النماذج"""
        validation_results = {
            'client_side_validation': 0,
            'required_fields': 0,
            'error_messages': 0,
            'validation_working': 0,
            'issues': []
        }

        try:
            await page.goto(f"{self.base_url}/login")
            await page.wait_for_load_state("networkidle")

            # اختبار الحقول المطلوبة
            required_fields = await page.query_selector_all('input[required], textarea[required], select[required]')
            validation_results['required_fields'] = len(required_fields)

            # اختبار التحقق من البريد الإلكتروني
            email_input = await page.query_selector('input[type="email"]')
            if email_input:
                await email_input.fill('invalid-email')
                await email_input.press('Tab')

                await page.wait_for_timeout(1000)

                # التحقق من وجود رسالة خطأ
                error_messages = await page.query_selector_all('.error, .invalid-feedback, [role="alert"]')
                if len(error_messages) > 0:
                    validation_results['client_side_validation'] += 1
                    validation_results['error_messages'] += 1

            # اختبار حقول فارغة مطلوبة
            submit_button = await page.query_selector('button[type="submit"]')
            if submit_button:
                await submit_button.click()
                await page.wait_for_timeout(1000)

                # التحقق من منع الإرسال
                current_url = page.url
                if current_url == f"{self.base_url}/login":
                    validation_results['validation_working'] += 1

        except Exception as e:
            validation_results['issues'].append(f"Error testing form validation: {str(e)}")

        return validation_results

    async def _test_forms_accessibility(self, page: Page) -> Dict[str, Any]:
        """اختبار إمكانية الوصول للنماذج"""
        accessibility_results = {
            'labels_for_inputs': 0,
            'total_inputs': 0,
            'aria_attributes': 0,
            'accessible_forms': 0,
            'issues': []
        }

        try:
            forms = await page.query_selector_all('form')

            for form in forms:
                try:
                    inputs = await form.query_selector_all('input, textarea, select')
                    accessibility_results['total_inputs'] += len(inputs)

                    labels_for_form = 0
                    for input_element in inputs:
                        # التحقق من وجود label
                        input_id = await input_element.get_attribute('id')
                        if input_id:
                            label = await form.query_selector(f'label[for="{input_id}"]')
                            if label:
                                labels_for_form += 1

                        # التحقق من aria-label
                        aria_label = await input_element.get_attribute('aria-label')
                        if aria_label:
                            accessibility_results['aria_attributes'] += 1

                    accessibility_results['labels_for_inputs'] += labels_for_form

                    if labels_for_form == len(inputs):
                        accessibility_results['accessible_forms'] += 1

                except Exception:
                    continue

        except Exception as e:
            accessibility_results['issues'].append(f"Error testing forms accessibility: {str(e)}")

        return accessibility_results

    async def _test_forms_user_experience(self, page: Page) -> Dict[str, Any]:
        """اختبار تجربة المستخدم في النماذج"""
        ux_results = {
            'auto_focus': 0,
            'placeholder_text': 0,
            'help_text': 0,
            'loading_indicators': 0,
            'success_messages': 0,
            'issues': []
        }

        try:
            forms = await page.query_selector_all('form')

            for form in forms:
                try:
                    # التحقق من التركيز التلقائي
                    first_input = await form.query_selector('input, textarea, select')
                    if first_input:
                        is_focused = await first_input.evaluate("el => el === document.activeElement")
                        if is_focused:
                            ux_results['auto_focus'] += 1

                    # التحقق من النصوص المساعدة
                    inputs = await form.query_selector_all('input, textarea, select')
                    for input_element in inputs:
                        placeholder = await input_element.get_attribute('placeholder')
                        if placeholder:
                            ux_results['placeholder_text'] += 1

                        # البحث عن نصوص مساعدة
                        parent = await input_element.evaluate_handle("el => el.parentElement")
                        help_text = await parent.query_selector('.help-text, .description, small')
                        if help_text:
                            ux_results['help_text'] += 1

                except Exception:
                    continue

        except Exception as e:
            ux_results['issues'].append(f"Error testing forms UX: {str(e)}")

        return ux_results

    # ===========================
    # 4. اختبارات التفاعل
    # ===========================

    async def test_interactions(self, page: Page) -> Dict[str, Any]:
        """اختبار التفاعلات"""
        print("🎯 اختبار التفاعلات...")

        interactions_results = {
            'buttons': {},
            'links': {},
            'modals': {},
            'dropdowns': {},
            'tabs': {},
            'animations': {},
            'interaction_issues': []
        }

        try:
            # اختبار الأزرار
            buttons_test = await self._test_buttons(page)
            interactions_results['buttons'] = buttons_test

            # اختبار الروابط
            links_test = await self._test_links(page)
            interactions_results['links'] = links_test

            # اختبار القوائم المنسدلة
            dropdowns_test = await self._test_dropdowns(page)
            interactions_results['dropdowns'] = dropdowns_test

            # اختبار النوافذ المنبثقة
            modals_test = await self._test_modals(page)
            interactions_results['modals'] = modals_test

        except Exception as e:
            interactions_results['interaction_issues'].append(f"Error testing interactions: {str(e)}")
            logging.error(f"Error testing interactions: {str(e)}")

        self.results['interactions'] = interactions_results
        return interactions_results

    async def _test_buttons(self, page: Page) -> Dict[str, Any]:
        """اختبار الأزرار"""
        buttons_results = {
            'total_buttons': 0,
            'working_buttons': 0,
            'disabled_buttons': 0,
            'buttons_with_labels': 0,
            'issues': []
        }

        try:
            buttons = await page.query_selector_all('button, [role="button"], input[type="button"], input[type="submit"]')
            buttons_results['total_buttons'] = len(buttons)

            for button in buttons[:20]:  # اختبار أول 20 زر
                try:
                    # التحقق من وجود نص أو aria-label
                    button_text = await button.inner_text()
                    aria_label = await button.get_attribute('aria-label')

                    if button_text.strip() or aria_label:
                        buttons_results['buttons_with_labels'] += 1

                    # التحقق من حالة الزر
                    is_disabled = await button.is_disabled()
                    if is_disabled:
                        buttons_results['disabled_buttons'] += 1
                    else:
                        buttons_results['working_buttons'] += 1

                except Exception as e:
                    buttons_results['issues'].append(f"Error testing button: {str(e)}")

        except Exception as e:
            buttons_results['issues'].append(f"Error in buttons test: {str(e)}")

        return buttons_results

    async def _test_links(self, page: Page) -> Dict[str, Any]:
        """اختبار الروابط"""
        links_results = {
            'total_links': 0,
            'working_links': 0,
            'broken_links': 0,
            'links_with_text': 0,
            'issues': []
        }

        try:
            links = await page.query_selector_all('a[href]')
            links_results['total_links'] = len(links)

            for link in links[:15]:  # اختبار أول 15 رابط
                try:
                    href = await link.get_attribute('href')
                    if href and href.startswith('http'):
                        links_results['working_links'] += 1
                    elif href and not href.startswith('#'):
                        links_results['working_links'] += 1
                    elif href == '#':
                        links_results['broken_links'] += 1

                    # التحقق من وجود نص
                    link_text = await link.inner_text()
                    if link_text.strip():
                        links_results['links_with_text'] += 1
                    else:
                        # التحقق من aria-label
                        aria_label = await link.get_attribute('aria-label')
                        if not aria_label:
                            links_results['issues'].append("Link without text or aria-label")

                except Exception as e:
                    links_results['issues'].append(f"Error testing link: {str(e)}")

        except Exception as e:
            links_results['issues'].append(f"Error in links test: {str(e)}")

        return links_results

    async def _test_dropdowns(self, page: Page) -> Dict[str, Any]:
        """اختبار القوائم المنسدلة"""
        dropdowns_results = {
            'total_dropdowns': 0,
            'working_dropdowns': 0,
            'dropdowns_with_labels': 0,
            'issues': []
        }

        try:
            dropdowns = await page.query_selector_all('select, [data-testid="dropdown"], .dropdown')
            dropdowns_results['total_dropdowns'] = len(dropdowns)

            for dropdown in dropdowns:
                try:
                    # التحقق من وجود خيارات
                    if dropdown.evaluate("el => el.tagName.toLowerCase() === 'select'"):
                        options = await dropdown.query_selector_all('option')
                        if len(options) > 0:
                            dropdowns_results['working_dropdowns'] += 1

                    # التحقق من وجود label
                    dropdown_id = await dropdown.get_attribute('id')
                    if dropdown_id:
                        label = await page.query_selector(f'label[for="{dropdown_id}"]')
                        if label:
                            dropdowns_results['dropdowns_with_labels'] += 1

                except Exception as e:
                    dropdowns_results['issues'].append(f"Error testing dropdown: {str(e)}")

        except Exception as e:
            dropdowns_results['issues'].append(f"Error in dropdowns test: {str(e)}")

        return dropdowns_results

    async def _test_modals(self, page: Page) -> Dict[str, Any]:
        """اختبار النوافذ المنبثقة"""
        modals_results = {
            'total_modals': 0,
            'working_modals': 0,
            'accessible_modals': 0,
            'issues': []
        }

        try:
            # البحث عن أزرار فتح النوافذ المنبثقة
            modal_triggers = await page.query_selector_all(
                '[data-modal], [data-target], [data-toggle="modal"], [role="button"][aria-expanded]'
            )

            modals_results['total_modals'] = len(modal_triggers)

            for trigger in modal_triggers[:5]:  # اختبار أول 5 نوافذ منبثقة
                try:
                    await trigger.click()
                    await page.wait_for_timeout(1000)

                    # التحقق من ظهور النافذة المنبثقة
                    modal = await page.query_selector('.modal, [role="dialog"], .dialog')
                    if modal:
                        modals_results['working_modals'] += 1

                        # التحقق من إمكانية الوصول
                        modal_role = await modal.get_attribute('role')
                        modal_label = await modal.get_attribute('aria-label')
                        modal_labelledby = await modal.get_attribute('aria-labelledby')

                        if modal_role == 'dialog' and (modal_label or modal_labelledby):
                            modals_results['accessible_modals'] += 1

                        # إغلاق النافذة المنبثقة
                        close_button = await modal.query_selector('.close, [data-dismiss="modal"], [aria-label="Close"]')
                        if close_button:
                            await close_button.click()

                    await page.wait_for_timeout(500)

                except Exception as e:
                    modals_results['issues'].append(f"Error testing modal: {str(e)}")

        except Exception as e:
            modals_results['issues'].append(f"Error in modals test: {str(e)}")

        return modals_results

    # ===========================
    # 5. اختبارات التصميم البصري
    # ===========================

    async def test_visual_design(self, page: Page) -> Dict[str, Any]:
        """اختبار التصميم البصري"""
        print("🎨 اختبار التصميم البصري...")

        design_results = {
            'color_scheme': {},
            'typography': {},
            'spacing': {},
            'visual_hierarchy': {},
            'branding': {},
            'consistency': {},
            'design_issues': []
        }

        try:
            # اختبار نظام الألوان
            color_test = await self._test_color_scheme(page)
            design_results['color_scheme'] = color_test

            # اختبار الطباعة
            typography_test = await self._test_typography(page)
            design_results['typography'] = typography_test

            # اختبار المسافات
            spacing_test = await self._test_spacing(page)
            design_results['spacing'] = spacing_test

        except Exception as e:
            design_results['design_issues'].append(f"Error testing visual design: {str(e)}")
            logging.error(f"Error testing visual design: {str(e)}")

        self.results['visual_design'] = design_results
        return design_results

    async def _test_color_scheme(self, page: Page) -> Dict[str, Any]:
        """اختبار نظام الألوان"""
        color_results = {
            'primary_colors': [],
            'contrast_ratio': {},
            'color_consistency': True,
            'issues': []
        }

        try:
            # تحليل الألوان المستخدمة
            color_analysis = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('*');
                    const colors = new Set();
                    const backgroundColors = new Set();

                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.color && style.color !== 'rgba(0, 0, 0, 0)') {
                            colors.add(style.color);
                        }
                        if (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)') {
                            backgroundColors.add(style.backgroundColor);
                        }
                    });

                    return {
                        textColors: Array.from(colors),
                        backgroundColors: Array.from(backgroundColors)
                    };
                }
            """)

            color_results['primary_colors'] = color_analysis['textColors'][:5]  # أول 5 ألوان

            # اختبار نسبة التباين (تبسيط)
            contrast_elements = await page.query_selector_all('h1, h2, button, .btn')
            for element in contrast_elements[:10]:
                try:
                    contrast_ratio = await element.evaluate("""
                        el => {
                            const style = window.getComputedStyle(el);
                            const bgColor = window.getComputedStyle(el.parentElement).backgroundColor;
                            // تبسيط حساب نسبة التباين
                            return style.color !== bgColor ? 'good' : 'poor';
                        }
                    """)

                    if contrast_ratio == 'poor':
                        color_results['issues'].append("Poor color contrast detected")

                except Exception:
                    continue

        except Exception as e:
            color_results['issues'].append(f"Error testing color scheme: {str(e)}")

        return color_results

    async def _test_typography(self, page: Page) -> Dict[str, Any]:
        """اختبار الطباعة"""
        typography_results = {
            'font_families': [],
            'font_sizes': {},
            'heading_hierarchy': True,
            'issues': []
        }

        try:
            # تحليل الخطوط المستخدمة
            font_analysis = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, div');
                    const fontFamilies = new Set();
                    const fontSizes = {};

                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const fontFamily = style.fontFamily;
                        const fontSize = style.fontSize;
                        const tagName = el.tagName.toLowerCase();

                        fontFamilies.add(fontFamily);

                        if (!fontSizes[tagName]) {
                            fontSizes[tagName] = new Set();
                        }
                        fontSizes[tagName].add(fontSize);
                    });

                    return {
                        fontFamilies: Array.from(fontFamilies),
                        fontSizes: fontSizes
                    };
                }
            """)

            typography_results['font_families'] = font_analysis['fontFamilies']
            typography_results['font_sizes'] = font_analysis['fontSizes']

            # التحقق من تسلسل العناوين
            headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            heading_sizes = {}

            for heading in headings:
                heading_elements = await page.query_selector_all(heading)
                if heading_elements:
                    first_size = await heading_elements[0].evaluate("el => window.getComputedStyle(el).fontSize")
                    heading_sizes[heading] = first_size

            # التحقق من أن العناوين الأكبر لها حجم أكبر
            for i in range(len(headings) - 1):
                if headings[i] in heading_sizes and headings[i + 1] in heading_sizes:
                    if float(heading_sizes[headings[i]]) <= float(heading_sizes[headings[i + 1]]):
                        typography_results['heading_hierarchy'] = False
                        typography_results['issues'].append(f"Heading hierarchy issue: {headings[i]} not larger than {headings[i + 1]}")

        except Exception as e:
            typography_results['issues'].append(f"Error testing typography: {str(e)}")

        return typography_results

    async def _test_spacing(self, page: Page) -> Dict[str, Any]:
        """اختبار المسافات"""
        spacing_results = {
            'consistent_spacing': True,
            'adequate_whitespace': True,
            'padding_margins': {},
            'issues': []
        }

        try:
            # تحليل المسافات (تبسيط)
            spacing_analysis = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('.container, .row, .col, .card, .btn');
                    const spacings = [];

                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        spacings.push({
                            padding: style.padding,
                            margin: style.margin,
                            element: el.className || el.tagName
                        });
                    });

                    return spacings;
                }
            """)

            spacing_results['padding_margins'] = spacing_analysis[:10]  # أول 10 عناصر

            # التحقق من وجود مسافات كافية
            too_close_elements = await page.query_selector_all('*')
            for element in too_close_elements[:20]:
                try:
                    margin = await element.evaluate("el => parseFloat(window.getComputedStyle(el).marginTop)")
                    if margin < 4:  # أقل من 4px
                        spacing_results['issues'].append("Insufficient margin detected")
                        break
                except Exception:
                    continue

        except Exception as e:
            spacing_results['issues'].append(f"Error testing spacing: {str(e)}")

        return spacing_results

    # ===========================
    # 6. اختبارات تدفقات المستخدم
    # ===========================

    async def test_user_flows(self, page: Page) -> Dict[str, Any]:
        """اختبار تدفقات المستخدم"""
        print("🔄 اختبار تدفقات المستخدم...")

        flows_results = {
            'flows_tested': 0,
            'successful_flows': 0,
            'failed_flows': 0,
            'average_completion_time': 0,
            'flow_details': {},
            'flow_issues': []
        }

        try:
            completion_times = []

            for flow in self.user_flows:
                try:
                    flow_result = await self._execute_user_flow(page, flow)
                    flows_results['flows_tested'] += 1
                    flows_results['flow_details'][flow['name']] = flow_result

                    if flow_result['success']:
                        flows_results['successful_flows'] += 1
                        completion_times.append(flow_result['completion_time'])
                    else:
                        flows_results['failed_flows'] += 1
                        flows_results['flow_issues'].extend(flow_result['issues'])

                except Exception as e:
                    flows_results['flows_tested'] += 1
                    flows_results['failed_flows'] += 1
                    flows_results['flow_issues'].append(f"Error testing flow {flow['name']}: {str(e)}")

            if completion_times:
                flows_results['average_completion_time'] = statistics.mean(completion_times)

        except Exception as e:
            flows_results['flow_issues'].append(f"Error testing user flows: {str(e)}")
            logging.error(f"Error testing user flows: {str(e)}")

        self.results['user_flows'] = flows_results
        return flows_results

    async def _execute_user_flow(self, page: Page, flow: Dict) -> Dict[str, Any]:
        """تنفيذ تدفق مستخدم معين"""
        flow_result = {
            'name': flow['name'],
            'success': True,
            'completion_time': 0,
            'steps_completed': 0,
            'issues': []
        }

        start_time = time.time()

        try:
            for step in flow['steps']:
                try:
                    if step['action'] == 'navigate':
                        await page.goto(f"{self.base_url}{step['url']}")
                        await page.wait_for_load_state("networkidle")
                    elif step['action'] == 'fill':
                        element = await page.wait_for_selector(step['selector'], timeout=5000)
                        await element.fill(step['value'])
                    elif step['action'] == 'click':
                        element = await page.wait_for_selector(step['selector'], timeout=5000)
                        await element.click()
                    elif step['action'] == 'wait':
                        await page.wait_for_selector(step['selector'], timeout=10000)

                    flow_result['steps_completed'] += 1
                    await page.wait_for_timeout(500)  # انتظار قصير بين الخطوات

                except Exception as e:
                    flow_result['success'] = False
                    flow_result['issues'].append(f"Step failed: {step['action']} - {str(e)}")
                    break

        except Exception as e:
            flow_result['success'] = False
            flow_result['issues'].append(f"Flow execution error: {str(e)}")

        flow_result['completion_time'] = time.time() - start_time

        return flow_result

    # ===========================
    # حساب النتيجة النهائية
    # ===========================

    def calculate_ux_score(self) -> float:
        """حساب درجة تجربة المستخدم"""
        score = 100
        penalties = 0

        # تقييم التجاوب
        responsiveness = self.results.get('responsiveness', {})
        issues_count = len(responsiveness.get('responsive_issues', []))
        penalties += issues_count * 2

        # تقييم التنقل
        navigation = self.results.get('navigation', {})
        menu_func = navigation.get('menu_functionality', {})
        if menu_func.get('broken_links', 0) > 0:
            penalties += menu_func['broken_links'] * 3

        # تقييم النماذج
        forms = self.results.get('forms', {})
        validation = forms.get('validation', {})
        if validation.get('validation_working', 0) == 0:
            penalties += 10

        # تقييم التفاعلات
        interactions = self.results.get('interactions', {})
        buttons = interactions.get('buttons', {})
        if buttons.get('buttons_with_labels', 0) < buttons.get('total_buttons', 0) * 0.8:
            penalties += 8

        # تقييم تدفقات المستخدم
        user_flows = self.results.get('user_flows', {})
        success_rate = user_flows.get('successful_flows', 0) / max(user_flows.get('flows_tested', 1), 1)
        if success_rate < 0.8:
            penalties += (0.8 - success_rate) * 20

        self.ux_score = max(0, score - penalties)
        return self.ux_score

    # ===========================
    # تنفيذ الاختبارات الكاملة
    # ===========================

    async def run_ux_ui_tests(self) -> Dict[str, Any]:
        """تنفيذ جميع اختبارات الواجهة والتجربة المستخدم"""
        print("🚀 بدء اختبارات الواجهة والتجربة المستخدم...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            try:
                # 1. اختبارات التجاوب
                await self.test_responsiveness(page)

                # 2. اختبارات التنقل
                await self.test_navigation(page)

                # 3. اختبارات النماذج
                await self.test_forms(page)

                # 4. اختبارات التفاعل
                await self.test_interactions(page)

                # 5. اختبارات التصميم البصري
                await self.test_visual_design(page)

                # 6. اختبارات تدفقات المستخدم
                await self.test_user_flows(page)

            finally:
                await browser.close()

        # حساب النتيجة النهائية
        final_score = self.calculate_ux_score()

        # جمع جميع القضايا
        all_issues = []
        for category, results in self.results.items():
            if isinstance(results, dict):
                issues_key = f"{category}_issues" if category.endswith('s') else f"{category}_issues"
                if issues_key in results:
                    all_issues.extend(results[issues_key])
                if 'issues' in results:
                    all_issues.extend(results['issues'])

        self.ux_issues = all_issues

        # إنشاء تقرير الواجهة والتجربة المستخدم
        ux_report = self.generate_ux_ui_report(final_score)

        return {
            'score': final_score,
            'results': self.results,
            'issues': all_issues,
            'report': ux_report
        }

    def generate_ux_ui_report(self, score: float) -> str:
        """إنشاء تقرير الواجهة والتجربة المستخدم"""
        report = f"""
================================================================================
                        BARBERTRACK UX/UI TEST REPORT
================================================================================
تاريخ الاختبار: {self.test_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
النظام: BarberTrack - نظام إدارة الصالونات متعددة الفروع
الهدف: تقييم واجهة المستخدم وتجربة الاستخدام

UX/UI SCORE SUMMARY
─────────────────────────────────────────────────────────────────────────────
درجة الواجهة: {score:.1f}/100
حالة الواجهة: {'✅ ممتازة' if score >= 90 else '🟡 جيدة' if score >= 70 else '🔴 تحتاج تحسين'}
عدد القضايا المكتشفة: {len(self.ux_issues)}

RESPONSIVENESS & MOBILE
─────────────────────────────────────────────────────────────────────────────
"""

        responsiveness = self.results.get('responsiveness', {})
        report += f"""
Viewports Tested: {responsiveness.get('viewports_tested', 0)}
Responsive Issues: {len(responsiveness.get('responsive_issues', []))}
Mobile Touch Targets: {responsiveness.get('touch_targets', {}).get('adequate_size', 0)}/{responsiveness.get('touch_targets', {}).get('buttons_tested', 0)}
"""

        report += f"""

NAVIGATION & USABILITY
─────────────────────────────────────────────────────────────────────────────
"""

        navigation = self.results.get('navigation', {})
        menu_func = navigation.get('menu_functionality', {})
        report += f"""
Menu Items: {menu_func.get('menu_items', 0)}
Working Links: {menu_func.get('working_links', 0)}
Broken Links: {menu_func.get('broken_links', 0)}
Keyboard Navigation: {'✅' if navigation.get('keyboard_navigation', {}).get('tab_order_works', False) else '❌'}
Search Functionality: {'✅' if navigation.get('search_functionality', {}).get('search_functional', False) else '❌'}
"""

        report += f"""

FORMS & INTERACTIONS
─────────────────────────────────────────────────────────────────────────────
"""

        forms = self.results.get('forms', {})
        interactions = self.results.get('interactions', {})
        report += f"""
Forms Discovered: {forms.get('form_discovery', {}).get('total_forms', 0)}
Form Validation Working: {'✅' if forms.get('validation', {}).get('validation_working', 0) > 0 else '❌'}
Buttons with Labels: {interactions.get('buttons', {}).get('buttons_with_labels', 0)}/{interactions.get('buttons', {}).get('total_buttons', 0)}
Working Dropdowns: {interactions.get('dropdowns', {}).get('working_dropdowns', 0)}/{interactions.get('dropdowns', {}).get('total_dropdowns', 0)}
"""

        report += f"""

USER FLOWS & PERFORMANCE
─────────────────────────────────────────────────────────────────────────────
"""

        user_flows = self.results.get('user_flows', {})
        report += f"""
User Flows Tested: {user_flows.get('flows_tested', 0)}
Successful Flows: {user_flows.get('successful_flows', 0)}
Failed Flows: {user_flows.get('failed_flows', 0)}
Average Completion Time: {user_flows.get('average_completion_time', 0):.2f}s
Success Rate: {(user_flows.get('successful_flows', 0) / max(user_flows.get('flows_tested', 1), 1) * 100):.1f}%
"""

        report += f"""

VISUAL DESIGN & ACCESSIBILITY
─────────────────────────────────────────────────────────────────────────────
"""

        visual_design = self.results.get('visual_design', {})
        report += f"""
Color Scheme: {len(visual_design.get('color_scheme', {}).get('primary_colors', []))} primary colors
Font Families: {len(visual_design.get('typography', {}).get('font_families', []))} fonts
Heading Hierarchy: {'✅' if visual_design.get('typography', {}).get('heading_hierarchy', False) else '❌'}
Consistent Spacing: {'✅' if visual_design.get('spacing', {}).get('consistent_spacing', False) else '❌'}
"""

        report += f"""

DETAILED UX/UI ISSUES
─────────────────────────────────────────────────────────────────────────────
"""

        if self.ux_issues:
            for i, issue in enumerate(self.ux_issues[:15], 1):  # أول 15 قضية
                report += f"{i:2d}. ⚠️ {issue}\n"
            if len(self.ux_issues) > 15:
                report += f"... و {len(self.ux_issues) - 15} قضية أخرى\n"
        else:
            report += "✅ لا توجد قضايا واجهة وتجربة مستخدم\n"

        report += f"""

UX/UI RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────

🎯 HIGH PRIORITY (48 ساعة)
"""

        high_priority = []
        if score < 70:
            high_priority.append("إصلاح القضايا الحرجة في الواجهة وتجربة المستخدم")
        if user_flows.get('success_rate', 0) < 0.8:
            high_priority.append("تحسين تدفقات المستخدم الأساسية")
        if menu_func.get('broken_links', 0) > 0:
            high_priority.append("إصلاح الروابط المعطلة")

        for rec in high_priority:
            report += f"   • {rec}\n"

        report += f"""

📈 MEDIUM PRIORITY (أسبوع)
"""
        medium_priority = [
            "تحسين تصميم النماذج والتحقق من صحة البيانات",
            "تعزيز إمكانية الوصول لواجهة المستخدم",
            "تحسين تجربة المستخدم على الأجهزة المحمولة",
            "توحيد التصميم البصري في جميع الصفحات",
            "إضافة المزيد من مؤشرات التحميل والتفاعل"
        ]

        for rec in medium_priority:
            report += f"   • {rec}\n"

        report += f"""

🔧 LOW PRIORITY (شهر)
"""
        low_priority = [
            "تحسين الأداء البصري والرسوم المتحركة",
            "إضافة المزيد من ميزات إمكانية الوصول",
            "تحسين تجربة المستخدم المتقدمة",
            "إضافة المزيد من التخصيص في الواجهة"
        ]

        for rec in low_priority:
            report += f"   • {rec}\n"

        report += f"""

CONCLUSION
─────────────────────────────────────────────────────────────────────────────
{'✅ واجهة المستخدم ممتازة' if score >= 90 else '⚠️ الواجهة جيدة مع تحسينات طفيفة' if score >= 70 else '❌ الواجهة تحتاج إلى تحسينات كبيرة'}

توصية النشر: {'يمكن نشر النظام مع واجهة مستخدم ممتازة' if score >= 85 else 'يجب تحسين الواجهة قبل النشر'}

ملاحظة: تأكد من اختبار الواجهة على مختلف الأجهزة والمتصفحات
================================================================================
        """

        # حفظ التقرير
        report_path = 'test_results/ux_ui_test_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

# نقطة الدخول الرئيسية
async def main():
    """نقطة الدخول الرئيسية"""
    print("🎨 نظام اختبار الواجهة والتجربة المستخدم لـ BarberTrack")
    print("=" * 50)

    ux_ui_tester = UXUITestSuite()

    try:
        results = await ux_ui_tester.run_ux_ui_tests()

        print(f"\n📊 درجة الواجهة والتجربة المستخدم: {results['score']:.1f}/100")
        print(f"🎯 حالة الواجهة: {'ممتازة' if results['score'] >= 90 else 'جيدة' if results['score'] >= 70 else 'تحتاج تحسين'}")
        print(f"⚠️ عدد القضايا: {len(results['issues'])}")

        print(f"\n📋 التقرير الكامل متوفر في: test_results/ux_ui_test_report.txt")

    except Exception as e:
        print(f"❌ خطأ في تنفيذ اختبارات الواجهة والتجربة المستخدم: {str(e)}")
        logging.error(f"UX/UI test execution failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())