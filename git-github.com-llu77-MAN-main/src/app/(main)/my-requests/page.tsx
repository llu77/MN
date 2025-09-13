'use client';
import { useState, useMemo } from 'react';
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
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CheckCircle, XCircle, ShieldCheck, UserCheck, ShieldAlert, History, PlusCircle, CalendarIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { format } from 'date-fns';

const requestSchema = z.object({
  requestType: z.string().min(1, "نوع الطلب مطلوب."),
  amount: z.coerce.number().optional(),
  leaveReason: z.string().optional(),
  resignationReason: z.string().optional(),
  maintenanceDetails: z.string().optional(),
  invoiceNumber: z.string().optional(),
  invoiceDate: z.date().optional(),
  details: z.string().optional(),
}).refine(data => {
    if (data.requestType === 'طلب إجازة') return !!data.leaveReason && data.leaveReason.length > 0;
    if (data.requestType === 'طلب استقالة') return !!data.resignationReason && data.resignationReason.length > 0;
    if (data.requestType === 'طلب صيانة') return !!data.maintenanceDetails && data.maintenanceDetails.length > 0;
    if (data.requestType === 'طلب مراجعة فاتورة') return !!data.invoiceNumber && data.invoiceNumber.length > 0 && !!data.invoiceDate;
    if (['طلب سلفة', 'طلب صرف متأخرات'].includes(data.requestType)) return data.amount !== undefined && data.amount > 0;
    return true;
}, {
    message: "الرجاء تعبئة الحقول الإضافية المطلوبة لهذا النوع من الطلبات.",
    path: ['details'],
});

type RequestFormValues = z.infer<typeof requestSchema>;

const getStatusVariant = (status: string) => {
  switch (status) {
    case 'موافق عليه':
      return 'bg-green-500/20 text-green-400 border-green-500/30';
    case 'قيد انتظار موافقة المشرف':
      return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
    case 'قيد انتظار موافقة الأدمن':
      return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    case 'مرفوض':
      return 'bg-red-500/20 text-red-400 border-red-500/30';
    default:
      return 'secondary';
  }
};

const statusIcons = {
  'موافق عليه': <CheckCircle className="h-4 w-4" />,
  'قيد انتظار موافقة المشرف': <UserCheck className="h-4 w-4" />,
  'قيد انتظار موافقة الأدمن': <ShieldCheck className="h-4 w-4" />,
  'مرفوض': <XCircle className="h-4 w-4" />,
  'سجل الطلبات': <History className="h-4 w-4" />,
};


function AccessDenied() {
    return (
        <div className="flex flex-col items-center justify-center h-[50vh] gap-4 text-center">
            <ShieldAlert className="w-16 h-16 text-destructive" />
            <h1 className="text-3xl font-bold">وصول مرفوض</h1>
            <p className="text-muted-foreground">هذه الصفحة مخصصة للموظفين والمشرفين فقط.</p>
             <Button asChild>
                <a href="/">العودة إلى لوحة التحكم</a>
            </Button>
        </div>
    )
}

function NewRequestForm({ setOpen, onCreateRequest }) {
  const { user } = useAuth();
  const { employees, branches, requestTypes } = useData();
  const form = useForm<RequestFormValues>({
    resolver: zodResolver(requestSchema),
    defaultValues: { requestType: '' }
  });

  const selectedRequestType = form.watch('requestType');

  const getResignationLetter = () => {
    const employee = employees.find(e => e.id === user.id);
    if (!employee) return "";
    const branch = branches.find(b => b.id === employee.branchId);
    return `السلام عليكم ورحمة الله وبركاته،\n\nانا الموظف ${employee.name} اتقدم بطلب استقاله وعدم الرغبه في اكمال المده المتبقيه فالعقد لظروف خاصه تخصني، شاكر لكم تعاونكم.\n\nالفرع: ${branch?.name}\nالمشرف: ${branch?.supervisor}\nاسم الموظف: ${employee.name}\nالتوقيع:`;
  };

  function onSubmit(data: RequestFormValues) {
    onCreateRequest(data);
    form.reset();
    setOpen(false);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="grid gap-4 py-4 max-h-[70vh] overflow-y-auto pr-4">
        <FormField
          control={form.control}
          name="requestType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>نوع الطلب</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger><SelectValue placeholder="اختر نوعًا" /></SelectTrigger>
                </FormControl>
                <SelectContent>
                  {requestTypes.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {(selectedRequestType === 'طلب سلفة' || selectedRequestType === 'طلب صرف متأخرات') && (
          <FormField
            control={form.control}
            name="amount"
            render={({ field }) => (
              <FormItem>
                <FormLabel>المبلغ (ر.س)</FormLabel>
                <FormControl><Input type="number" placeholder="0.00" {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}
        
        {selectedRequestType === 'طلب إجازة' && (
          <FormField
            control={form.control}
            name="leaveReason"
            render={({ field }) => (
              <FormItem>
                <FormLabel>سبب الإجازة</FormLabel>
                <FormControl><Textarea placeholder="الرجاء كتابة سبب طلب الإجازة..." {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}
        
        {selectedRequestType === 'طلب صيانة' && (
          <FormField
            control={form.control}
            name="maintenanceDetails"
            render={({ field }) => (
              <FormItem>
                <FormLabel>تفاصيل الصيانة المطلوبة</FormLabel>
                <FormControl><Textarea placeholder="مثال: مكيف الغرفة لا يعمل..." {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}
        
        {selectedRequestType === 'طلب مراجعة فاتورة' && (
            <div className="grid grid-cols-2 gap-4">
                <FormField
                    control={form.control}
                    name="invoiceNumber"
                    render={({ field }) => (
                    <FormItem>
                        <FormLabel>رقم الفاتورة</FormLabel>
                        <FormControl><Input placeholder="INV-2023-123" {...field} /></FormControl>
                        <FormMessage />
                    </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="invoiceDate"
                    render={({ field }) => (
                    <FormItem className="flex flex-col">
                        <FormLabel>تاريخ الفاتورة</FormLabel>
                        <Popover>
                        <PopoverTrigger asChild>
                            <FormControl>
                            <Button variant={"outline"} className={cn("pl-3 text-right font-normal",!field.value && "text-muted-foreground")}>
                                {field.value ? format(field.value, "PPP") : <span>اختر تاريخًا</span>}
                                <CalendarIcon className="mr-auto h-4 w-4 opacity-50" />
                            </Button>
                            </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                            <Calendar mode="single" selected={field.value} onSelect={field.onChange} initialFocus/>
                        </PopoverContent>
                        </Popover>
                        <FormMessage />
                    </FormItem>
                    )}
                />
            </div>
        )}

        {selectedRequestType === 'طلب استقالة' && (
           <FormField
            control={form.control}
            name="resignationReason"
            render={({ field }) => (
              <FormItem>
                <FormLabel>خطاب الاستقالة</FormLabel>
                <FormControl>
                  <Textarea {...field} rows={8} defaultValue={getResignationLetter()} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {['طلب إجازة', 'طلب صيانة'].includes(selectedRequestType) && (
            <FormField
                control={form.control}
                name="details"
                render={({ field }) => (
                <FormItem>
                    <FormLabel>تفاصيل إضافية</FormLabel>
                    <FormControl>
                    <Textarea {...field} placeholder="أضف أي ملاحظات أو تفاصيل أخرى هنا..." rows={3} />
                    </FormControl>
                    <FormMessage />
                </FormItem>
                )}
            />
        )}
        
        {form.formState.errors.details && <FormMessage>{form.formState.errors.details.message}</FormMessage>}
        
        <DialogFooter className="pt-4 pr-0">
          <Button type="submit">إرسال الطلب</Button>
        </DialogFooter>
      </form>
    </Form>
  );
}

export default function MyRequestsPage() {
  const { user } = useAuth();
  const { employeeRequests, createRequest, employees } = useData();
  const [open, setOpen] = useState(false);
  
  const myRequests = useMemo(() => {
    const employeeData = employees.find(e => e.id === user.id);
    if (!employeeData) return [];
    return employeeRequests.filter(req => req.employee === employeeData.name);
  }, [user.id, employeeRequests, employees]);

  const handleCreateRequest = (data: RequestFormValues) => {
    const employee = employees.find(e => e.id === user.id);
    if (!employee) return;
    createRequest(data, employee);
  };

  if (user.role !== 'employee' && user.role !== 'supervisor') {
      return <AccessDenied />
  }

  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight font-headline">طلباتي</h1>
          <p className="text-muted-foreground">إنشاء ومتابعة حالة جميع الطلبات التي قمت بتقديمها.</p>
        </div>
         <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>
              <PlusCircle className="ml-2 h-4 w-4" />
              طلب جديد
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>إنشاء طلب جديد</DialogTitle>
              <DialogDescription>املأ التفاصيل لتقديم طلب جديد. سيتم إرساله للمراجعة.</DialogDescription>
            </DialogHeader>
            <NewRequestForm setOpen={setOpen} onCreateRequest={handleCreateRequest} />
          </DialogContent>
        </Dialog>
      </header>

      <Card>
        <CardHeader>
            <CardTitle>سجل الطلبات</CardTitle>
            <CardDescription>قائمة بجميع طلباتك وحالاتها الحالية.</CardDescription>
        </CardHeader>
        <CardContent>
            <Table>
                <TableHeader>
                <TableRow>
                    <TableHead>النوع</TableHead>
                    <TableHead>التاريخ</TableHead>
                    <TableHead className="text-left">الحالة</TableHead>
                </TableRow>
                </TableHeader>
                <TableBody>
                {myRequests.length > 0 ? myRequests.map(req => (
                    <TableRow key={req.id}>
                        <TableCell className="font-medium">{req.type}</TableCell>
                        <TableCell>{req.date}</TableCell>
                        <TableCell className="text-left">
                            <Badge variant="outline" className={cn("gap-1.5 whitespace-nowrap", getStatusVariant(req.status))}>
                            {statusIcons[req.status]}
                            {req.status}
                            </Badge>
                        </TableCell>
                    </TableRow>
                )) : (
                     <TableRow>
                        <TableCell colSpan={3} className="text-center text-muted-foreground p-8">
                             ليس لديك أي طلبات مقدمة حاليًا.
                        </TableCell>
                    </TableRow>
                )}
                </TableBody>
            </Table>
        </CardContent>
      </Card>
    </div>
  );
}
