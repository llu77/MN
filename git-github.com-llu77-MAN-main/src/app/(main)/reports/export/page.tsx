'use client';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { format } from 'date-fns';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { DateRange } from 'react-day-picker';
import { cn } from '@/lib/utils';
import { CalendarIcon, LoaderCircle, Printer, Wand2 } from 'lucide-react';
import { generateReport } from './actions';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const reportSchema = z.object({
  reportType: z.enum(['revenues', 'expenses'], {
    required_error: "نوع التقرير مطلوب.",
  }),
  dateRange: z.object({
    from: z.date({ required_error: "تاريخ البدء مطلوب." }),
    to: z.date({ required_error: "تاريخ الانتهاء مطلوب." }),
  }),
});

type ReportFormValues = z.infer<typeof reportSchema>;

interface ReportResult {
  report: string;
  arabicSummary: string;
}

export default function ExportReportPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ReportResult | null>(null);

  const form = useForm<ReportFormValues>({
    resolver: zodResolver(reportSchema),
    defaultValues: {
      reportType: 'revenues',
      dateRange: {
        from: new Date(new Date().setDate(1)),
        to: new Date(),
      },
    },
  });

  async function onSubmit(data: ReportFormValues) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await generateReport(data);
      if (response.error) {
        setError(response.error);
      } else {
        setResult(response.data);
      }
    } catch (e) {
      setError('حدث خطأ غير متوقع.');
    } finally {
      setLoading(false);
    }
  }

  const handlePrint = () => {
    const printContent = document.getElementById('report-print-area');
    if (printContent) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>طباعة التقرير</title>');
        printWindow.document.write('<link rel="stylesheet" href="/globals.css" type="text/css" media="print"/>');
        printWindow.document.head.insertAdjacentHTML('beforeend', `
            <style>
                body { direction: rtl; font-family: 'Cairo', sans-serif; background-color: white; color: black; }
                .prose { max-width: 100%; color: black; }
                h1, h2, h3, p { color: black !important; }
                @media print {
                    body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                    .no-print { display: none !important; }
                }
            </style>
        `);
        printWindow.document.write('</head><body dir="rtl">');
        printWindow.document.write(printContent.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => {
            printWindow.print();
            printWindow.close();
        }, 500);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold tracking-tight font-headline">إنشاء وتصدير تقرير</h1>
        <p className="text-muted-foreground">استخدم الذكاء الاصطناعي لإنشاء تقرير قابل للطباعة مع ملخص باللغة العربية.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>خيارات التقرير</CardTitle>
            <CardDescription>اختر النوع والنطاق الزمني لتقريرك.</CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                  control={form.control}
                  name="reportType"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>نوع التقرير</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="اختر نوع التقرير" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="revenues">الإيرادات</SelectItem>
                          <SelectItem value="expenses">المصروفات</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="dateRange"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>النطاق الزمني</FormLabel>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant={'outline'}
                            className={cn(
                              'justify-start text-right font-normal',
                              !field.value.from && 'text-muted-foreground'
                            )}
                          >
                            <CalendarIcon className="ml-2 h-4 w-4" />
                            {field.value.from ? (
                              field.value.to ? (
                                <>
                                  {format(field.value.to, 'LLL dd, y')} -{' '}
                                  {format(field.value.from, 'LLL dd, y')}
                                </>
                              ) : (
                                format(field.value.from, 'LLL dd, y')
                              )
                            ) : (
                              <span>اختر تاريخًا</span>
                            )}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            initialFocus
                            mode="range"
                            defaultMonth={field.value.from}
                            selected={{ from: field.value.from, to: field.value.to }}
                            onSelect={(range) => field.onChange(range)}
                            numberOfMonths={2}
                          />
                        </PopoverContent>
                      </Popover>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? (
                    <LoaderCircle className="animate-spin ml-2" />
                  ) : (
                    <Wand2 className="ml-2" />
                  )}
                  إنشاء تقرير
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>

        <div className="lg:col-span-2">
            {loading && (
                <Card>
                    <CardContent className="pt-6 flex flex-col items-center justify-center h-96">
                        <LoaderCircle className="w-12 h-12 animate-spin text-primary" />
                        <p className="mt-4 text-muted-foreground">جاري إنشاء تقريرك باستخدام الذكاء الاصطناعي ...</p>
                    </CardContent>
                </Card>
            )}
            {error && (
                 <Alert variant="destructive">
                    <AlertTitle>خطأ في إنشاء التقرير</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}
            {result && (
                <Card>
                    <CardHeader className="flex-row items-center justify-between">
                        <div>
                            <CardTitle>التقرير المُنشأ</CardTitle>
                            <CardDescription>راجع تقريرك المُنشأ أدناه.</CardDescription>
                        </div>
                        <Button onClick={handlePrint} className="no-print">
                            <Printer className="ml-2" /> طباعة
                        </Button>
                    </CardHeader>
                    <CardContent>
                        <div id="report-print-area" className="prose prose-sm prose-invert max-w-none p-6 bg-background border rounded-lg">
                            <h2 className="text-right font-bold" dir="rtl">ملخص بالذكاء الاصطناعي</h2>
                            <p className="text-right" dir="rtl">{result.arabicSummary}</p>
                            <div dangerouslySetInnerHTML={{ __html: result.report }} />
                        </div>
                    </CardContent>
                </Card>
            )}
            {!loading && !error && !result && (
                 <Card>
                    <CardContent className="pt-6 flex flex-col items-center justify-center h-96">
                        <p className="text-muted-foreground">سيظهر تقريرك المُنشأ هنا.</p>
                    </CardContent>
                </Card>
            )}
        </div>
      </div>
    </div>
  );
}
