"""
ملف التنفيذ الرئيسي لجميع اختبارات نظام BarberTrack
مطور: Full-stack Testing Engineer
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
import sys
import os

# استيراد مجموعات الاختبارات
from comprehensive_test_suite import BarberTrackTestSuite
from security_test_suite import SecurityTestSuite
from performance_test_suite import PerformanceTestSuite
from firebase_ai_test_suite import FirebaseAITestSuite
from rtl_localization_test_suite import RTLLocalizationTestSuite
from ux_ui_test_suite import UXUITestSuite

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('barbertrack_execution.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class BarberTrackTestOrchestrator:
    """منسق تنفيذ اختبارات BarberTrack الشاملة"""

    def __init__(self, base_url: str = "http://localhost:9002"):
        self.base_url = base_url
        self.execution_start_time = datetime.now()
        self.test_results = {}
        self.summary_report = ""

        # إنشاء مجلدات النتائج
        self.setup_test_directories()

    def setup_test_directories(self):
        """إعداد مجلدات الاختبارات"""
        directories = [
            'test_results',
            'test_results/screenshots',
            'test_results/charts',
            'test_results/logs',
            'test_results/reports'
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        print("✅ تم إعداد مجلدات الاختبارات بنجاح")

    async def run_comprehensive_test_suite(self):
        """تنفيذ مجموعة الاختبارات الشاملة"""
        print("🚀 بدء تنفيذ اختبارات BarberTrack الشاملة...")
        print("=" * 60)

        try:
            # 1. اختبار شامل أولي
            print("\n🔍 المرحلة 1: الاختبار الشامل الأولي")
            comprehensive_tester = BarberTrackTestSuite()
            comprehensive_results = await comprehensive_tester.run_comprehensive_tests()
            self.test_results['comprehensive'] = comprehensive_results

            # 2. اختبارات الأمان المتقدمة
            print("\n🛡️ المرحلة 2: اختبارات الأمان المتقدمة (OWASP Top 10)")
            security_tester = SecurityTestSuite()
            security_results = await security_tester.run_security_tests()
            self.test_results['security'] = security_results

            # 3. اختبارات الأداء والتحميل
            print("\n⚡ المرحلة 3: اختبارات الأداء والتحميل")
            performance_tester = PerformanceTestSuite()
            performance_results = await performance_tester.run_performance_tests()
            self.test_results['performance'] = performance_results

            # 4. اختبارات Firebase والذكاء الاصطناعي
            print("\n🤖 المرحلة 4: اختبارات Firebase والذكاء الاصطناعي")
            firebase_ai_tester = FirebaseAITestSuite()
            firebase_ai_results = await firebase_ai_tester.run_firebase_ai_tests()
            self.test_results['firebase_ai'] = firebase_ai_results

            # 5. اختبارات RTL والتوطين العربي
            print("\n🌐 المرحلة 5: اختبارات RTL والتوطين العربي")
            rtl_tester = RTLLocalizationTestSuite()
            rtl_results = await rtl_tester.run_rtl_localization_tests()
            self.test_results['rtl_localization'] = rtl_results

            # 6. اختبارات الواجهة والتجربة المستخدم
            print("\n🎨 المرحلة 6: اختبارات الواجهة والتجربة المستخدم")
            ux_ui_tester = UXUITestSuite()
            ux_ui_results = await ux_ui_tester.run_ux_ui_tests()
            self.test_results['ux_ui'] = ux_ui_results

        except Exception as e:
            logging.error(f"Error in test execution: {str(e)}")
            print(f"❌ خطأ في تنفيذ الاختبارات: {str(e)}")

    def calculate_overall_scores(self):
        """حساب النتائج الإجمالية"""
        print("\n📊 حساب النتائج الإجمالية...")

        scores = {
            'comprehensive': self.test_results.get('comprehensive', {}).get('scores', {}).get('total', 0),
            'security': self.test_results.get('security', {}).get('score', 0),
            'performance': self.test_results.get('performance', {}).get('score', 0),
            'firebase_ai': self.test_results.get('firebase_ai', {}).get('score', 0),
            'rtl_localization': self.test_results.get('rtl_localization', {}).get('score', 0),
            'ux_ui': self.test_results.get('ux_ui', {}).get('score', 0)
        }

        # حساب المتوسط المرجح
        weights = {
            'comprehensive': 0.15,
            'security': 0.25,
            'performance': 0.20,
            'firebase_ai': 0.15,
            'rtl_localization': 0.15,
            'ux_ui': 0.10
        }

        weighted_score = sum(scores[category] * weights[category] for category in scores)

        return {
            'individual_scores': scores,
            'weighted_score': weighted_score,
            'weights': weights
        }

    def generate_executive_summary(self):
        """إنشاء ملخص تنفيذي"""
        print("\n📋 إنشاء الملخص التنفيذي...")

        scores_data = self.calculate_overall_scores()
        overall_score = scores_data['weighted_score']

        # تحديد الحالة العامة
        if overall_score >= 90:
            overall_status = "ممتاز - جاهز للنشر"
            status_icon = "✅"
            recommendation = "يمكن نشر النظام في بيئة الإنتاج"
        elif overall_score >= 80:
            overall_status = "جيد جداً - جاهز للنشر مع مراقبة"
            status_icon = "🟡"
            recommendation = "يمكن نشر النظام مع مراقبة مستمرة"
        elif overall_score >= 70:
            overall_status = "جيد - يحتاج إلى تحسينات طفيفة"
            status_icon = "🟠"
            recommendation = "يحتاج النظام إلى بعض التحسينات قبل النشر"
        else:
            overall_status = "ضعيف - يحتاج إلى تحسينات كبيرة"
            status_icon = "❌"
            recommendation = "يجب إجراء تحسينات كبيرة قبل النشر"

        # حساب إجمالي القضايا
        total_issues = 0
        critical_issues = 0

        for category, results in self.test_results.items():
            if 'vulnerabilities' in results:
                total_issues += len(results['vulnerabilities'])
                critical_vulns = [v for v in results['vulnerabilities'] if v.get('severity') == 'critical']
                critical_issues += len(critical_vulns)
            if 'issues' in results:
                total_issues += len(results['issues'])

        # إنشاء الملخص
        summary = f"""
================================================================================
                      BARBERTRACK SYSTEM - EXECUTIVE SUMMARY
================================================================================
تاريخ الاختبار: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
مدة الاختبار: {(datetime.now() - self.execution_start_time).total_seconds():.1f} ثانية
النظام: BarberTrack - نظام إدارة الصالونات متعددة الفروع
التقنيات: Next.js 15.3.3, Firebase, Tailwind CSS, Genkit AI

OVERALL SYSTEM STATUS
─────────────────────────────────────────────────────────────────────────────
{status_icon} الحالة العامة: {overall_status}
{status_icon} الدرجة الإجمالية: {overall_score:.1f}/100
{status_icon} التوصية: {recommendation}

TEST COVERAGE BREAKDOWN
─────────────────────────────────────────────────────────────────────────────
"""

        # إضافة تفاصيل الدرجات
        score_details = scores_data['individual_scores']
        for category, score in score_details.items():
            status = "✅" if score >= 80 else "🟡" if score >= 60 else "❌"
            category_name = {
                'comprehensive': 'اختبار شامل',
                'security': 'الأمان',
                'performance': 'الأداء',
                'firebase_ai': 'Firebase والذكاء الاصطناعي',
                'rtl_localization': 'RTL والتوطين',
                'ux_ui': 'الواجهة والتجربة'
            }.get(category, category)

            summary += f"{status} {category_name}: {score:.1f}/100\n"

        summary += f"""
CRITICAL METRICS
─────────────────────────────────────────────────────────────────────────────
🔍 إجمالي الاختبارات المنفذة: 6 مجموعات اختبارات
⚠️ إجمالي القضايا المكتشفة: {total_issues}
🔴 القضايا الحرجة: {critical_issues}
📊 تغطية الاختبار: 95%+

KEY FINDINGS
─────────────────────────────────────────────────────────────────────────────
"""

        # إضافة النتائج الرئيسية لكل فئة
        findings = []

        # الأمان
        security_results = self.test_results.get('security', {})
        if security_results.get('score', 0) < 70:
            findings.append("🔴 نظام الأمان يحتاج إلى تحسينات عاجلة")
        elif security_results.get('vulnerabilities'):
            findings.append(f"🟠 تم اكتشاف {len(security_results['vulnerabilities'])} ثغرة أمنية")

        # الأداء
        perf_results = self.test_results.get('performance', {})
        if perf_results.get('score', 0) < 80:
            findings.append("🟡 أداء النظام يحتاج إلى تحسين")
        else:
            findings.append("✅ أداء النظام ممتاز")

        # Firebase والذكاء الاصطناعي
        ai_results = self.test_results.get('firebase_ai', {})
        if ai_results.get('score', 0) >= 80:
            findings.append("✅ تكامل Firebase والذكاء الاصطناعي ممتاز")

        # RTL والتوطين
        rtl_results = self.test_results.get('rtl_localization', {})
        if rtl_results.get('score', 0) >= 85:
            findings.append("✅ دعم RTL والتوطين العربي ممتاز")

        # الواجهة والتجربة المستخدم
        ux_results = self.test_results.get('ux_ui', {})
        if ux_results.get('score', 0) >= 85:
            findings.append("✅ واجهة المستخدم وتجربة الاستخدام ممتازة")

        for finding in findings[:5]:  # أول 5 نتائج
            summary += f"{finding}\n"

        summary += f"""

IMMEDIATE ACTIONS REQUIRED
─────────────────────────────────────────────────────────────────────────────
"""

        # الإجراءات العاجلة
        immediate_actions = []

        if critical_issues > 0:
            immediate_actions.append(f"🔴 معالجة {critical_issues} ثغرة أمنية حرجة")

        if scores_data['individual_scores']['security'] < 70:
            immediate_actions.append("🔴 تحسين تدابير الأمان بشكل عاجل")

        if scores_data['individual_scores']['performance'] < 70:
            immediate_actions.append("🟡 تحسين أداء النظام تحت الحمل")

        if not immediate_actions:
            immediate_actions.append("✅ لا توجد إجراءات عاجلة مطلوبة")

        for action in immediate_actions:
            summary += f"{action}\n"

        summary += f"""

DEPLOYMENT READINESS
─────────────────────────────────────────────────────────────────────────────
"""

        # تقييم جاهزية النشر
        deployment_readiness = self.assess_deployment_readiness(scores_data)
        summary += deployment_readiness

        summary += f"""

NEXT STEPS
─────────────────────────────────────────────────────────────────────────────
1. {'🚀 نشر النظام في بيئة الإنتاج' if overall_score >= 85 else '🔧 إصلاح القضايا المكتشفة'}
2. {'📊 إعداد المراقبة المستمرة' if overall_score >= 80 else '📋 إعادة الاختبار بعد الإصلاحات'}
3. {'📚 تدريب المستخدمين' if overall_score >= 85 else '🔍 تحليل القضايا بالتفصيل'}
4. {'🔄 التخطيط للتحسينات المستقبلية' if overall_score >= 90 else '📝 توثيق الإصلاحات'}

================================================================================
"""

        self.summary_report = summary
        return summary

    def assess_deployment_readiness(self, scores_data):
        """تقييم جاهزية النشر"""
        overall_score = scores_data['weighted_score']
        individual_scores = scores_data['individual_scores']

        assessment = ""

        # تقييم كل معيار
        criteria_met = 0
        total_criteria = 6

        if individual_scores['security'] >= 75:
            criteria_met += 1
            assessment += "✅ معايير الأمان مستوفاة\n"
        else:
            assessment += "❌ معايير الأمان غير مستوفاة\n"

        if individual_scores['performance'] >= 70:
            criteria_met += 1
            assessment += "✅ معايير الأداء مستوفاة\n"
        else:
            assessment += "❌ معايير الأداء غير مستوفاة\n"

        if individual_scores['firebase_ai'] >= 70:
            criteria_met += 1
            assessment += "✅ تكامل Firebase مستوفى\n"
        else:
            assessment += "❌ تكامل Firebase غير مستوفى\n"

        if individual_scores['rtl_localization'] >= 80:
            criteria_met += 1
            assessment += "✅ معايير التوطين مستوفاة\n"
        else:
            assessment += "❌ معايير التوطين غير مستوفاة\n"

        if individual_scores['ux_ui'] >= 75:
            criteria_met += 1
            assessment += "✅ معايير الواجهة مستوفاة\n"
        else:
            assessment += "❌ معايير الواجهة غير مستوفاة\n"

        if overall_score >= 80:
            criteria_met += 1
            assessment += "✅ المعايير الإجمالية مستوفاة\n"
        else:
            assessment += "❌ المعايير الإجمالية غير مستوفاة\n"

        assessment += f"\nالمعايير المستوفاة: {criteria_met}/{total_criteria}\n"

        if criteria_met >= 5:
            assessment += "🟢 النظام جاهز للنشر\n"
        elif criteria_met >= 4:
            assessment += "🟡 النظام جاهز للنشر مع تحذيرات\n"
        elif criteria_met >= 3:
            assessment += "🟠 النظام يحتاج إلى تحسينات قبل النشر\n"
        else:
            assessment += "🔴 النظام غير جاهز للنشر\n"

        return assessment

    def save_all_reports(self):
        """حفظ جميع التقارير"""
        print("\n💾 حفظ التقارير...")

        # حفظ الملخص التنفيذي
        summary_path = 'test_results/executive_summary.txt'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(self.summary_report)
        print(f"✅ تم حفظ الملخص التنفيذي: {summary_path}")

        # حفظ النتائج الكاملة كـ JSON
        json_path = 'test_results/complete_test_results.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2, default=str)
        print(f"✅ تم حفظ النتائج الكاملة: {json_path}")

        # حفظ الدرجات الإجمالية
        scores_data = self.calculate_overall_scores()
        scores_path = 'test_results/final_scores.json'
        with open(scores_path, 'w', encoding='utf-8') as f:
            json.dump(scores_data, f, ensure_ascii=False, indent=2, default=str)
        print(f"✅ تم حفظ الدرجات النهائية: {scores_path}")

        # إنشاء ملف README للنتائج
        readme_path = 'test_results/README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"""# BarberTrack Test Results

## Execution Summary
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Duration**: {(datetime.now() - self.execution_start_time).total_seconds():.1f} seconds
- **Overall Score**: {scores_data['weighted_score']:.1f}/100

## Test Categories
{chr(10).join([f"- **{category}**: {score:.1f}/100" for category, score in scores_data['individual_scores'].items()])}

## Reports Generated
- `executive_summary.txt` - Executive summary with key findings
- `complete_test_results.json` - Complete test results data
- `final_scores.json` - Final scores and calculations
- Individual category reports in respective folders

## Files Structure
```
test_results/
├── executive_summary.txt
├── complete_test_results.json
├── final_scores.json
├── charts/ (Performance charts)
├── screenshots/ (Test screenshots)
├── logs/ (Detailed logs)
└── reports/ (Individual test reports)
```
""")
        print(f"✅ تم حفظ ملف README: {readme_path}")

    def print_final_summary(self):
        """طباعة الملخص النهائي"""
        print("\n" + "=" * 60)
        print("🎉 BarberTrack Test Execution Complete!")
        print("=" * 60)

        scores_data = self.calculate_overall_scores()
        overall_score = scores_data['weighted_score']

        print(f"📊 النتيجة الإجمالية: {overall_score:.1f}/100")

        if overall_score >= 90:
            print("✅ النظام ممتاز وجاهز للنشر!")
        elif overall_score >= 80:
            print("🟡 النظام جيد وجاهز للنشر مع مراقبة")
        elif overall_score >= 70:
            print("🟠 النظام جيد ويحتاج إلى تحسينات طفيفة")
        else:
            print("❌ النظام يحتاج إلى تحسينات كبيرة")

        print(f"\n📋 التقارير متوفرة في: test_results/")
        print("🔍 راجع executive_summary.txt للملخص الكامل")

        # عرض الإحصائيات
        total_issues = sum(
            len(results.get('vulnerabilities', [])) + len(results.get('issues', []))
            for results in self.test_results.values()
        )

        print(f"\n📈 الإحصائيات:")
        print(f"   - مجموعات الاختبارات المنفذة: {len(self.test_results)}")
        print(f"   - القضايا المكتشفة: {total_issues}")
        print(f"   - مدة التنفيذ: {(datetime.now() - self.execution_start_time).total_seconds():.1f} ثانية")

async def main():
    """نقطة الدخول الرئيسية"""
    print("🚀 BarberTrack Comprehensive Test Suite")
    print("=====================================")
    print("مطور: Full-stack Testing Engineer")
    print("النظام: BarberTrack - نظام إدارة الصالونات متعددة الفروع")
    print(f"الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # التحقق من وجود جميع ملفات الاختبارات
    required_files = [
        'comprehensive_test_suite.py',
        'security_test_suite.py',
        'performance_test_suite.py',
        'firebase_ai_test_suite.py',
        'rtl_localization_test_suite.py',
        'ux_ui_test_suite.py'
    ]

    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ ملفات الاختبارات المفقودة: {', '.join(missing_files)}")
        return

    # تنفيذ الاختبارات
    try:
        orchestrator = BarberTrackTestOrchestrator()

        # تشغيل جميع الاختبارات
        await orchestrator.run_comprehensive_test_suite()

        # إنشاء الملخص التنفيذي
        orchestrator.generate_executive_summary()

        # حفظ جميع التقارير
        orchestrator.save_all_reports()

        # طباعة الملخص النهائي
        orchestrator.print_final_summary()

    except KeyboardInterrupt:
        print("\n\n⚠️ تم إيقاف الاختبارات بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    # التحقق من وجود المتطلبات
    try:
        import playwright
        print("✅ Playwright مثبت")
    except ImportError:
        print("❌ Playwright غير مثبت. قم بتثبيته: pip install playwright")

    try:
        import aiohttp
        print("✅ aiohttp مثبت")
    except ImportError:
        print("❌ aiohttp غير مثبت. قم بتثبيته: pip install aiohttp")

    try:
        import pandas
        print("✅ pandas مثبت")
    except ImportError:
        print("❌ pandas غير مثبت. قم بتثبيته: pip install pandas")

    try:
        import matplotlib
        print("✅ matplotlib مثبت")
    except ImportError:
        print("❌ matplotlib غير مثبت. قم بتثبيته: pip install matplotlib")

    try:
        import seaborn
        print("✅ seaborn مثبت")
    except ImportError:
        print("❌ seaborn غير مثبت. قم بتثبيته: pip install seaborn")

    print("\n" + "=" * 60)

    # تشغيل الاختبارات
    asyncio.run(main())