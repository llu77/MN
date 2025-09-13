"""
نصوص اختبار الأمان المتقدمة (OWASP Top 10) لنظام سهل
مطور: Full-stack Security Testing Specialist
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Page, Browser
import requests
import re
from datetime import datetime
import hashlib
import base64

class SecurityTestSuite:
    """مجموعة اختبارات الأمان المتقدمة لـ سهل Cloudflare D1 وWorkers"""

    def __init__(self, base_url: str = "http://localhost:9002"):
        self.base_url = base_url
        self.results = {
            'injection_tests': [],
            'xss_tests': [],
            'auth_tests': [],
            'authorization_tests': [],
            'security_headers': [],
            'file_upload_tests': [],
            'rate_limiting_tests': [],
            'csrf_tests': [],
            'sensitive_data_tests': [],
            'api_security_tests': [],
            'cloudflare_workers_tests': [],
            'branch_isolation_tests': [],
            'realtime_sync_tests': [],
            'd1_database_tests': []
        }
        self.vulnerabilities = []
        self.security_score = 100
        self.test_timestamp = datetime.now()
        self.cloudflare_workers_url = "https://sahl.llu77.workers.dev"  # Workers URL
        self.cloudflare_d1_database = "sahl-db"  # D1 Database name

        # إعداد التسجيل
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('security_test_results.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    # ===========================
    # 1. اختبارات حقن SQL و NoSQL
    # ===========================

    async def test_injection_attacks(self, page: Page) -> Dict[str, Any]:
        """اختبار هجمات الحقن (SQLi, NoSQLi, OS Command)"""
        print("🔍 اختبار هجمات الحقن...")

        test_results = {
            'sql_injection': [],
            'nosql_injection': [],
            'command_injection': [],
            'xss_injection': [],
            'ldap_injection': []
        }

        # Payloads للاختبار
        injection_payloads = {
            'sql': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT branch_id, branch_name FROM branches--",
                "'; DROP TABLE users; --",
                "' AND (SELECT COUNT(*) FROM branches) > 0--",
                "' OR SLEEP(10)--",
                "' WAITFOR DELAY '0:0:10'--",
                "' || (SELECT COUNT(*) FROM users) --",
                "'; SELECT sqlite_version(); --",
                "' UNION SELECT name, sql FROM sqlite_master--"
            ],
            'nosql': [
                '{"$ne": null}',
                '{"$gt": ""}',
                '{"$where": "function() { return true; }"}',
                "'; return true; var x='",
                "' || 1==1 || '",
                "{$gt: ''}",
                "{$ne: null}"
            ],
            'command': [
                "; ls -la",
                "| whoami",
                "& dir",
                "`cat /etc/passwd`",
                "$(cat /etc/passwd)",
                "<!--#exec cmd=\"ls\"-->",
                "&& ping -c 10 127.0.0.1"
            ],
            'xss': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>",
                "'\"><script>alert(document.cookie)</script>",
                "<iframe src=\"javascript:alert('XSS')\">",
                "<body onload=alert('XSS')>",
                "';alert(String.fromCharCode(88,83,83));//"
            ]
        }

        # اختبار كل نقطة إدخال محتملة
        input_fields = await self._find_input_fields(page)

        for field_info in input_fields:
            field_name = field_info['name']
            field_type = field_info['type']
            field_placeholder = field_info.get('placeholder', '')

            for injection_type, payloads in injection_payloads.items():
                for payload in payloads:
                    try:
                        result = await self._test_single_injection(
                            page, field_name, payload, injection_type
                        )
                        if result['vulnerable']:
                            test_results[injection_type].append({
                                'field': field_name,
                                'payload': payload,
                                'evidence': result['evidence'],
                                'severity': self._calculate_severity(result['evidence'])
                            })
                            self.vulnerabilities.append({
                                'type': f'{injection_type}_injection',
                                'field': field_name,
                                'payload': payload,
                                'severity': self._calculate_severity(result['evidence']),
                                'description': f"ثغرة حقن {injection_type} في حقل {field_name}"
                            })
                    except Exception as e:
                        logging.error(f"Error testing {injection_type} on {field_name}: {str(e)}")

        self.results['injection_tests'] = test_results
        return test_results

    async def _find_input_fields(self, page: Page) -> List[Dict[str, Any]]:
        """العثور على جميع حقول الإدخال في الصفحة"""
        fields = []

        input_elements = await page.query_selector_all('input, textarea, select')
        for element in input_elements:
            try:
                field_info = await element.evaluate("""el => ({
                    name: el.name || el.id || el.placeholder || 'unnamed',
                    type: el.type || 'text',
                    placeholder: el.placeholder || '',
                    required: el.required || false,
                    disabled: el.disabled || false
                })""")
                fields.append(field_info)
            except:
                continue

        return fields

    async def _test_single_injection(self, page: Page, field_name: str, payload: str, injection_type: str) -> Dict[str, Any]:
        """اختبار حقن واحد في حقل معين"""
        try:
            # الانتقال إلى صفحة تحتوي على الحقل
            await page.goto(self.base_url)

            # البحث عن الحقل وإدخال القيمة
            selector = f"input[name='{field_name}'], textarea[name='{field_name}'], input[placeholder*='{field_name}']"
            field = await page.query_selector(selector)

            if not field:
                return {'vulnerable': False, 'evidence': ''}

            await field.fill(payload)
            await field.press('Enter')  # أو الضغط على زر الإرسال

            await page.wait_for_timeout(2000)

            # التحقق من وجود أخطاء أو استجابات غير متوقعة
            page_content = await page.content()
            error_indicators = [
                'error', 'exception', 'warning', 'sql', 'syntax',
                'stack trace', 'debug', 'query failed'
            ]

            evidence = ''
            for indicator in error_indicators:
                if indicator in page_content.lower():
                    evidence = f"Found '{indicator}' in page response"
                    break

            # التحقق من تنفيذ الـ XSS
            if injection_type == 'xss':
                try:
                    alerts = await page.evaluate("() => window.alert.toString()")
                    if "function" in alerts:
                        evidence = "XSS script executed successfully"
                except:
                    pass

            return {
                'vulnerable': len(evidence) > 0,
                'evidence': evidence
            }

        except Exception as e:
            return {'vulnerable': False, 'evidence': str(e)}

    # ===========================
    # 2. اختبارات المصادقة والتصريح
    # ===========================

    async def test_authentication_security(self, page: Page) -> Dict[str, Any]:
        """اختبار أمان المصادقة"""
        print("🔐 اختبار أمان المصادقة...")

        auth_results = {
            'password_strength': [],
            'brute_force_protection': [],
            'session_management': [],
            'password_reset': [],
            'multi_factor_auth': []
        }

        # اختبار قوة كلمات المرور
        weak_passwords = ['123456', 'password', 'admin123', 'qwerty', '111111']
        for password in weak_passwords:
            try:
                result = await self._test_weak_password(page, password)
                if result['accepted']:
                    auth_results['password_strength'].append({
                        'password': password,
                        'evidence': result['evidence']
                    })
                    self.vulnerabilities.append({
                        'type': 'weak_password',
                        'password': password,
                        'severity': 'high',
                        'description': f"قبول كلمة مرور ضعيفة: {password}"
                    })
            except Exception as e:
                logging.error(f"Error testing weak password {password}: {str(e)}")

        # اختبار حماية brute force
        brute_force_result = await self._test_brute_force_protection(page)
        auth_results['brute_force_protection'].append(brute_force_result)

        # اختبار إدارة الجلسات
        session_result = await self._test_session_management(page)
        auth_results['session_management'].append(session_result)

        self.results['auth_tests'] = auth_results
        return auth_results

    async def _test_brute_force_protection(self, page: Page) -> Dict[str, Any]:
        """اختبار حماية هجمات brute force"""
        login_attempts = []
        is_protected = False

        for i in range(10):  # 10 محاولات تسجيل دخول
            try:
                await page.goto(f"{self.base_url}/login")
                await page.fill('input[type="email"]', f"test{i}@example.com")
                await page.fill('input[type="password"]', "wrongpassword")
                await page.click('button[type="submit"]')

                await page.wait_for_timeout(1000)

                # التحقق من وجود رسائل حماية
                page_content = await page.content()
                if "too many attempts" in page_content.lower() or "locked" in page_content.lower():
                    is_protected = True
                    break

                login_attempts.append(f"Attempt {i+1}: {'blocked' if is_protected else 'allowed'}")

            except Exception as e:
                login_attempts.append(f"Attempt {i+1}: error - {str(e)}")

        return {
            'protected': is_protected,
            'attempts_made': len(login_attempts),
            'evidence': login_attempts
        }

    async def _test_session_management(self, page: Page) -> Dict[str, Any]:
        """اختبار إدارة الجلسات"""
        session_issues = []

        try:
            # تسجيل الدخول (إذا أمكن)
            await page.goto(f"{self.base_url}/login")
            await page.fill('input[type="email"]', "test@example.com")
            await page.fill('input[type="password"]', "testpassword")
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(2000)

            # التحقق من cookies الجلسة
            cookies = await page.context.cookies()
            session_cookies = [c for c in cookies if 'session' in c['name'].lower()]

            if not session_cookies:
                session_issues.append("No session cookies found")
            else:
                for cookie in session_cookies:
                    if not cookie.get('secure', False):
                        session_issues.append(f"Session cookie '{cookie['name']}' not marked as secure")
                    if not cookie.get('httpOnly', False):
                        session_issues.append(f"Session cookie '{cookie['name']}' not HttpOnly")
                    if cookie.get('sameSite') != 'Strict':
                        session_issues.append(f"Session cookie '{cookie['name']}' not SameSite=Strict")

        except Exception as e:
            session_issues.append(f"Session management test error: {str(e)}")

        return {
            'issues_found': len(session_issues),
            'evidence': session_issues
        }

    # ===========================
    # 3. اختبارات الرؤوس الأمنية
    # ===========================

    async def test_security_headers(self) -> Dict[str, Any]:
        """اختبار الرؤوس الأمنية"""
        print("🔒 اختبار الرؤوس الأمنية...")

        try:
            response = requests.get(self.base_url, timeout=10)
            headers = response.headers

            expected_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Content-Security-Policy': "default-src 'self'",
                'Referrer-Policy': 'strict-origin-when-cross-origin',
                'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
            }

            header_results = {}
            missing_headers = []

            for header, expected_value in expected_headers.items():
                if header in headers:
                    actual_value = headers[header]
                    header_results[header] = {
                        'expected': expected_value,
                        'actual': actual_value,
                        'status': 'good' if expected_value in actual_value else 'needs_improvement'
                    }
                else:
                    missing_headers.append(header)
                    header_results[header] = {
                        'expected': expected_value,
                        'actual': 'MISSING',
                        'status': 'missing'
                    }

            if missing_headers:
                self.vulnerabilities.append({
                    'type': 'missing_security_headers',
                    'headers': missing_headers,
                    'severity': 'medium',
                    'description': f"Missing security headers: {', '.join(missing_headers)}"
                })

            self.results['security_headers'] = header_results
            return header_results

        except Exception as e:
            logging.error(f"Error testing security headers: {str(e)}")
            return {'error': str(e)}

    # ===========================
    # 4. اختبارات CSRF
    # ===========================

    async def test_csrf_protection(self, page: Page) -> Dict[str, Any]:
        """اختبار حماية CSRF"""
        print("🛡️ اختبار حماية CSRF...")

        csrf_results = {
            'forms_with_csrf': [],
            'forms_without_csrf': [],
            'token_validation': []
        }

        try:
            await page.goto(self.base_url)

            # البحث عن جميع النماذج
            forms = await page.query_selector_all('form')

            for form in forms:
                form_info = await form.evaluate("""form => ({
                    action: form.action || '',
                    method: form.method || 'GET',
                    has_csrf_token: form.querySelector('input[name*="csrf"], input[name*="token"]') !== null
                })""")

                if form_info['method'].upper() in ['POST', 'PUT', 'DELETE']:
                    if form_info['has_csrf_token']:
                        csrf_results['forms_with_csrf'].append(form_info)
                    else:
                        csrf_results['forms_without_csrf'].append(form_info)
                        self.vulnerabilities.append({
                            'type': 'missing_csrf_token',
                            'form_action': form_info['action'],
                            'severity': 'high',
                            'description': f"POST form without CSRF token: {form_info['action']}"
                        })

        except Exception as e:
            logging.error(f"Error testing CSRF protection: {str(e)}")

        self.results['csrf_tests'] = csrf_results
        return csrf_results

    # ===========================
    # 5. اختبارات تحديد المعدل
    # ===========================

    async def test_rate_limiting(self) -> Dict[str, Any]:
        """اختبار تحديد المعدل"""
        print("⚡ اختبار تحديد المعدل...")

        rate_limiting_results = {
            'api_endpoints': {},
            'login_attempts': {},
            'file_uploads': {}
        }

        # اختبار نقاط API المختلفة
        endpoints_to_test = [
            '/api/login',
            '/api/users',
            '/api/revenue',
            '/api/expenses',
            '/api/reports'
        ]

        for endpoint in endpoints_to_test:
            try:
                # إرسال 50 طلب متتالي
                responses = []
                for i in range(50):
                    response = requests.get(
                        f"{self.base_url}{endpoint}",
                        timeout=5
                    )
                    responses.append({
                        'status_code': response.status_code,
                        'response_time': response.elapsed.total_seconds()
                    })

                # تحليل الاستجابات
                status_codes = [r['status_code'] for r in responses]
                blocked_requests = sum(1 for code in status_codes if code in [429, 403])

                rate_limiting_results['api_endpoints'][endpoint] = {
                    'total_requests': len(responses),
                    'blocked_requests': blocked_requests,
                    'rate_limited': blocked_requests > 0,
                    'evidence': f"{blocked_requests}/{len(responses)} requests blocked"
                }

            except Exception as e:
                rate_limiting_results['api_endpoints'][endpoint] = {
                    'error': str(e)
                }

        self.results['rate_limiting_tests'] = rate_limiting_results
        return rate_limiting_results

    # ===========================
    # 6. اختبارات البيانات الحساسة
    # ===========================

    async def test_sensitive_data_exposure(self, page: Page) -> Dict[str, Any]:
        """اختبار كشف البيانات الحساسة"""
        print("🔍 اختبار كشف البيانات الحساسة...")

        sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b05[0-9]{8}\b|\b9665[0-9]{8}\b',
            'id_number': r'\b[0-9]{10}\b',
            'credit_card': r'\b[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}\b',
            'api_key': r'\bAIza[0-9A-Za-z_-]{35}\b|sk-[a-zA-Z0-9]{48}',
            'jwt_token': r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*',
            'password': r'["\']password["\']\s*:\s*["\'][^"\']+["\']'
        }

        exposure_results = {}

        try:
            await page.goto(self.base_url)
            await page.wait_for_timeout(2000)

            # جمع محتوى الصفحة
            page_content = await page.content()
            page_text = await page.inner_text('body')

            # البحث عن أنماط البيانات الحساسة
            for data_type, pattern in sensitive_patterns.items():
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    exposure_results[data_type] = {
                        'count': len(matches),
                        'matches': matches[:5],  # أول 5 مطابقات فقط
                        'masked': self._mask_sensitive_data(matches)
                    }

                    self.vulnerabilities.append({
                        'type': 'sensitive_data_exposure',
                        'data_type': data_type,
                        'count': len(matches),
                        'severity': 'high' if data_type in ['credit_card', 'api_key', 'jwt_token'] else 'medium',
                        'description': f"Found {len(matches)} instances of {data_type} in page content"
                    })

        except Exception as e:
            logging.error(f"Error testing sensitive data exposure: {str(e)}")

        self.results['sensitive_data_tests'] = exposure_results
        return exposure_results

    def _mask_sensitive_data(self, data: List[str]) -> List[str]:
        """إخفاء البيانات الحساسة للتقرير"""
        masked = []
        for item in data:
            if len(item) > 4:
                masked.append(item[:2] + '*' * (len(item) - 4) + item[-2:])
            else:
                masked.append('*' * len(item))
        return masked

    # ===========================
    # 7. اختبارات API أمنية
    # ===========================

    async def test_api_security(self) -> Dict[str, Any]:
        """اختبار أمان API"""
        print("🔗 اختبار أمان API...")

        api_security_results = {
            'endpoints_tested': [],
            'vulnerable_endpoints': [],
            'authentication_issues': [],
            'authorization_issues': []
        }

        # قائمة نقاط النهاية للاختبار
        api_endpoints = [
            '/api/auth/login',
            '/api/users',
            '/api/revenue',
            '/api/expenses',
            '/api/bonuses',
            '/api/requests',
            '/api/reports'
        ]

        for endpoint in api_endpoints:
            try:
                # اختبار بدون مصادقة
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)

                endpoint_result = {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'auth_required': response.status_code in [401, 403],
                    'response_size': len(response.content)
                }

                # اختبار حقن في معلمات URL
                injection_test = await self._test_api_injection(endpoint)
                endpoint_result['injection_vulnerable'] = injection_test['vulnerable']

                if injection_test['vulnerable']:
                    api_security_results['vulnerable_endpoints'].append(endpoint)
                    self.vulnerabilities.append({
                        'type': 'api_injection',
                        'endpoint': endpoint,
                        'severity': 'high',
                        'description': f"API endpoint vulnerable to injection: {endpoint}"
                    })

                api_security_results['endpoints_tested'].append(endpoint_result)

            except Exception as e:
                api_security_results['endpoints_tested'].append({
                    'endpoint': endpoint,
                    'error': str(e)
                })

        self.results['api_security_tests'] = api_security_results
        return api_security_results

    async def _test_api_injection(self, endpoint: str) -> Dict[str, Any]:
        """اختبار حقن في نقاط API"""
        injection_payloads = [
            "?test=<script>alert('xss')</script>",
            "?test=' OR '1'='1",
            "?test=${7*7}",
            "?test={{7*7}}"
        ]

        for payload in injection_payloads:
            try:
                response = requests.get(f"{self.base_url}{endpoint}{payload}", timeout=5)

                # التحقق من وجود أخطاء أو استجابات غير متوقعة
                if response.status_code == 500 or 'error' in response.text.lower():
                    return {
                        'vulnerable': True,
                        'payload': payload,
                        'evidence': f"Server error with payload: {payload}"
                    }

            except:
                continue

        return {'vulnerable': False, 'payload': None, 'evidence': ''}

    # ===========================
    # 8. اختبارات Cloudflare Workers
    # ===========================

    async def test_cloudflare_workers_security(self) -> Dict[str, Any]:
        """اختبار أمان Cloudflare Workers"""
        print("☁️ اختبار أمان Cloudflare Workers...")

        workers_results = {
            'auth_worker': {},
            'branch_worker': {},
            'revenue_worker': {},
            'sync_worker': {},
            'worker_security_headers': {},
            'worker_rate_limiting': {},
            'worker_cors': {}
        }

        # اختبار أمان كل Worker
        workers_to_test = [
            ('auth', '/api/auth'),
            ('branch', '/api/branches'),
            ('revenue', '/api/revenue'),
            ('sync', '/api/sync')
        ]

        for worker_name, endpoint in workers_to_test:
            try:
                worker_result = await self._test_worker_security(worker_name, endpoint)
                workers_results[f'{worker_name}_worker'] = worker_result
            except Exception as e:
                logging.error(f"Error testing {worker_name} worker: {str(e)}")
                workers_results[f'{worker_name}_worker'] = {'error': str(e)}

        # اختبار الرؤوس الأمنية للـ Workers
        headers_result = await self._test_workers_security_headers()
        workers_results['worker_security_headers'] = headers_result

        # اختبار تحديد المعدل للـ Workers
        rate_limiting_result = await self._test_workers_rate_limiting()
        workers_results['worker_rate_limiting'] = rate_limiting_result

        # اختبار CORS للـ Workers
        cors_result = await self._test_workers_cors()
        workers_results['worker_cors'] = cors_result

        self.results['cloudflare_workers_tests'] = workers_results
        return workers_results

    async def _test_worker_security(self, worker_name: str, endpoint: str) -> Dict[str, Any]:
        """اختبار أمان Worker معين"""
        result = {
            'endpoint': endpoint,
            'vulnerabilities': [],
            'security_headers': [],
            'access_control': []
        }

        try:
            # اختبار الوصول غير المصرح به
            response = requests.get(f"{self.cloudflare_workers_url}{endpoint}", timeout=10)

            if response.status_code == 200:
                result['access_control'].append({
                    'issue': 'Public access to protected endpoint',
                    'severity': 'high'
                })
                self.vulnerabilities.append({
                    'type': 'worker_public_access',
                    'worker': worker_name,
                    'severity': 'high',
                    'description': f"Worker {worker_name} allows public access to protected endpoint"
                })

            # اختبار حقن SQL في Workers
            injection_tests = await self._test_worker_injection(endpoint)
            result['vulnerabilities'].extend(injection_tests)

            # اختبار معالجة الأخطاء
            error_result = await self._test_worker_error_handling(endpoint)
            result['vulnerabilities'].extend(error_result)

        except Exception as e:
            result['error'] = str(e)

        return result

    async def _test_worker_injection(self, endpoint: str) -> List[Dict[str, Any]]:
        """اختبار حقن SQL في Workers"""
        vulnerabilities = []

        injection_payloads = [
            "?branch_id=' OR '1'='1",
            "?user_id=1 UNION SELECT * FROM users",
            "?query='; DROP TABLE branches; --",
            "?data=<script>alert('xss')</script>",
            "?filter={'$ne': null}"
        ]

        for payload in injection_payloads:
            try:
                response = requests.get(
                    f"{self.cloudflare_workers_url}{endpoint}{payload}",
                    timeout=10
                )

                if response.status_code >= 400:
                    continue

                # التحقق من وجود استجابات غير متوقعة
                if 'error' in response.text.lower() or 'exception' in response.text.lower():
                    vulnerabilities.append({
                        'type': 'worker_injection',
                        'payload': payload,
                        'severity': 'high',
                        'evidence': f"Server error with payload: {payload}"
                    })

            except Exception:
                continue

        return vulnerabilities

    async def _test_workers_security_headers(self) -> Dict[str, Any]:
        """اختبار الرؤوس الأمنية للـ Workers"""
        headers_result = {}

        try:
            response = requests.get(self.cloudflare_workers_url, timeout=10)
            headers = response.headers

            required_headers = {
                'Worker-Security': 'required',
                'CF-Worker': 'present',
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY'
            }

            for header, expected in required_headers.items():
                if header not in headers:
                    headers_result[header] = 'MISSING'
                    self.vulnerabilities.append({
                        'type': 'missing_worker_header',
                        'header': header,
                        'severity': 'medium',
                        'description': f"Missing security header: {header}"
                    })
                else:
                    headers_result[header] = 'PRESENT'

        except Exception as e:
            headers_result['error'] = str(e)

        return headers_result

    async def _test_workers_rate_limiting(self) -> Dict[str, Any]:
        """اختبار تحديد المعدل للـ Workers"""
        rate_limiting_result = {'endpoints': {}}

        endpoints = ['/api/auth', '/api/branches', '/api/revenue']

        for endpoint in endpoints:
            try:
                # إرسال 20 طلب متتالي
                responses = []
                for i in range(20):
                    response = requests.get(
                        f"{self.cloudflare_workers_url}{endpoint}",
                        timeout=5
                    )
                    responses.append(response.status_code)

                blocked_count = sum(1 for code in responses if code in [429, 403])

                rate_limiting_result['endpoints'][endpoint] = {
                    'total_requests': len(responses),
                    'blocked_requests': blocked_count,
                    'rate_limited': blocked_count > 0
                }

                if blocked_count == 0:
                    self.vulnerabilities.append({
                        'type': 'worker_no_rate_limiting',
                        'endpoint': endpoint,
                        'severity': 'medium',
                        'description': f"Worker endpoint {endpoint} has no rate limiting"
                    })

            except Exception as e:
                rate_limiting_result['endpoints'][endpoint] = {'error': str(e)}

        return rate_limiting_result

    async def _test_workers_cors(self) -> Dict[str, Any]:
        """اختبار CORS للـ Workers"""
        cors_result = {}

        try:
            # اختبار طلب من مصدر مختلف
            headers = {'Origin': 'https://malicious-site.com'}
            response = requests.get(
                self.cloudflare_workers_url,
                headers=headers,
                timeout=10
            )

            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }

            # التحقق من CORS صارم
            if cors_headers['Access-Control-Allow-Origin'] == '*':
                cors_result['security_issue'] = 'CORS allows all origins'
                self.vulnerabilities.append({
                    'type': 'worker_cors_misconfig',
                    'severity': 'medium',
                    'description': 'Worker allows CORS from any origin'
                })
            else:
                cors_result['status'] = 'CORS properly configured'

        except Exception as e:
            cors_result['error'] = str(e)

        return cors_result

    async def _test_worker_error_handling(self, endpoint: str) -> List[Dict[str, Any]]:
        """اختبار معالجة الأخطاء في Workers"""
        vulnerabilities = []

        # إرسال طلبات غير صالحة
        invalid_requests = [
            f"{endpoint}?invalid_param=value",
            f"{endpoint}?id=invalid",
            f"{endpoint}?json={{malformed}}"
        ]

        for request in invalid_requests:
            try:
                response = requests.get(
                    f"{self.cloudflare_workers_url}{request}",
                    timeout=10
                )

                # التحقق من كشف معلومات حساسة في رسائل الخطأ
                if 'trace' in response.text.lower() or 'stack' in response.text.lower():
                    vulnerabilities.append({
                        'type': 'worker_information_disclosure',
                        'request': request,
                        'severity': 'medium',
                        'evidence': 'Stack trace or debug information disclosed'
                    })

            except Exception:
                continue

        return vulnerabilities

    # ===========================
    # 9. اختبارات عزل الفروع
    # ===========================

    async def test_branch_isolation_security(self, page: Page) -> Dict[str, Any]:
        """اختبار عزل بيانات الفروع"""
        print("🏢 اختبار عزل بيانات الفروع...")

        isolation_results = {
            'data_access_tests': [],
            'cross_branch_access': [],
            'privilege_escalation': [],
            'data_leakage': []
        }

        # اختبار الوصول إلى بيانات فرع آخر
        cross_branch_result = await self._test_cross_branch_data_access(page)
        isolation_results['cross_branch_access'] = cross_branch_result

        # اختبار تصعيد الصلاحيات
        privilege_result = await self._test_privilege_escalation(page)
        isolation_results['privilege_escalation'] = privilege_result

        # اختبار تسريب البيانات
        leakage_result = await self._test_data_leakage(page)
        isolation_results['data_leakage'] = leakage_result

        self.results['branch_isolation_tests'] = isolation_results
        return isolation_results

    async def _test_cross_branch_data_access(self, page: Page) -> Dict[str, Any]:
        """اختبار الوصول إلى بيانات فرع آخر"""
        cross_access_issues = []

        # محاولة الوصول إلى بيانات فرع لعبان من حساب طويق
        test_scenarios = [
            ('employee', 'طويق', 'لعبان'),
            ('supervisor', 'طويق', 'لعبان'),
            ('admin', 'طويق', 'لعبان')
        ]

        for role, from_branch, to_branch in test_scenarios:
            try:
                # محاولة الوصول إلى بيانات الفرع الآخر
                result = await self._attempt_branch_access(page, role, from_branch, to_branch)

                if result['access_granted']:
                    cross_access_issues.append({
                        'role': role,
                        'from_branch': from_branch,
                        'to_branch': to_branch,
                        'severity': 'critical',
                        'evidence': result['evidence']
                    })
                    self.vulnerabilities.append({
                        'type': 'branch_isolation_breach',
                        'role': role,
                        'from_branch': from_branch,
                        'to_branch': to_branch,
                        'severity': 'critical',
                        'description': f"{role} from {from_branch} can access {to_branch} data"
                    })

            except Exception as e:
                cross_access_issues.append({
                    'role': role,
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'error': str(e)
                })

        return {'issues': cross_access_issues, 'total_tests': len(test_scenarios)}

    async def _attempt_branch_access(self, page: Page, role: str, from_branch: str, to_branch: str) -> Dict[str, Any]:
        """محاولة الوصول إلى بيانات فرع آخر"""
        try:
            # تسجيل الدخول بحساب من الفرع الأول
            await page.goto(f"{self.base_url}/login")
            await page.fill('input[type="email"]', f"{role}@{from_branch}.com")
            await page.fill('input[type="password"]', "testpassword")
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(2000)

            # محاولة الوصول إلى بيانات الفرع الآخر
            await page.goto(f"{self.base_url}/api/branches/{to_branch}/revenue")

            await page.wait_for_timeout(2000)

            page_content = await page.content()

            # التحقق من الوصول إلى البيانات
            if 'revenue' in page_content.lower() or 'إيرادات' in page_content:
                return {
                    'access_granted': True,
                    'evidence': 'Successfully accessed branch revenue data'
                }
            elif 'unauthorized' in page_content.lower() or 'forbidden' in page_content.lower():
                return {
                    'access_granted': False,
                    'evidence': 'Access properly denied'
                }
            else:
                return {
                    'access_granted': False,
                    'evidence': 'Unclear access status'
                }

        except Exception as e:
            return {
                'access_granted': False,
                'evidence': f'Error during access attempt: {str(e)}'
            }

    async def _test_privilege_escalation(self, page: Page) -> Dict[str, Any]:
        """اختبار تصعيد الصلاحيات بين الفروع"""
        escalation_issues = []

        # محاولة تصعيد الصلاحيات
        escalation_tests = [
            ('employee', 'admin'),
            ('supervisor', 'admin'),
            ('partner', 'admin')
        ]

        for from_role, to_role in escalation_tests:
            try:
                result = await self._attempt_privilege_escalation(page, from_role, to_role)

                if result['escalation_successful']:
                    escalation_issues.append({
                        'from_role': from_role,
                        'to_role': to_role,
                        'severity': 'critical',
                        'evidence': result['evidence']
                    })
                    self.vulnerabilities.append({
                        'type': 'privilege_escalation',
                        'from_role': from_role,
                        'to_role': to_role,
                        'severity': 'critical',
                        'description': f"{from_role} can escalate to {to_role} privileges"
                    })

            except Exception as e:
                escalation_issues.append({
                    'from_role': from_role,
                    'to_role': to_role,
                    'error': str(e)
                })

        return {'issues': escalation_issues, 'total_tests': len(escalation_tests)}

    async def _attempt_privilege_escalation(self, page: Page, from_role: str, to_role: str) -> Dict[str, Any]:
        """محاولة تصعيد الصلاحيات"""
        try:
            # تسجيل الدخول بدور الأقل
            await page.goto(f"{self.base_url}/login")
            await page.fill('input[type="email"]', f"{from_role}@example.com")
            await page.fill('input[type="password"]', "testpassword")
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(2000)

            # محاولة الوصول إلى صفحة مخصصة للدور الأعلى
            await page.goto(f"{self.base_url}/admin/users")

            await page.wait_for_timeout(2000)

            page_content = await page.content()

            # التحقق من الوصول إلى صفحة الإدارة
            if 'users' in page_content.lower() or 'المستخدمين' in page_content:
                return {
                    'escalation_successful': True,
                    'evidence': 'Successfully accessed admin page'
                }
            elif 'access denied' in page_content.lower() or 'unauthorized' in page_content.lower():
                return {
                    'escalation_successful': False,
                    'evidence': 'Access properly denied'
                }
            else:
                return {
                    'escalation_successful': False,
                    'evidence': 'Unclear access status'
                }

        except Exception as e:
            return {
                'escalation_successful': False,
                'evidence': f'Error during escalation attempt: {str(e)}'
            }

    async def _test_data_leakage(self, page: Page) -> Dict[str, Any]:
        """اختبار تسريب البيانات بين الفروع"""
        leakage_issues = []

        # اختبار نقاط التسريب المحتملة
        leakage_tests = [
            '/api/users/all',  # الحصول على جميع المستخدمين
            '/api/revenue/all',  # الحصول على جميع الإيرادات
            '/api/expenses/all',  # الحصول على جميع المصروفات
            '/api/branches/all'   # الحصول على جميع الفروع
        ]

        for endpoint in leakage_tests:
            try:
                # تسجيل الدخول كمستخدم عادي
                await page.goto(f"{self.base_url}/login")
                await page.fill('input[type="email"]', "employee@example.com")
                await page.fill('input[type="password"]', "testpassword")
                await page.click('button[type="submit"]')

                await page.wait_for_timeout(2000)

                # محاولة الوصول إلى نقطة التسريب
                await page.goto(f"{self.base_url}{endpoint}")

                await page.wait_for_timeout(2000)

                page_content = await page.content()

                # التحقق من كشف البيانات
                if 'data' in page_content.lower() and len(page_content) > 1000:
                    leakage_issues.append({
                        'endpoint': endpoint,
                        'severity': 'high',
                        'evidence': 'Data potentially leaked through endpoint'
                    })
                    self.vulnerabilities.append({
                        'type': 'data_leakage',
                        'endpoint': endpoint,
                        'severity': 'high',
                        'description': f"Data leakage through endpoint: {endpoint}"
                    })

            except Exception as e:
                leakage_issues.append({
                    'endpoint': endpoint,
                    'error': str(e)
                })

        return {'issues': leakage_issues, 'total_tests': len(leakage_tests)}

    # ===========================
    # 10. اختبارات المزامنة الحقيقية
    # ===========================

    async def test_realtime_sync_security(self) -> Dict[str, Any]:
        """اختبار أمان المزامنة الحقيقية"""
        print("🔄 اختبار أمان المزامنة الحقيقية...")

        sync_results = {
            'websocket_security': [],
            'sync_validation': [],
            'message_integrity': [],
            'sync_auth': []
        }

        # اختبار أمان WebSocket
        websocket_result = await self._test_websocket_security()
        sync_results['websocket_security'] = websocket_result

        # اختبار تحقق المزامنة
        validation_result = await self._test_sync_validation()
        sync_results['sync_validation'] = validation_result

        # اختبار سلامة الرسائل
        integrity_result = await self._test_message_integrity()
        sync_results['message_integrity'] = integrity_result

        # اختبار مصادقة المزامنة
        auth_result = await self._test_sync_authentication()
        sync_results['sync_auth'] = auth_result

        self.results['realtime_sync_tests'] = sync_results
        return sync_results

    async def _test_websocket_security(self) -> Dict[str, Any]:
        """اختبار أمان WebSocket"""
        websocket_issues = []

        try:
            # اختبار الاتصال غير المصرح به
            unauthorized_result = await self._test_unauthorized_websocket()
            websocket_issues.append(unauthorized_result)

            # اختبار حقن في WebSocket
            injection_result = await self._test_websocket_injection()
            websocket_issues.append(injection_result)

            # اختبار تحديد المعدل في WebSocket
            rate_result = await self._test_websocket_rate_limiting()
            websocket_issues.append(rate_result)

        except Exception as e:
            websocket_issues.append({'error': str(e)})

        return {'security_issues': websocket_issues}

    async def _test_unauthorized_websocket(self) -> Dict[str, Any]:
        """اختبار الاتصال غير المصرح به بالـ WebSocket"""
        try:
            # محاولة الاتصال بدون مصادقة
            result = {'connection_attempted': True, 'connection_successful': False}

            # هذا اختبار وهمي - في الواقع سيحتاج إلى مكتبة WebSocket حقيقية
            # للتنفيذ الفعلي، نختبر من خلال API endpoints المتعلقة بال WebSocket

            response = requests.get(f"{self.base_url}/api/ws/info", timeout=10)

            if response.status_code == 200:
                result['connection_successful'] = True
                result['security_issue'] = 'WebSocket info endpoint accessible without auth'
                self.vulnerabilities.append({
                    'type': 'websocket_unauthorized_access',
                    'severity': 'medium',
                    'description': 'WebSocket information endpoint accessible without authentication'
                })

            return result

        except Exception as e:
            return {'error': str(e)}

    async def _test_websocket_injection(self) -> Dict[str, Any]:
        """اختبار حقن في WebSocket"""
        injection_issues = []

        # محاولات الحقن في WebSocket
        injection_payloads = [
            '{"type": "sync", "data": "<script>alert(\'xss\')</script>"}',
            '{"type": "update", "data": {"branch_id": "\' OR 1=1--"}}',
            '{"type": "message", "data": "{$ne: null}"}',
            '{"type": "sync", "data": "malicious_data"}'
        ]

        for payload in injection_payloads:
            try:
                # إرسال الحمولة إلى نقطة نهاية WebSocket
                response = requests.post(
                    f"{self.base_url}/api/ws/send",
                    json={'message': payload},
                    timeout=10
                )

                if response.status_code == 200:
                    injection_issues.append({
                        'payload': payload,
                        'severity': 'high',
                        'evidence': 'Payload accepted without validation'
                    })
                    self.vulnerabilities.append({
                        'type': 'websocket_injection',
                        'payload': payload,
                        'severity': 'high',
                        'description': f'WebSocket injection possible with payload: {payload[:50]}...'
                    })

            except Exception:
                continue

        return {'injection_attempts': len(injection_payloads), 'issues_found': len(injection_issues)}

    async def _test_websocket_rate_limiting(self) -> Dict[str, Any]:
        """اختبار تحديد المعدل في WebSocket"""
        try:
            # إرسال رسائل متعددة بسرعة
            messages_sent = 0
            blocked_messages = 0

            for i in range(50):  # 50 رسالة
                try:
                    response = requests.post(
                        f"{self.base_url}/api/ws/send",
                        json={'message': f'test_message_{i}'},
                        timeout=5
                    )

                    messages_sent += 1
                    if response.status_code in [429, 403]:
                        blocked_messages += 1
                        break

                except Exception:
                    continue

            return {
                'messages_sent': messages_sent,
                'messages_blocked': blocked_messages,
                'rate_limited': blocked_messages > 0
            }

        except Exception as e:
            return {'error': str(e)}

    async def _test_sync_validation(self) -> Dict[str, Any]:
        """اختبار تحقق المزامنة"""
        validation_issues = []

        # اختبار إرسال بيانات غير صالحة للمزامنة
        invalid_sync_data = [
            {'branch_id': 'invalid', 'data': 'test'},
            {'branch_id': 1, 'data': None},
            {'branch_id': 1, 'data': 'malicious<script>alert(1)</script>'},
            {'branch_id': 999, 'data': 'test'},  # فرع غير موجود
            {'branch_id': 1, 'data': {'malicious': 'data'}}
        ]

        for invalid_data in invalid_sync_data:
            try:
                response = requests.post(
                    f"{self.base_url}/api/sync/update",
                    json=invalid_data,
                    timeout=10
                )

                if response.status_code == 200:
                    validation_issues.append({
                        'data': invalid_data,
                        'severity': 'medium',
                        'evidence': 'Invalid sync data accepted'
                    })
                    self.vulnerabilities.append({
                        'type': 'sync_validation_bypass',
                        'data_type': type(invalid_data.get('data')).__name__,
                        'severity': 'medium',
                        'description': f'Sync validation bypassed with invalid data'
                    })

            except Exception:
                continue

        return {'validation_tests': len(invalid_sync_data), 'issues_found': len(validation_issues)}

    async def _test_message_integrity(self) -> Dict[str, Any]:
        """اختبار سلامة الرسائل في المزامنة"""
        integrity_issues = []

        # اختبار تعديل الرسائل أثناء النقل
        tampering_tests = [
            {'original': {'branch_id': 1, 'amount': 100}, 'tampered': {'branch_id': 1, 'amount': 999999}},
            {'original': {'user_id': 1, 'role': 'employee'}, 'tampered': {'user_id': 1, 'role': 'admin'}},
            {'original': {'sync_id': 'abc123'}, 'tampered': {'sync_id': 'malicious'}}
        ]

        for test in tampering_tests:
            try:
                # إرسال الرسالة المعدلة
                response = requests.post(
                    f"{self.base_url}/api/sync/message",
                    json=test['tampered'],
                    timeout=10
                )

                if response.status_code == 200:
                    integrity_issues.append({
                        'test_type': 'message_tampering',
                        'severity': 'high',
                        'evidence': 'Tampered message accepted'
                    })
                    self.vulnerabilities.append({
                        'type': 'message_integrity_breach',
                        'severity': 'high',
                        'description': 'Message integrity can be compromised during sync'
                    })

            except Exception:
                continue

        return {'integrity_tests': len(tampering_tests), 'issues_found': len(integrity_issues)}

    async def _test_sync_authentication(self) -> Dict[str, Any]:
        """اختبار مصادقة المزامنة"""
        auth_issues = []

        # اختبار المزامنة بدون مصادقة
        try:
            response = requests.post(
                f"{self.base_url}/api/sync/data",
                json={'test': 'data'},
                timeout=10
            )

            if response.status_code == 200:
                auth_issues.append({
                    'issue': 'Sync without authentication',
                    'severity': 'critical',
                    'evidence': 'Sync endpoint accessible without auth'
                })
                self.vulnerabilities.append({
                    'type': 'sync_authentication_bypass',
                    'severity': 'critical',
                    'description': 'Real-time sync possible without authentication'
                })

        except Exception as e:
            auth_issues.append({'error': str(e)})

        return {'auth_tests': 1, 'issues_found': len(auth_issues)}

    # ===========================
    # 11. اختبارات D1 Database
    # ===========================

    async def test_d1_database_security(self) -> Dict[str, Any]:
        """اختبار أمان قاعدة بيانات D1"""
        print("🗄️ اختبار أمان قاعدة بيانات D1...")

        d1_results = {
            'sql_injection': [],
            'data_access': [],
            'database_configuration': [],
            'backup_security': []
        }

        # اختبار حقن SQL في D1
        sql_injection_result = await self._test_d1_sql_injection()
        d1_results['sql_injection'] = sql_injection_result

        # اختبار الوصول إلى البيانات
        data_access_result = await self._test_d1_data_access()
        d1_results['data_access'] = data_access_result

        # اختبار إعدادات قاعدة البيانات
        config_result = await self._test_d1_configuration()
        d1_results['database_configuration'] = config_result

        self.results['d1_database_tests'] = d1_results
        return d1_results

    async def _test_d1_sql_injection(self) -> Dict[str, Any]:
        """اختبار حقن SQL في D1"""
        injection_issues = []

        # اختبارات حقن SQL خاصة بـ SQLite (D1)
        d1_injection_payloads = [
            "?branch_id=' UNION SELECT name, sql FROM sqlite_master--",
            "?user_id=1; SELECT COUNT(*) FROM users--",
            "?query=' OR 1=1--",
            "?data='; PRAGMA table_info(users); --",
            "?filter={'$where': 'function() { return true; }'}"
        ]

        for payload in d1_injection_payloads:
            try:
                response = requests.get(
                    f"{self.cloudflare_workers_url}/api/data{payload}",
                    timeout=10
                )

                if response.status_code >= 400:
                    continue

                # التحقق من وجود أخطاء أو استجابات غير متوقعة
                if 'error' in response.text.lower() or 'sqlite' in response.text.lower():
                    injection_issues.append({
                        'payload': payload,
                        'severity': 'critical',
                        'evidence': 'SQLite error or injection successful'
                    })
                    self.vulnerabilities.append({
                        'type': 'd1_sql_injection',
                        'payload': payload,
                        'severity': 'critical',
                        'description': f'D1 SQL injection possible with payload: {payload}'
                    })

            except Exception:
                continue

        return {'injection_attempts': len(d1_injection_payloads), 'vulnerabilities_found': len(injection_issues)}

    async def _test_d1_data_access(self) -> Dict[str, Any]:
        """اختبار الوصول إلى بيانات D1"""
        access_issues = []

        # محاولات الوصول المباشر إلى البيانات
        direct_access_tests = [
            '/api/d1/branches',
            '/api/d1/users',
            '/api/d1/revenue',
            '/api/d1/expenses'
        ]

        for endpoint in direct_access_tests:
            try:
                response = requests.get(
                    f"{self.cloudflare_workers_url}{endpoint}",
                    timeout=10
                )

                if response.status_code == 200:
                    access_issues.append({
                        'endpoint': endpoint,
                        'severity': 'high',
                        'evidence': 'Direct D1 access possible'
                    })
                    self.vulnerabilities.append({
                        'type': 'd1_direct_access',
                        'endpoint': endpoint,
                        'severity': 'high',
                        'description': f'Direct access to D1 data through {endpoint}'
                    })

            except Exception:
                continue

        return {'access_tests': len(direct_access_tests), 'issues_found': len(access_issues)}

    async def _test_d1_configuration(self) -> Dict[str, Any]:
        """اختبار إعدادات D1"""
        config_issues = []

        try:
            # اختبار الوصول إلى معلومات قاعدة البيانات
            response = requests.get(
                f"{self.cloudflare_workers_url}/api/d1/info",
                timeout=10
            )

            if response.status_code == 200:
                config_issues.append({
                    'issue': 'D1 database info exposed',
                    'severity': 'medium',
                    'evidence': 'Database configuration information accessible'
                })
                self.vulnerabilities.append({
                    'type': 'd1_info_disclosure',
                    'severity': 'medium',
                    'description': 'D1 database configuration information exposed'
                })

        except Exception as e:
            config_issues.append({'error': str(e)})

        return {'configuration_tests': 1, 'issues_found': len(config_issues)}

    # ===========================
    # أدوات مساعدة
    # ===========================

    def _calculate_severity(self, evidence: str) -> str:
        """حساب شدة الثغرة"""
        evidence_lower = evidence.lower()

        if any(keyword in evidence_lower for keyword in ['sql', 'database', 'stack trace', 'exception']):
            return 'critical'
        elif any(keyword in evidence_lower for keyword in ['xss', 'script', 'javascript']):
            return 'high'
        elif any(keyword in evidence_lower for keyword in ['error', 'warning', 'failed']):
            return 'medium'
        else:
            return 'low'

    async def _test_weak_password(self, page: Page, password: str) -> Dict[str, Any]:
        """اختبار كلمة مرور ضعيفة"""
        try:
            await page.goto(f"{self.base_url}/register")
            await page.fill('input[type="email"]', f"test_{password}@example.com")
            await page.fill('input[type="password"]', password)
            await page.fill('input[name="confirmPassword"]', password)
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(2000)

            page_content = await page.content()
            if 'success' in page_content.lower() or 'welcome' in page_content.lower():
                return {
                    'accepted': True,
                    'evidence': f"Weak password '{password}' was accepted"
                }

            return {
                'accepted': False,
                'evidence': f"Weak password '{password}' was rejected"
            }

        except Exception as e:
            return {
                'accepted': False,
                'evidence': f"Error testing password: {str(e)}"
            }

    # ===========================
    # حساب النتيجة النهائية
    # ===========================

    def calculate_security_score(self) -> float:
        """حساب درجة الأمان الإجمالية"""
        if not self.vulnerabilities:
            return 100.0

        # خصم نقاط بناءً على شدة الثغرات
        severity_penalties = {
            'critical': 20,
            'high': 15,
            'medium': 8,
            'low': 3
        }

        total_penalty = 0
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'medium')
            total_penalty += severity_penalties.get(severity, 5)

        self.security_score = max(0, 100 - total_penalty)
        return self.security_score

    # ===========================
    # تنفيذ الاختبارات الكاملة
    # ===========================

    async def run_security_tests(self) -> Dict[str, Any]:
        """تنفيذ جميع اختبارات الأمان لـ Cloudflare"""
        print("🚀 بدء اختبارات الأمان المتقدمة لـ Cloudflare...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            try:
                # 1. اختبارات الحقن
                await self.test_injection_attacks(page)

                # 2. اختبارات المصادقة
                await self.test_authentication_security(page)

                # 3. اختبارات الرؤوس الأمنية
                await self.test_security_headers()

                # 4. اختبارات CSRF
                await self.test_csrf_protection(page)

                # 5. اختبارات تحديد المعدل
                await self.test_rate_limiting()

                # 6. اختبارات البيانات الحساسة
                await self.test_sensitive_data_exposure(page)

                # 7. اختبارات API أمنية
                await self.test_api_security()

                # 8. اختبارات Cloudflare Workers
                await self.test_cloudflare_workers_security()

                # 9. اختبارات عزل الفروع
                await self.test_branch_isolation_security(page)

                # 10. اختبارات المزامنة الحقيقية
                await self.test_realtime_sync_security()

                # 11. اختبارات D1 Database
                await self.test_d1_database_security()

            finally:
                await browser.close()

        # حساب النتيجة النهائية
        final_score = self.calculate_security_score()

        # إنشاء تقرير الأمان
        security_report = self.generate_security_report(final_score)

        return {
            'score': final_score,
            'vulnerabilities': self.vulnerabilities,
            'results': self.results,
            'report': security_report
        }

    def generate_security_report(self, score: float) -> str:
        """إنشاء تقرير أمان مفصل"""
        report = f"""
================================================================================
                            BARBERTRACK SECURITY AUDIT REPORT
================================================================================
تاريخ الاختبار: {self.test_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
النظام: BarberTrack - نظام إدارة الصالونات متعددة الفروع
الهدف: تقييم أمان النظام واكتشاف الثغرات الأمنية

SECURITY SCORE SUMMARY
─────────────────────────────────────────────────────────────────────────────
درجة الأمان الإجمالية: {score:.1f}/100
حالة النظام: {'✅ آمن' if score >= 80 else '⚠️ يحتاج تحسينات' if score >= 60 else '❌ غير آمن'}
عدد الثغرات المكتشفة: {len(self.vulnerabilities)}

VULNERABILITY BREAKDOWN
─────────────────────────────────────────────────────────────────────────────
"""

        # تحليل الثغرات حسب الشدة
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'medium')
            severity_counts[severity] += 1

        report += f"""
🔴 Critical: {severity_counts['critical']} ثغرات
🟠 High: {severity_counts['high']} ثغرات
🟡 Medium: {severity_counts['medium']} ثغرات
🟢 Low: {severity_counts['low']} ثغرات

DETAILED VULNERABILITIES
─────────────────────────────────────────────────────────────────────────────
"""

        for i, vuln in enumerate(self.vulnerabilities, 1):
            severity_icon = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(vuln.get('severity', 'medium'), '⚪')

            report += f"""
{i:2d}. {severity_icon} {vuln.get('description', 'Unknown vulnerability')}
    النوع: {vuln.get('type', 'Unknown')}
    الشدة: {vuln.get('severity', 'medium')}
"""

        report += f"""

SECURITY RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────

🎯 HIGH PRIORITY (24 ساعة)
"""

        critical_vulns = [v for v in self.vulnerabilities if v.get('severity') == 'critical']
        high_vulns = [v for v in self.vulnerabilities if v.get('severity') == 'high']

        for vuln in critical_vulns[:5]:  # أول 5 ثغرات حرجة
            report += f"   • إصلاح ثغرة {vuln.get('type', 'security')}: {vuln.get('description', '')[:50]}...\n"

        report += f"""

📈 MEDIUM PRIORITY (أسبوع)
"""
        for vuln in high_vulns[:5]:  # أول 5 ثغرات عالية
            report += f"   • معالجة {vuln.get('type', 'security')}: {vuln.get('description', '')[:50]}...\n"

        if severity_counts['critical'] == 0 and severity_counts['high'] == 0:
            report += "   • نظام آمن نسبياً، استمر في المراقبة والتحديث\n"

        report += f"""

SECURITY BEST PRACTICES
─────────────────────────────────────────────────────────────────────────────
1. تحديث جميع المكتبات والإطارات بشكل منتظم
2. تنفيذ WAF (Web Application Firewall)
3. مراقبة السجلات الأمنية بشكل مستمر
4. إجراء اختبارات اختراق دورية
5. تدريب الموظفين على الأمان السيبراني
6. تنفيذ سياسات كلمات مرور قوية
7. استخدام التشفير للبيانات الحساسة

      report += f"""
CLOUDFLARE SECURITY RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────

🎯 WORKERS SECURITY (24 ساعة)
"""

        # توصيات Cloudflare
        worker_vulns = [v for v in self.vulnerabilities if 'worker' in v.get('type', '')]
        for vuln in worker_vulns[:3]:
            report += f"   • إصلاح ثغرة {vuln.get('type', 'worker')}: {vuln.get('description', '')[:50]}...\n"

        report += f"""

🏢 BRANCH ISOLATION (24 ساعة)
"""

        isolation_vulns = [v for v in self.vulnerabilities if 'branch' in v.get('type', '') or 'isolation' in v.get('type', '')]
        for vuln in isolation_vulns[:3]:
            report += f"   • معالجة {vuln.get('type', 'isolation')}: {vuln.get('description', '')[:50]}...\n"

        report += f"""

🔄 REAL-TIME SYNC SECURITY (48 ساعة)
"""

        sync_vulns = [v for v in self.vulnerabilities if 'sync' in v.get('type', '') or 'websocket' in v.get('type', '')]
        for vuln in sync_vulns[:3]:
            report += f"   • تأمين {vuln.get('type', 'sync')}: {vuln.get('description', '')[:50]}...\n"

        report += f"""

🗄️ D1 DATABASE SECURITY (48 ساعة)
"""

        d1_vulns = [v for v in self.vulnerabilities if 'd1' in v.get('type', '')]
        for vuln in d1_vulns[:3]:
            report += f"   • حماية {vuln.get('type', 'd1')}: {vuln.get('description', '')[:50]}...\n"

        report += f"""

CLOUDFLARE BEST PRACTICES
─────────────────────────────────────────────────────────────────────────────
1. تكوين Worker Security Headers بشكل صحيح
2. تطبيق Rate Limiting على جميع نقاط النهاية
3. استخدام JWT tokens لمصادقة Workers
4. تطبيق CORS صارمة
5. تشفير البيانات الحساسة قبل تخزينها في D1
6. تطبيق عزل الفروع على مستوى Workers
7. استخدام Web Application Firewall (WAF)
8. مراقبة سجلات Workers بشكل مستمر
9. تنفيذ سياسات أمان قوية للمزامنة الحقيقية
10. اختبار تحديثات الأمان بانتظام

CONCLUSION
─────────────────────────────────────────────────────────────────────────────
{'✅ النظام آمن للنشر' if score >= 85 else '⚠️ يحتاج النظام إلى تحسينات أمنية قبل النشر' if score >= 70 else '❌ النظام غير آمن ويحتاج إلى إصلاحات عاجلة'}

توصية: {'يمكن نشر النظام مع مراقبة أمنية مستمرة' if score >= 80 else 'يجب إصلاح الثغرات الحرجة والعالية قبل النشر'}
================================================================================
        """

        # حفظ التقرير
        report_path = 'test_results/security_audit_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

# نقطة الدخول الرئيسية
async def main():
    """نقطة الدخول الرئيسية"""
    print("🛡️ نظام اختبار الأمان المتقدم لـ BarberTrack")
    print("=" * 50)

    security_tester = SecurityTestSuite()

    try:
        results = await security_tester.run_security_tests()

        print(f"\n📊 درجة الأمان: {results['score']:.1f}/100")
        print(f"🔍 عدد الثغرات المكتشفة: {len(results['vulnerabilities'])}")

        if results['score'] >= 80:
            print("✅ النظام آمن نسبياً")
        elif results['score'] >= 60:
            print("⚠️ يحتاج النظام إلى تحسينات أمنية")
        else:
            print("❌ النظام يحتاج إلى إصلاحات أمنية عاجلة")

        print(f"\n📋 التقرير الكامل متوفر في: test_results/security_audit_report.txt")

    except Exception as e:
        print(f"❌ خطأ في تنفيذ اختبارات الأمان: {str(e)}")
        logging.error(f"Security test execution failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())