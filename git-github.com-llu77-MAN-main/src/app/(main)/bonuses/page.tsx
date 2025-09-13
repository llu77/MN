'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
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
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { FileDown, Percent } from 'lucide-react';
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useAuth } from '@/hooks/use-auth';
import { useMemo } from 'react';
import { useData } from '@/hooks/use-data';

const chartConfig = {
  bonus: {
    label: 'بونص',
    color: 'hsl(var(--primary))',
  },
  revenue: {
    label: 'الإيرادات',
    color: 'hsl(var(--accent))',
  },
};

export default function BonusesPage() {
    const { user } = useAuth();
    const { employees, branches, bonusData } = useData();
    
    // In a real app, this data would be fetched based on the user's branch
    // For now, we filter the mock data
    const branchEmployees = useMemo(() => {
        if (user.role === 'admin') return employees;
        if (user.role === 'supervisor') {
            const supervisorBranchId = employees.find(e => e.id === user.id)?.branchId;
            return employees.filter(e => e.branchId === supervisorBranchId);
        }
        return [];
    }, [user, employees]);

    const branchEmployeeNames = useMemo(() => branchEmployees.map(e => e.name), [branchEmployees]);

    const filteredBonusData = useMemo(() => bonusData.filter(d => branchEmployeeNames.includes(d.name)), [branchEmployeeNames, bonusData]);
    
    const currentBranch = useMemo(() => branches.find(b => b.id === user.branchId), [user.branchId, branches]);


  const handlePrint = () => {
    const printContent = document.getElementById('bonuses-print-area');
    if (printContent) {
      const printWindow = window.open('', '_blank');
      printWindow.document.write('<html><head><title>تقرير البونص</title>');
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
          .print-header { text-align: center; margin-bottom: 2rem; border-bottom: 2px solid #ccc; padding-bottom: 1rem; }
          .print-header h1 { font-size: 2rem; font-weight: bold; color: #673ab7; }
          .print-header p { font-size: 1rem; color: #666; }
          table { width: 100%; border-collapse: collapse; font-size: 1rem; }
          th, td { border: 1px solid #ddd; padding: 0.75rem; text-align: right; }
          th { background-color: #f2f2f2; }
          .print-footer { text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ccc; font-size: 0.8rem; color: #666; position: fixed; bottom: 0; width: 100%; }
          .no-print { display: none !important; }
          .print-only { display: block !important; }
          .print-bg-white { background-color: white !important; }
          .print-text-black * { color: black !important; }
          
          /* Ensure cards and charts are visible */
          .printable-card {
            border: 1px solid #ddd;
            border-radius: 0.5rem;
            box-shadow: none;
            background-color: white !important;
            page-break-inside: avoid;
          }
           .printable-card-header, .printable-card-content {
             background-color: white !important;
           }
        </style>
      `);
      printWindow.document.write('</head><body dir="rtl">');
      printWindow.document.write('<div class="print-container">');
       
       // Clone the content to avoid removing it from the original page
      const clonedContent = printContent.cloneNode(true) as HTMLElement;
      
      // Add a printable header
      const header = document.createElement('div');
      header.className = 'print-header';
      header.innerHTML = `<h1>تقرير البونص الشهري</h1><p>فرع: ${currentBranch?.name} - المشرف: ${user.name}</p>`;
      
      // Add a printable footer
      const footer = document.createElement('div');
      footer.className = 'print-footer';
      footer.innerHTML = '<p>BarberTrack | contact@barbertrack.com | +966 12 345 6789</p>';

      const finalPrintDiv = printWindow.document.createElement('div');
      finalPrintDiv.appendChild(header);
      finalPrintDiv.appendChild(clonedContent);
      finalPrintDiv.appendChild(footer);

      printWindow.document.body.appendChild(finalPrintDiv);
      printWindow.document.close();
      printWindow.focus();

      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 500);
    }
  };

  const aggregatedBonusData = filteredBonusData.reduce((acc, current) => {
    const existing = acc.find(item => item.name === current.name);
    if (existing) {
        existing.revenue += current.revenue;
        existing.bonus += current.bonus;
    } else {
        acc.push({ name: current.name, revenue: current.revenue, bonus: current.bonus });
    }
    return acc;
  }, []);

  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start no-print">
        <div>
            <h1 className="text-3xl font-bold tracking-tight font-headline">نظام البونص</h1>
            <p className="text-muted-foreground">مراجعة وإدارة بونص الموظفين لفرع: {currentBranch?.name || 'كل الفروع'}</p>
        </div>
        <Button onClick={handlePrint}>
            <FileDown className="ml-2 h-4 w-4" />
            تصدير PDF
        </Button>
      </header>

      <div id="bonuses-print-area">
        <div className="grid gap-8 md:grid-cols-5">
            <Card className="md:col-span-3 printable-card print-bg-white print-text-black">
            <CardHeader className="printable-card-header">
                <CardTitle>أداء الموظفين والبورصات (إجمالي الشهر)</CardTitle>
                <CardDescription>مقارنة بين إجمالي إيرادات الموظفين والبونص المستحق للشهر الحالي.</CardDescription>
            </CardHeader>
            <CardContent className="pl-2 printable-card-content">
                <ChartContainer config={chartConfig} className="h-[350px] w-full">
                    <ResponsiveContainer>
                        <BarChart data={aggregatedBonusData}>
                            <CartesianGrid vertical={false} />
                            <XAxis dataKey="name" tickLine={false} tickMargin={10} axisLine={false} />
                            <YAxis />
                            <ChartTooltip content={<ChartTooltipContent />} />
                            <Bar dataKey="revenue" fill="var(--color-revenue)" radius={4} name="الإيرادات" />
                            <Bar dataKey="bonus" fill="var(--color-bonus)" radius={4} name="البونص" />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartContainer>
            </CardContent>
            </Card>
            
            <Card className="md:col-span-2 printable-card print-bg-white print-text-black">
            <CardHeader className="printable-card-header">
                <CardTitle>تفاصيل البونص الأسبوعية</CardTitle>
                <CardDescription>تفاصيل البونص الأسبوعية لكل موظف.</CardDescription>
            </CardHeader>
            <CardContent className="printable-card-content">
                <Table>
                <TableHeader>
                    <TableRow>
                    <TableHead>الموظف</TableHead>
                    <TableHead>الأسبوع</TableHead>
                    <TableHead>الإيرادات</TableHead>
                    <TableHead className="text-left">البونص</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {filteredBonusData.map(emp => (
                        <TableRow key={`${emp.name}-${emp.week}`}>
                            <TableCell className="font-medium flex items-center gap-3">
                                <Avatar className="h-8 w-8 no-print">
                                    <AvatarFallback>{emp.name.substring(0,2)}</AvatarFallback>
                                </Avatar>
                                {emp.name}
                            </TableCell>
                            <TableCell>{emp.week}</TableCell>
                             <TableCell>ر.س {emp.revenue.toFixed(2)}</TableCell>
                            <TableCell className="text-left font-bold text-primary">ر.س {emp.bonus.toFixed(2)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                </Table>
            </CardContent>
            <CardFooter>
                <p className="text-xs text-muted-foreground">يتم احتساب البونص بناءً على الإيرادات الأسبوعية.</p>
            </CardFooter>
            </Card>
        </div>
      </div>

    </div>
  );
}
