'use client';
import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { useToast } from '@/hooks/use-toast';
import { Printer } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';
import { Icons } from '@/components/icons';

const expenseSchema = z.object({
  branch: z.string().min(1, 'الفرع مطلوب.'),
  category: z.string().min(1, 'الفئة مطلوبة.'),
  paymentMethod: z.string().min(1, 'طريقة الدفع مطلوبة.'),
  amount: z.coerce.number().positive('يجب أن يكون المبلغ رقمًا موجبًا.'),
  description: z.string().optional(),
});

type ExpenseFormValues = z.infer<typeof expenseSchema>;

const chartConfig = {};


export default function ExpensesPage() {
  const { user } = useAuth();
  const { recentExpenses, addExpense, branches, expenseCategoryList, expenseCategories } = useData();
  const { toast } = useToast();
  const userBranch = branches.find(b => b.id === user.branchId);
  
  expenseCategories.forEach(item => {
    chartConfig[item.category] = { label: item.category, color: item.fill };
});

  const form = useForm<ExpenseFormValues>({
    resolver: zodResolver(expenseSchema),
    defaultValues: {
        branch: user.role === 'supervisor' ? user.branchId : '',
        category: '',
        paymentMethod: '',
        amount: 0,
        description: '',
    }
  });

  useEffect(() => {
    if (user.role === 'supervisor' && user.branchId) {
      form.setValue('branch', user.branchId);
    }
  }, [user.role, user.branchId, form]);

  function onSubmit(data: ExpenseFormValues) {
    const newExpense = {
        category: data.category,
        amount: data.amount,
        method: data.paymentMethod,
        description: data.description || 'لا يوجد وصف',
    };
    addExpense(newExpense);
    
    toast({
      title: "نجاح",
      description: "تم تسجيل المصروف بنجاح.",
      variant: "default",
    });

    form.reset({
        branch: user.role === 'supervisor' ? user.branchId : '',
        category: '',
        paymentMethod: '',
        amount: 0,
        description: ''
    });
  }
  
  const handlePrint = () => {
    const printContent = document.getElementById('expenses-print-area');
    if (printContent) {
      const printWindow = window.open('', '_blank');
      printWindow.document.write('<html><head><title>تقرير المصروفات</title>');
      printWindow.document.write('<link rel="stylesheet" href="/globals.css" type="text/css" media="all"/>');
      printWindow.document.head.insertAdjacentHTML('beforeend', `
        <style>
          @import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap');
          body { 
            direction: rtl; 
            font-family: 'PT Sans', sans-serif; 
            background-color: white !important; 
            color: black !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          .print-container { padding: 2rem; }
          .print-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #6d28d9; padding-bottom: 1rem; margin-bottom: 2rem; }
          .print-header .logo { font-size: 1.5rem; font-weight: bold; color: #6d28d9; display: flex; align-items: center; gap: 0.5rem;}
          .print-header h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #374151; }
          .print-header p { font-size: 1rem; color: #666; }
          table { width: 100%; border-collapse: collapse; font-size: 1rem; margin-top: 2rem; }
          th, td { border: 1px solid #ddd; padding: 0.75rem; text-align: right; }
          th { background-color: #f2f2f2; }
          .print-footer { text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ccc; font-size: 0.8rem; color: #666; position: fixed; bottom: 0; width: 100%; }
          .no-print { display: none !important; }
          .chart-print-container { page-break-inside: avoid; margin-bottom: 2rem; }
          .card-header-print { padding: 1rem; border-bottom: 1px solid #eee; }
        </style>
      `);
      printWindow.document.write('</head><body dir="rtl">');
      
       const header = `
        <div class="print-header">
          <div class="logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-8"><path d="M14.5 6.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0z"></path><path d="M12 18H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h1"></path><path d="M7 14h1.5"></path><path d="M7 10h1"></path><path d="m17 10-5.5 5.5"></path><path d="m22 15-5.5-5.5"></path><path d="M12 22v-4"></path><path d="M17 10h.01"></path><path d="M22 15h.01"></path></svg> <span>BarberTrack</span></div>
          <div>
            <h1>تقرير المصروفات</h1>
            <p>فرع: ${userBranch?.name || 'كل الفروع'} - المشرف: ${user.name}</p>
          </div>
        </div>
      `;

      const footer = `<div class="print-footer"><p>BarberTrack | contact@barbertrack.com | +966 12 345 6789</p></div>`;

      printWindow.document.body.innerHTML = `<div class="print-container">${header}${printContent.innerHTML}${footer}</div>`;

      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 500);
    }
  };

  return (
    <div className="grid gap-8 lg:grid-cols-5">
        <div className="lg:col-span-3">
            <Card>
                <CardHeader className="flex flex-row justify-between items-start no-print">
                    <div>
                        <CardTitle>المصروفات الأخيرة</CardTitle>
                        <CardDescription>قائمة بآخر المصروفات المسجلة في الفرع.</CardDescription>
                    </div>
                     <Button variant="outline" onClick={handlePrint}>
                        <Printer className="ml-2 h-4 w-4" />
                        طباعة
                    </Button>
                </CardHeader>
                <CardContent id="expenses-print-area">
                    <div className="grid gap-8">
                       <div className="chart-print-container">
                            <div className="card-header-print">
                                <h3>توزيع المصروفات</h3>
                            </div>
                             <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[250px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <ChartTooltip content={<ChartTooltipContent nameKey="category" />} />
                                        <Pie data={expenseCategories} dataKey="value" nameKey="category" cx="50%" cy="50%" innerRadius={60} outerRadius={80} strokeWidth={2}>
                                        {expenseCategories.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.fill} />
                                        ))}
                                        </Pie>
                                    </PieChart>
                                </ResponsiveContainer>
                            </ChartContainer>
                       </div>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                <TableHead>الفئة</TableHead>
                                <TableHead>المبلغ</TableHead>
                                <TableHead>طريقة الدفع</TableHead>
                                <TableHead className="text-left">الوصف</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {recentExpenses.map((expense, index) => (
                                <TableRow key={index}>
                                    <TableCell>{expense.category}</TableCell>
                                    <TableCell>ر.س {expense.amount.toFixed(2)}</TableCell>
                                    <TableCell>{expense.method}</TableCell>
                                    <TableCell className="text-left">{expense.description}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>
        </div>
      <div className="lg:col-span-2 no-print">
        <Card>
          <CardHeader>
            <CardTitle>تسجيل مصروف جديد</CardTitle>
            <CardDescription>أدخل تفاصيل المصروف الجديد.</CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                  control={form.control}
                  name="branch"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>الفرع</FormLabel>
                      <Select 
                        onValueChange={field.onChange} 
                        value={field.value} 
                        disabled={user.role === 'supervisor'}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="اختر فرعًا" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                           {branches.map(branch => <SelectItem key={branch.id} value={branch.id}>{branch.name}</SelectItem>)}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                 <FormField
                  control={form.control}
                  name="category"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>فئة المصروف</FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                          <SelectTrigger><SelectValue placeholder="اختر فئة" /></SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {expenseCategoryList.map(category => <SelectItem key={category} value={category}>{category}</SelectItem>)}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="paymentMethod"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>طريقة الدفع</FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                          <SelectTrigger><SelectValue placeholder="اختر طريقة" /></SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="نقداً">نقداً</SelectItem>
                          <SelectItem value="شبكة">شبكة</SelectItem>
                          <SelectItem value="تحويل بنكي">تحويل بنكي</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="amount"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>المبلغ (ر.س)</FormLabel>
                      <FormControl>
                        <Input type="number" placeholder="0.00" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="description"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>وصف قصير (اختياري)</FormLabel>
                      <FormControl>
                        <Input placeholder="مثال: شراء أدوات جديدة" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button type="submit" className="w-full">تسجيل المصروف</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
