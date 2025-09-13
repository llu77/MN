'use client';

import { useState, useEffect, useMemo } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
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
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { CalendarIcon, PlusCircle, Trash2, Printer } from 'lucide-react';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';
import { Icons } from '@/components/icons';

const revenueSchema = z.object({
  branch: z.string().min(1, 'الفرع مطلوب.'),
  date: z.date({
    required_error: "التاريخ مطلوب.",
  }),
  cash: z.coerce.number().min(0, "يجب أن يكون المبلغ النقدي موجبًا."),
  network: z.coerce.number().min(0, "يجب أن يكون مبلغ الشبكة موجبًا."),
  employeeSplits: z.array(z.object({
    employeeId: z.string().min(1, "الرجاء اختيار موظف."),
    amount: z.coerce.number().min(0, "يجب أن يكون المبلغ موجبًا."),
  })).min(1, "يجب إضافة حصة موظف واحد على الأقل."),
}).refine(data => {
    const totalRevenue = data.cash + data.network;
    const totalSplits = data.employeeSplits.reduce((acc, split) => acc + split.amount, 0);
    // Use a small epsilon for float comparison
    return Math.abs(totalRevenue - totalSplits) < 0.01;
}, {
  message: "يجب أن يساوي إجمالي الإيرادات (نقدي + شبكة) مجموع حصص الموظفين.",
  path: ["employeeSplits"], // Assign error to a field for display
});


type RevenueFormValues = z.infer<typeof revenueSchema>;


export default function RevenuePage() {
  const { user } = useAuth();
  const { dailyEntries, addDailyEntry, employees, branches } = useData();
  const supervisorBranchId = useMemo(() => employees.find(e => e.id === user.id)?.branchId, [user.id, employees]);

  const form = useForm<RevenueFormValues>({
    resolver: zodResolver(revenueSchema),
    defaultValues: {
      branch: user.role === 'supervisor' ? supervisorBranchId : '',
      date: new Date(),
      cash: 0,
      network: 0,
      employeeSplits: [{ employeeId: '', amount: 0 }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "employeeSplits",
  });
  
  const watchedValues = form.watch();
  const selectedBranchId = watchedValues.branch;
  
  const filteredEmployees = useMemo(() => {
    if (!selectedBranchId) return [];
    return employees.filter(e => e.branchId === selectedBranchId && (e.role === 'employee' || e.role === 'supervisor'));
  }, [employees, selectedBranchId]);
  
  const userBranch = useMemo(() => branches.find(b => b.id === user.branchId), [branches, user.branchId]);

  const totalEmployeeSplit = watchedValues.employeeSplits.reduce((acc, split) => acc + (Number(split.amount) || 0), 0);
  const totalRevenue = (Number(watchedValues.cash) || 0) + (Number(watchedValues.network) || 0);
  const difference = totalRevenue - totalEmployeeSplit;
  const isBalanced = Math.abs(difference) < 0.01;


  function onSubmit(data: RevenueFormValues) {
    addDailyEntry(data);
    form.reset({
        branch: user.role === 'supervisor' ? supervisorBranchId : '',
        date: new Date(),
        cash: 0,
        network: 0,
        employeeSplits: [{ employeeId: '', amount: 0 }],
    });
  }
  
  const handlePrint = () => {
    const printContent = document.getElementById('revenue-print-area');
    if (printContent) {
      const printWindow = window.open('', '_blank');
      printWindow.document.write('<html><head><title>تقرير الإيرادات</title>');
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
            <h1>تقرير إدخالات الإيرادات</h1>
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
                <CardTitle>إدخالات الإيرادات الأخيرة</CardTitle>
                <CardDescription>سجل بإيرادات الأيام الأخيرة.</CardDescription>
            </div>
            <Button variant="outline" onClick={handlePrint}>
                <Printer className="ml-2 h-4 w-4" />
                طباعة
            </Button>
          </CardHeader>
          <CardContent id="revenue-print-area">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>التاريخ</TableHead>
                  <TableHead>نقدي</TableHead>
                  <TableHead>شبكة</TableHead>
                  <TableHead className="text-left">المجموع</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {dailyEntries.map((entry, i) => (
                   <TableRow key={i}>
                    <TableCell>{format(entry.date, 'yyyy-MM-dd')}</TableCell>
                    <TableCell>ر.س {entry.cash.toFixed(2)}</TableCell>
                    <TableCell>ر.س {entry.network.toFixed(2)}</TableCell>
                    <TableCell className="text-left font-medium">ر.س {(entry.cash + entry.network).toFixed(2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
      <div className="lg:col-span-2 no-print">
        <Card>
          <CardHeader>
            <CardTitle>تسجيل الإيرادات اليومية</CardTitle>
            <CardDescription>أدخل تفاصيل إيرادات اليوم.</CardDescription>
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
                            onValueChange={(value) => {
                                field.onChange(value);
                                form.reset({ 
                                    ...form.getValues(), 
                                    branch: value,
                                    employeeSplits: [{ employeeId: '', amount: 0 }] 
                                });
                            }} 
                            value={field.value}
                            disabled={user.role === 'supervisor'}
                        >
                          <FormControl>
                            <SelectTrigger><SelectValue placeholder="اختر فرعًا" /></SelectTrigger>
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
                  name="date"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>التاريخ</FormLabel>
                      <Popover>
                        <PopoverTrigger asChild>
                          <FormControl>
                            <Button
                              variant={"outline"}
                              className={cn(
                                "pl-3 text-right font-normal",
                                !field.value && "text-muted-foreground"
                              )}
                            >
                              {field.value ? (
                                format(field.value, "PPP")
                              ) : (
                                <span>اختر تاريخًا</span>
                              )}
                              <CalendarIcon className="mr-auto h-4 w-4 opacity-50" />
                            </Button>
                          </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            mode="single"
                            selected={field.value}
                            onSelect={field.onChange}
                            disabled={(date) =>
                              date > new Date() || date < new Date("1900-01-01")
                            }
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="grid grid-cols-2 gap-4">
                   <FormField
                    control={form.control}
                    name="cash"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>الإيرادات النقدية (ر.س)</FormLabel>
                        <FormControl>
                          <Input type="number" placeholder="0.00" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="network"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>إيرادات الشبكة (ر.س)</FormLabel>
                        <FormControl>
                          <Input type="number" placeholder="0.00" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <FormLabel>حصص الموظفين</FormLabel>
                    <FormMessage>{form.formState.errors.employeeSplits?.message}</FormMessage>
                  </div>
                   <div className="space-y-4 mt-2">
                     {fields.map((field, index) => (
                       <div key={field.id} className="flex items-end gap-2">
                          <FormField
                            control={form.control}
                            name={`employeeSplits.${index}.employeeId`}
                            render={({ field }) => (
                               <FormItem className="flex-1">
                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                    <FormControl>
                                    <SelectTrigger disabled={!selectedBranchId}>
                                        <SelectValue placeholder="اختر موظف" />
                                    </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                    {filteredEmployees.map(emp => (
                                        <SelectItem key={emp.id} value={emp.id}>{emp.name}</SelectItem>
                                    ))}
                                    </SelectContent>
                                </Select>
                               </FormItem>
                            )}
                          />
                          <FormField
                            control={form.control}
                            name={`employeeSplits.${index}.amount`}
                            render={({ field }) => (
                               <FormItem>
                                 <FormControl>
                                    <Input type="number" placeholder="0.00" {...field} className="w-28" />
                                 </FormControl>
                               </FormItem>
                            )}
                          />
                         <Button type="button" variant="ghost" size="icon" onClick={() => remove(index)} disabled={fields.length <= 1}>
                           <Trash2 className="h-4 w-4 text-destructive" />
                         </Button>
                       </div>
                     ))}
                     <Button
                       type="button"
                       variant="outline"
                       size="sm"
                       onClick={() => append({ employeeId: '', amount: 0 })}
                       disabled={!selectedBranchId}
                     >
                       <PlusCircle className="ml-2 h-4 w-4" /> أضف موظفًا
                     </Button>
                   </div>
                </div>

                <Card className={cn("p-4 transition-colors", isBalanced ? 'bg-green-950/50 border-green-500/30' : 'bg-red-950/50 border-red-500/30')}>
                    <div className="flex justify-between text-sm font-medium">
                        <span>إجمالي الإيرادات:</span>
                        <span>{totalRevenue.toFixed(2)} ر.س</span>
                    </div>
                     <div className="flex justify-between text-sm font-medium">
                        <span>إجمالي الحصص:</span>
                        <span>{totalEmployeeSplit.toFixed(2)} ر.س</span>
                    </div>
                     <div className="flex justify-between text-sm font-bold mt-2 pt-2 border-t border-white/10">
                        <span>الفرق:</span>
                        <span className={cn(isBalanced ? 'text-green-400' : 'text-red-400')}>{difference.toFixed(2)} ر.س</span>
                    </div>
                </Card>

                <Button type="submit" className="w-full" disabled={!isBalanced}>إرسال الإيرادات</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

    