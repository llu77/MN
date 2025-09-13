import { Banknote, Receipt, Users, ShoppingBag } from 'lucide-react';

export const dashboardCards = [
  {
    title: 'إجمالي الإيرادات',
    value: '45,231.89',
    change: '+20.1% عن الشهر الماضي',
    icon: Banknote,
  },
  {
    title: 'إجمالي المصروفات',
    value: '12,875.00',
    change: '+15.2% عن الشهر الماضي',
    icon: Receipt,
  },
  {
    title: 'الطلبات المعلقة',
    value: '12',
    change: '+5 منذ الأمس',
    icon: Users,
  },
  {
    title: 'المنتجات المباعة',
    value: '+573',
    change: '+19% عن الشهر الماضي',
    icon: ShoppingBag,
  },
];

export const monthlyChartData = [
  { month: 'يناير', revenue: 4000, expenses: 2400 },
  { month: 'فبراير', revenue: 3000, expenses: 1398 },
  { month: 'مارس', revenue: 5000, expenses: 9800 },
  { month: 'أبريل', revenue: 2780, expenses: 3908 },
  { month: 'مايو', revenue: 1890, expenses: 4800 },
  { month: 'يونيو', revenue: 2390, expenses: 3800 },
  { month: 'يوليو', revenue: 3490, expenses: 4300 },
  { month: 'أغسطس', revenue: 3650, expenses: 4100 },
  { month: 'سبتمبر', revenue: 3120, expenses: 3950 },
  { month: 'أكتوبر', revenue: 4230, expenses: 5100 },
  { month: 'نوفمبر', revenue: 4500, expenses: 5200 },
  { month: 'ديسمبر', revenue: 4890, expenses: 5500 },
];

export const recentTransactions = [
    { id: 'TXN001', type: 'إيرادات', amount: '99.00', method: 'نقداً', date: '2023-10-26' },
    { id: 'TXN002', type: 'مصروفات', amount: '25.00', method: 'بطاقة', date: '2023-10-26' },
    { id: 'TXN003', type: 'إيرادات', amount: '150.00', method: 'شبكة', date: '2023-10-25' },
    { id: 'TXN004', type: 'مصروفات', amount: '200.00', method: 'نقداً', date: '2023-10-24' },
    { id: 'TXN005', type: 'إيرادات', amount: '50.00', method: 'نقداً', date: '2023-10-24' },
];

export const branches = [
  { id: 'laban', name: 'فرع لبن', supervisor: 'عبدالحي جلال' },
  { id: 'tuwaiq', name: 'فرع طويق', supervisor: 'محمد اسماعيل' },
];

export const employees = [
  // Main Admin
  { id: 'admin1', name: 'عمر المطيري', email: 'nntn127@gmail.com', branchId: 'all', role: 'admin', avatar: '' },
  // Laban Branch
  { id: 'sup1', name: 'عبدالحي جلال', email: 'ab@gasah.com', branchId: 'laban', role: 'supervisor', avatar: '' },
  { id: 'emp1', name: 'محمود عماره', email: 'ma@gasah.com', branchId: 'laban', role: 'employee', avatar: '' },
  { id: 'emp2', name: 'السيد', email: 'sa@gasah.com', branchId: 'laban', role: 'employee', avatar: '' },
  { id: 'emp3', name: 'علاء ناصر', email: 'al@gasah.com', branchId: 'laban', role: 'employee', avatar: '' },
  { id: 'emp4', name: 'عمرو', email: 'om@gasah.com', branchId: 'laban', role: 'employee', avatar: '' },
  { id: 'partner1', name: 'عبدالله المطيري', email: 'Aa@gasah.com', branchId: 'laban', role: 'partner', avatar: '' },
  { id: 'partner2', name: 'سالم الوادعي', email: 'SS@gasah.com', branchId: 'laban', role: 'partner', avatar: '' },
  // Tuwaiq Branch
  { id: 'sup2', name: 'محمد اسماعيل', email: 'mo@tad.com', branchId: 'tuwaiq', role: 'supervisor', avatar: '' },
  { id: 'emp5', name: 'محمد واصر', email: 'mo1@tad.com', branchId: 'tuwaiq', role: 'employee', avatar: '' },
  { id: 'emp6', name: 'فارس', email: 'Fa@tad.com', branchId: 'tuwaiq', role: 'employee', avatar: '' },
  { id: 'emp7', name: 'سعيد', email: 'sa@tad.com', branchId: 'tuwaiq', role: 'employee', avatar: '' },
  { id: 'partner3', name: 'سعود الجريسي', email: 'SS@tad.com', branchId: 'tuwaiq', role: 'partner', avatar: '' },
];

export const requestTypes = [
  'طلب صرف متأخرات',
  'طلب سلفة',
  'طلب إجازة',
  'طلب استقالة',
  'طلب صيانة',
  'طلب مراجعة فاتورة',
];

export const employeeRequests = [
    { id: 'REQ001', employee: 'محمود عماره', avatar: '', type: 'طلب إجازة', date: '2023-11-01', status: 'قيد انتظار موافقة المشرف', details: {} },
    { id: 'REQ002', employee: 'محمد واصر', avatar: '', type: 'طلب سلفة', date: '2023-10-28', status: 'موافق عليه', details: { amount: 500 } },
    { id: 'REQ003', employee: 'عمرو', avatar: '', type: 'طلب إجازة', date: '2023-10-27', status: 'مرفوض', details: {} },
    { id: 'REQ004', employee: 'فارس', avatar: '', type: 'طلب استقالة', date: '2023-10-25', status: 'قيد انتظار موافقة الأدمن', details: {} },
    { id: 'REQ005', employee: 'محمود عماره', avatar: '', type: 'طلب صرف متأخرات', date: '2023-10-24', status: 'قيد انتظار موافقة المشرف', details: { amount: 1200 } },
    { id: 'REQ006', employee: 'عبدالحي جلال', avatar: '', type: 'طلب صيانة', date: '2023-10-23', status: 'قيد انتظار موافقة المشرف', details: { maintenanceDetails: 'المكيف لا يعمل' } },
];

export const bonusData = [
    { name: 'محمود عماره', week: 'الأسبوع الأول', revenue: 800, bonus: 50 },
    { name: 'السيد', week: 'الأسبوع الأول', revenue: 750, bonus: 50 },
    { name: 'محمود عماره', week: 'الأسبوع الثاني', revenue: 950, bonus: 100 },
    { name: 'السيد', week: 'الأسبوع الثاني', revenue: 800, bonus: 50 },
    { name: 'عمرو', week: 'الأسبوع الثاني', revenue: 500, bonus: 0 },
    { name: 'محمود عماره', week: 'الأسبوع الثالث', revenue: 1100, bonus: 100 },
    { name: 'السيد', week: 'الأسبوع الثالث', revenue: 900, bonus: 100 },
    { name: 'محمد واصر', week: 'الأسبوع الأول', revenue: 900, bonus: 100 },
    { name: 'محمد واصر', week: 'الأسبوع الثاني', revenue: 1200, bonus: 150 },
];

export const expenseCategoryList = [
    'اصدار/تجديد اقامه', 'تاشيره', 'اغراض محل', 'كهرباء', 'انترنت', 'ورق', 'رسوم حكوميه', 'تذكره طيران', 'مواصلات', 'صيانه', 'مخالفه', 'شهاده صحيه', 'صيانه سكن', 'ايجار محل', 'ايجار سكن', 'ملابس', 'نقل كفاله', 'تامين صحي', 'تحسينات', 'اغراض سكن'
];

export const recentExpenses = [
    { category: 'اغراض محل', amount: 150.00, method: 'بطاقة', description: 'مقصات جديدة' },
    { category: 'ايجار محل', amount: 2500.00, method: 'تحويل بنكي', description: 'الإيجار الشهري' },
    { category: 'كهرباء', amount: 300.00, method: 'بطاقة', description: 'فاتورة الكهرباء' },
    { category: 'صيانه', amount: 100.00, method: 'نقداً', description: 'إعلان على وسائل التواصل الاجتماعي' },
];

export const expenseCategories = [
    { category: 'ايجار محل', value: 45, fill: 'hsl(var(--chart-1))' },
    { category: 'كهرباء', value: 15, fill: 'hsl(var(--chart-2))' },
    { category: 'اغراض محل', value: 25, fill: 'hsl(var(--chart-3))' },
    { category: 'تامين صحي', value: 10, fill: 'hsl(var(--chart-4))' },
    { category: 'صيانه', value: 5, fill: 'hsl(var(--chart-5))' },
];


export const employeePerformance = [
    { name: 'محمود عماره', revenue: 2850, bonus: 250, avatar: '' },
    { name: 'السيد', revenue: 2450, bonus: 200, avatar: '' },
    { name: 'فارس', revenue: 2000, bonus: 150, avatar: '' },
    { name: 'عمرو', revenue: 1500, bonus: 50, avatar: '' },
    { name: 'علاء ناصر', revenue: 1200, bonus: 50, avatar: '' },
];

export const productCatalog = [
  { id: 'p1', name: 'بلاديكس أمواس أزرق', price: 24 },
  { id: 'p2', name: 'مناشف استخدام مره واحده 50×100', price: 21 },
  { id: 'p3', name: 'كرات قطن', price: 3 },
  { id: 'p4', name: 'أعواد قطن أزرق', price: 4 },
  { id: 'p5', name: 'شمع بابز أسود أو أزرق', price: 41 },
  { id: 'p6', name: 'مناشف منعشه 25', price: 12 },
  { id: 'p7', name: 'جل حلاقة ازرق sahon', price: 5 },
  { id: 'p8', name: 'سفنج لتنظيف البشرة 12 حبه', price: 9 },
  { id: 'p9', name: 'واكس للشعر', price: 27 },
  { id: 'p10', name: 'مناديل رول نظافه', price: 8 },
  { id: 'p11', name: 'مناديل بلاتينا 600 حبه', price: 34 },
  { id: 'p12', name: 'قطن', price: 3 },
  { id: 'p13', name: 'واكس سستم أعود خشبيه 50حبه', price: 3 },
  { id: 'p14', name: 'مريله بلاستك أصفر كرتون', price: 41 },
  { id: 'p15', name: 'ورق رقبه', price: 10 },
  { id: 'p16', name: 'قفازات أسود مقاس اكس لارج 100', price: 9 },
  { id: 'p17', name: 'قفازات أسود مقاس لارج 100', price: 9 },
  { id: 'p18', name: 'ليمون منظف للوجه', price: 3 },
  { id: 'p19', name: 'ماكينة تنعيم', price: 20 },
  { id: 'p20', name: 'تونك أسود لملئ الفراغات', price: 12 },
  { id: 'p21', name: 'صابون للارضيات', price: 9 },
  { id: 'p22', name: 'لمبه لجهاز التعقيم', price: 5 },
  { id: 'p23', name: 'زيت دقن', price: 20 },
  { id: 'p24', name: 'غطاء رأس لحمام الزيت', price: 5 },
  { id: 'p25', name: 'أسبريه ملمع', price: 12 },
  { id: 'p26', name: 'كمامات', price: 7 },
  { id: 'p27', name: 'ديتول / منظف أرضيات', price: 23 },
  { id: 'p28', name: 'مرايه', price: 12 },
  { id: 'p29', name: 'أسبريه مثبت للشعر', price: 16 },
  { id: 'p30', name: 'مناشف منشفه منعشه لافاندر', price: 23 },
  { id: 'p31', name: 'شامبو فاتيكا', price: 9 },
  { id: 'p32', name: 'أمشاط تدريج', price: 10 },
  { id: 'p33', name: 'ماسك طين', price: 15 },
  { id: 'p34', name: 'ماسك نعناع', price: 15 },
  { id: 'p35', 'name': 'ماسك خيار', price: 15 },
  { id: 'p36', name: 'ماسك فحم', price: 15 },
  { id: 'p37', name: 'ماسك فراوله', price: 15 },
  { id: 'p38', name: 'ماسك قهوه', price: 15 },
  { id: 'p39', name: 'بودره', price: 5 },
  { id: 'p40', name: 'شمع', price: 44 },
  { id: 'p41', name: 'لزقة انف 20 حبه', price: 5 },
  { id: 'p42', name: 'اكياس نفايات اصفر 10/8 جالون', price: 6 },
  { id: 'p43', name: 'اكياس نفايات اسود 50 جالون', price: 8 },
  { id: 'p44', name: 'صبغه راس بني غامق 303', price: 15 },
  { id: 'p45', name: 'صبغه دقن بني غامق ابل', price: 15 },
  { id: 'p46', name: 'حنى اسود', price: 11 },
  { id: 'p47', name: 'حمام زيت', price: 15 },
  { id: 'p48', name: 'معطر 500 مل', price: 150 },
  { id: 'p49', name: 'سيروم فيتامين سي', price: 15 },
  { id: 'p50', name: 'سيروم كولاجين', price: 15 },
  { id: 'p51', name: 'مشط بلاستيك', price: 5 },
  { id: 'p52', name: 'امشاط بلاستيك', price: 15 },
  { id: 'p53', name: 'علبه بخاخه ماء', price: 6 },
  { id: 'p54', name: 'مقص حلاقة 5/5', price: 20 },
  { id: 'p55', name: 'مقص حلاقة 6', price: 25 },
  { id: 'p56', name: 'مكنسه للارضيات', price: 10 },
  { id: 'p57', name: 'فتالة ممسحه ارضيات', price: 10 },
];

export let productOrders = [
    { 
        orderId: 'ORD-001', 
        customer: 'نادي السادة', 
        date: '2023-10-26', 
        total: 1113.00, 
        items: [
            { productId: 'p1', name: 'بلاديكس أمواس أزرق', quantity: 10, price: 24 },
            { productId: 'p5', name: 'شمع بابز أسود أو أزرق', quantity: 20, price: 41 },
        ],
        subtotal: 1060,
        vat: 53,
    },
    { 
        orderId: 'ORD-002', 
        customer: 'الشارب', 
        date: '2023-10-25', 
        total: 829.50, 
        items: [
            { productId: 'p7', name: 'جل حلاقة ازرق sahon', quantity: 50, price: 5 },
            { productId: 'p9', name: 'واكس للشعر', quantity: 20, price: 27 },
        ],
        subtotal: 790,
        vat: 39.5,
    },
    { 
        orderId: 'ORD-003', 
        customer: 'بليد آند بريستل', 
        date: '2023-10-24', 
        total: 2100.00, 
        items: [
            { productId: 'p19', name: 'ماكينة تنعيم', quantity: 100, price: 20 },
        ],
        subtotal: 2000,
        vat: 100,
    },
    { 
        orderId: 'ORD-004', 
        customer: 'Sharp Cuts', 
        date: '2023-10-22', 
        total: 472.50, 
        items: [
            { productId: 'p54', name: 'مقص حلاقة 5/5', quantity: 10, price: 20 },
            { productId: 'p55', name: 'مقص حلاقة 6', quantity: 10, price: 25 },
        ],
        subtotal: 450,
        vat: 22.5,
    },
];

export const notifications = [
    {
        id: 'notif1',
        sender: 'عبدالحي جلال',
        avatar: '',
        message: 'تمت الموافقة على طلب الإجازة الخاص بمحمود عماره.',
        timestamp: 'قبل 5 دقائق',
    },
    {
        id: 'notif2',
        sender: 'النظام',
        avatar: '',
        message: 'تم إنشاء تقرير الإيرادات الشهري بنجاح.',
        timestamp: 'قبل ساعة واحدة',
    },
    {
        id: 'notif3',
        sender: 'محمد اسماعيل',
        avatar: '',
        message: 'طلب جديد للسلفة من محمد واصر.',
        timestamp: 'قبل 3 ساعات',
    },
    {
        id: 'notif4',
        sender: 'عمر المطيري',
        avatar: '',
        message: 'تم رفض طلب صيانة مكيف فرع لبن.',
        timestamp: 'أمس',
    },
];
    
export const dailyEntries = [
    {
        branch: 'laban',
        date: new Date('2023-10-27'),
        cash: 550.00,
        network: 320.50,
        employeeSplits: [
            { employeeId: 'emp1', amount: 450 },
            { employeeId: 'emp2', amount: 420.50 },
        ]
    },
    {
        branch: 'tuwaiq',
        date: new Date('2023-10-26'),
        cash: 780.00,
        network: 450.00,
        employeeSplits: [
             { employeeId: 'emp5', amount: 1230.00 },
        ]
    }
];

    




