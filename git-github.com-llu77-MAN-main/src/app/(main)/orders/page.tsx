'use client';

import { useState, useEffect, useMemo } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { PlusCircle, Trash2, FileText, Printer } from 'lucide-react';
import { cn } from '@/lib/utils';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Form, FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Icons } from '@/components/icons';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';

const orderSchema = z.object({
  customer: z.string().min(1, 'اسم العميل مطلوب'),
  items: z.array(z.object({
    productId: z.string().min(1, 'المنتج مطلوب'),
    quantity: z.coerce.number().min(1, 'يجب أن تكون الكمية 1 على الأقل'),
  })).min(1, 'يجب أن يحتوي الطلب على عنصر واحد على الأقل'),
});
type OrderFormValues = z.infer<typeof orderSchema>;

function CreateOrderForm({ setOpen, onCreateOrder }) {
    const { productCatalog } = useData();
  const form = useForm<OrderFormValues>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      customer: '',
      items: [{ productId: '', quantity: 1 }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "items",
  });

  const watchedItems = form.watch('items');
  const {subtotal, vat, total, fullItems} = watchedItems.reduce((acc, item) => {
    const product = productCatalog.find(p => p.id === item.productId);
    const quantity = item.quantity || 0;
    const itemTotal = product ? product.price * quantity : 0;
    acc.subtotal += itemTotal;
    if (product) {
        acc.fullItems.push({ ...product, quantity });
    }
    return acc;
  }, { subtotal: 0, vat: 0, total: 0, fullItems: [] });

  const calculatedVat = subtotal * 0.05;
  const calculatedTotal = subtotal + calculatedVat;


  function onSubmit(data: OrderFormValues) {
    onCreateOrder({
      customer: data.customer,
      items: fullItems,
      subtotal: subtotal,
      vat: calculatedVat,
      total: calculatedTotal,
    });
    form.reset();
    setOpen(false);
  }
  
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="customer"
          render={({ field }) => (
            <FormItem>
              <Label>اسم العميل</Label>
              <FormControl>
                <Input placeholder="مثال: نادي السادة" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <div>
          <Label>المنتجات</Label>
          <div className="space-y-4 mt-2 max-h-60 overflow-y-auto pr-2">
            {fields.map((field, index) => (
              <div key={field.id} className="flex items-start gap-2">
                <FormField
                  control={form.control}
                  name={`items.${index}.productId`}
                  render={({ field }) => (
                    <FormItem className="flex-1">
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl><SelectTrigger><SelectValue placeholder="اختر منتج" /></SelectTrigger></FormControl>
                        <SelectContent><SelectContent>
                          {productCatalog.map(p => <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>)}
                        </SelectContent></SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`items.${index}.quantity`}
                  render={({ field }) => (
                    <FormItem>
                      <FormControl><Input type="number" placeholder="الكمية" {...field} className="w-24" /></FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                 <div className="flex items-center h-10">
                    <Button type="button" variant="ghost" size="icon" onClick={() => remove(index)} disabled={fields.length <= 1}>
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                </div>
              </div>
            ))}
          </div>
           <Button type="button" variant="outline" size="sm" onClick={() => append({ productId: '', quantity: 1 })} className="mt-4">
              <PlusCircle className="ml-2 h-4 w-4" /> أضف منتج
            </Button>
        </div>

        <Separator />
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-muted-foreground">المجموع الفرعي:</span><span>ر.س {subtotal.toFixed(2)}</span></div>
          <div className="flex justify-between"><span className="text-muted-foreground">ضريبة القيمة المضافة (5%):</span><span>ر.س {calculatedVat.toFixed(2)}</span></div>
          <div className="flex justify-between font-bold text-base"><span>المجموع:</span><span>ر.س {calculatedTotal.toFixed(2)}</span></div>
        </div>

        <DialogFooter>
          <Button type="submit">إنشاء طلب</Button>
        </DialogFooter>
      </form>
    </Form>
  );
}

export default function OrdersPage() {
  const { user } = useAuth();
  const { branches, productOrders, createProductOrder } = useData();
  const [openCreate, setOpenCreate] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  
  const userBranch = useMemo(() => {
      if (user.role === 'admin') return { name: 'كل الفروع' };
      return branches.find(b => b.id === user.branchId);
  }, [branches, user]);


  const handleCreateOrder = (newOrderData) => {
    createProductOrder(newOrderData);
  };


  const handlePrint = () => {
    const printContent = document.getElementById('orders-print-area');
    if (printContent) {
      const printWindow = window.open('', '_blank');
      printWindow.document.write('<html><head><title>تقرير طلبات المنتجات</title>');
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
          .print-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #673ab7; padding-bottom: 1rem; margin-bottom: 2rem; }
          .print-header .logo { font-size: 1.5rem; font-weight: bold; color: #673ab7; display: flex; align-items: center; gap: 0.5rem;}
          .print-header h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #374151; }
          .print-header p { font-size: 1rem; color: #666; }
          table { width: 100%; border-collapse: collapse; font-size: 1rem; }
          th, td { border: 1px solid #ddd; padding: 0.75rem; text-align: right; }
          th { background-color: #f2f2f2; }
          .print-footer { text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ccc; font-size: 0.8rem; color: #666; position: fixed; bottom: 0; width: 100%; }
          .no-print { display: none !important; }
        </style>
      `);
      printWindow.document.write('</head><body dir="rtl">');
      
      const header = `
        <div class="print-header">
          <div class="logo"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-8"><path d="M14.5 6.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0z"></path><path d="M12 18H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h1"></path><path d="M7 14h1.5"></path><path d="M7 10h1"></path><path d="m17 10-5.5 5.5"></path><path d="m22 15-5.5-5.5"></path><path d="M12 22v-4"></path><path d="M17 10h.01"></path><path d="M22 15h.01"></path></svg> <span>BarberTrack</span></div>
          <div>
            <h1>تقرير طلبات المنتجات</h1>
            <p>فرع: ${userBranch?.name} - المستخدم: ${user.name}</p>
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
  
  const handleInvoicePrint = () => {
    const content = document.getElementById('invoice-print-area');
    if (!content) return;

    const iframe = document.createElement('iframe');
    iframe.style.position = 'absolute';
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = 'none';
    document.body.appendChild(iframe);

    const doc = iframe.contentWindow.document;
    doc.open();
    doc.write('<html><head><title>طباعة الفاتورة</title>');
    
    // Copy all stylesheets from the main document to the iframe
    Array.from(document.styleSheets).forEach(styleSheet => {
      try {
        if (styleSheet.href) {
          const link = doc.createElement('link');
          link.rel = 'stylesheet';
          link.type = 'text/css';
          link.href = styleSheet.href;
          doc.head.appendChild(link);
        } else if (styleSheet.cssRules) {
          const style = doc.createElement('style');
          style.textContent = Array.from(styleSheet.cssRules)
            .map(rule => rule.cssText)
            .join('\n');
          doc.head.appendChild(style);
        }
      } catch (e) {
        console.warn('Could not copy stylesheet:', e);
      }
    });

    doc.write('</head><body dir="rtl">');
    doc.write('<div class="print-invoice-container p-8">'); // Add padding for better print layout
    doc.write(content.innerHTML);
    doc.write('</div></body></html>');
    doc.close();

    // Add a small delay to ensure everything is rendered, especially external stylesheets
    setTimeout(() => {
      iframe.contentWindow.focus();
      iframe.contentWindow.print();
      document.body.removeChild(iframe);
    }, 1000);
  };


  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start no-print">
        <div>
          <h1 className="text-3xl font-bold tracking-tight font-headline">طلبات المنتجات</h1>
          <p className="text-muted-foreground">إنشاء وإدارة طلبات المنتجات والمستلزمات.</p>
        </div>
        <div className="flex gap-2">
            <Dialog open={openCreate} onOpenChange={setOpenCreate}>
                <DialogTrigger asChild>
                    <Button><PlusCircle className="ml-2 h-4 w-4" />إنشاء طلب</Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                    <DialogHeader>
                        <DialogTitle>إنشاء طلب جديد</DialogTitle>
                    </DialogHeader>
                    <CreateOrderForm setOpen={setOpenCreate} onCreateOrder={handleCreateOrder} />
                </DialogContent>
            </Dialog>
        </div>
      </header>

      <Card>
        <CardHeader>
          <CardTitle>سجل الطلبات</CardTitle>
          <CardDescription>قائمة بجميع طلبات المنتجات السابقة والحالية.</CardDescription>
        </CardHeader>
        <CardContent>
          <div id="orders-print-area">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>معرف الطلب</TableHead>
                    <TableHead>العميل</TableHead>
                    <TableHead>التاريخ</TableHead>
                    <TableHead className="text-left">المجموع</TableHead>
                    <TableHead className="text-left no-print">
                        <div className="flex items-center justify-end gap-2">
                            الإجراءات
                            <Button variant="ghost" size="icon" onClick={handlePrint} className="h-8 w-8">
                                <Printer className="h-4 w-4" />
                            </Button>
                        </div>
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {productOrders.map((order) => (
                    <TableRow key={order.orderId}>
                      <TableCell className="font-medium">{order.orderId}</TableCell>
                      <TableCell>{order.customer}</TableCell>
                      <TableCell>{order.date}</TableCell>
                      <TableCell className="text-left">ر.س {order.total.toFixed(2)}</TableCell>
                      <TableCell className="text-left no-print">
                        <Button variant="ghost" size="icon" onClick={() => setSelectedOrder(order)}>
                          <FileText className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
          </div>
        </CardContent>
      </Card>
      
      {selectedOrder && (
        <Dialog open={!!selectedOrder} onOpenChange={() => setSelectedOrder(null)}>
            <DialogContent className="max-w-2xl print-bg-white print-text-black" id="invoice-dialog">
                <DialogHeader>
                    <DialogTitle className="sr-only">تفاصيل الفاتورة</DialogTitle>
                </DialogHeader>
                <div id="invoice-print-area">
                    <style type="text/css" media="print">
                      {`
                        body { 
                            background-color: white !important; 
                            color: black !important; 
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }
                        .print-bg-white { background-color: white !important; }
                        .print-text-black, .print-text-black * { color: black !important; }
                        .no-print { display: none !important; }
                        @page {
                            size: A4;
                            margin: 1cm;
                        }
                      `}
                    </style>
                    <div className="print-invoice print-bg-white print-text-black">
                        <div className="print-header flex justify-between items-center border-b-2 border-primary pb-4 mb-8">
                           <div className="logo flex items-center gap-2 text-primary">
                               <Icons.logo className="size-8" />
                               <span className="font-headline text-2xl font-bold">BarberTrack</span>
                           </div>
                           <h1 className="text-4xl font-bold">فاتورة</h1>
                        </div>
                        <div className="print-invoice-details grid grid-cols-2 gap-8 mb-8">
                            <div>
                                <div className="font-bold text-lg mb-1">فاتورة إلى:</div>
                                <div className="text-gray-600">
                                    {selectedOrder.customer}<br />
                                    123 الشارع الرئيسي<br />
                                    دبي, الإمارات العربية المتحدة
                                </div>
                            </div>
                             <div>
                                <div className="font-bold text-lg mb-1">تفاصيل الفاتورة:</div>
                                <div className="text-gray-600">
                                    <span className="font-semibold">رقم الفاتورة:</span> {selectedOrder.orderId}<br />
                                    <span className="font-semibold">تاريخ الفاتورة:</span> {selectedOrder.date}<br />
                                </div>
                            </div>
                        </div>
                        
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>المنتج</TableHead>
                                    <TableHead>الكمية</TableHead>
                                    <TableHead className="text-left">سعر الوحدة</TableHead>
                                    <TableHead className="text-left">المجموع</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {selectedOrder.items.map((item, index) => (
                                <TableRow key={index}>
                                    <TableCell>{item.name}</TableCell>
                                    <TableCell>{item.quantity}</TableCell>
                                    <TableCell className="text-left">ر.س {item.price.toFixed(2)}</TableCell>
                                    <TableCell className="text-left">ر.س {(item.quantity * item.price).toFixed(2)}</TableCell>
                                </TableRow>
                                ))}
                            </TableBody>
                        </Table>

                        <div className="flex justify-end mt-8">
                            <div className="w-full max-w-sm space-y-2">
                                 <div className="flex justify-between">
                                    <span>المجموع الفرعي:</span>
                                    <span>ر.س {selectedOrder.subtotal.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>ضريبة القيمة المضافة (5%):</span>
                                    <span>ر.س {selectedOrder.vat.toFixed(2)}</span>
                                </div>
                                <Separator className="my-2" />
                                <div className="flex justify-between font-bold text-lg">
                                    <span>المجموع الإجمالي:</span>
                                    <span>ر.س {selectedOrder.total.toFixed(2)}</span>
                                </div>
                            </div>
                        </div>

                        <div className="print-footer text-center mt-16 pt-4 border-t text-xs text-gray-500">
                            <p>شكرًا لتعاملكم معنا!</p>
                            <p>BarberTrack | contact@barbertrack.com | +966 12 345 6789</p>
                        </div>
                    </div>
                </div>
                 <DialogFooter className="no-print pt-4">
                    <Button variant="outline" onClick={handleInvoicePrint}>
                        <Printer className="ml-2 h-4 w-4" />
                        طباعة
                    </Button>
                    <Button onClick={() => setSelectedOrder(null)}>إغلاق</Button>
                 </DialogFooter>
            </DialogContent>
        </Dialog>
      )}
    </div>
  );
}
