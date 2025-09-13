'use client';
import { useState, useEffect, useMemo } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
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
import { FileDown } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Input } from '@/components/ui/input';
import { useData } from '@/hooks/use-data';
import { useAuth } from '@/hooks/use-auth';

type PayrollEntry = {
    id: string;
    name: string;
    baseSalary: number;
    deductions: number;
    incentives: number;
    advance: number;
}

export default function PayrollPage() {
    const { user } = useAuth();
    const { employees } = useData();
    const [selectedMonth, setSelectedMonth] = useState('2023-10');
    const [payrolls, setPayrolls] = useState<PayrollEntry[]>([]);

     const branchEmployees = useMemo(() => {
        if (user.role === 'admin') {
            return employees.filter(e => e.role === 'employee' || e.role === 'supervisor');
        }
        if (user.role === 'supervisor') {
            const supervisorBranchId = employees.find(e => e.id === user.id)?.branchId;
            return employees.filter(e => e.branchId === supervisorBranchId && (e.role === 'employee' || e.role === 'supervisor'));
        }
        return [];
    }, [user, employees]);


    useEffect(() => {
        // Initialize payrolls with employees, but with empty values
        const initialPayrolls = branchEmployees
            .map(e => ({
                id: e.id,
                name: e.name,
                baseSalary: 0,
                deductions: 0,
                incentives: 0,
                advance: 0,
            }));
        setPayrolls(initialPayrolls);
    }, [selectedMonth, branchEmployees]);

    const handleInputChange = (employeeId: string, field: keyof Omit<PayrollEntry, 'id' | 'name'>, value: string) => {
        const numericValue = parseFloat(value) || 0;
        setPayrolls(currentPayrolls => 
            currentPayrolls.map(p => 
                p.id === employeeId ? { ...p, [field]: numericValue } : p
            )
        );
    };

    const calculateTotalPay = (payroll: PayrollEntry) => {
        return payroll.baseSalary + payroll.incentives - payroll.deductions - payroll.advance;
    }
    
    const totalNetPay = payrolls.reduce((acc, p) => acc + calculateTotalPay(p), 0);

    const handlePrint = () => {
        const printWindow = window.open('', '_blank');
        if (!printWindow) return;

        const selectedMonthText = document.querySelector('#month span')?.textContent || selectedMonth;

        let tableContent = '';
        payrolls.forEach(p => {
            tableContent += `
                <tr>
                    <td>${p.name}</td>
                    <td>ر.س ${p.baseSalary.toFixed(2)}</td>
                    <td>ر.س ${p.incentives.toFixed(2)}</td>
                    <td>ر.س ${p.deductions.toFixed(2)}</td>
                    <td>ر.س ${p.advance.toFixed(2)}</td>
                    <td class="font-bold">ر.س ${calculateTotalPay(p).toFixed(2)}</td>
                </tr>
            `;
        });

        printWindow.document.write('<html><head><title>كشف رواتب</title>');
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
                table { width: 100%; border-collapse: collapse; font-size: 1rem; margin-top: 2rem; }
                th, td { border: 1px solid #ddd; padding: 0.75rem; text-align: right; }
                th { background-color: #f2f2f2; }
                .totals { margin-top: 2rem; width: 300px; float: left; text-align: right; }
                .totals div { display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; padding: 0.5rem; border-top: 1px solid #ddd;}
                .print-footer { text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ccc; font-size: 0.8rem; color: #666; position: fixed; bottom: 0; width: 100%; }
                .no-print { display: none !important; }
                .font-bold { font-weight: bold; }
            </style>
        `);
        printWindow.document.write('</head><body dir="rtl">');
        printWindow.document.write(`
            <div class="print-container">
                <div class="print-header">
                    <h1>كشف الرواتب</h1>
                    <p>الشهر: ${selectedMonthText}</p>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>الموظف</th>
                            <th>الراتب الأساسي</th>
                            <th>الحوافز</th>
                            <th>الخصومات</th>
                            <th>السلفة</th>
                            <th>صافي الراتب</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableContent}
                    </tbody>
                </table>
                <div style="clear: both;"></div>
                <div class="totals">
                    <div>
                        <span>الإجمالي</span>
                        <span>ر.س ${totalNetPay.toFixed(2)}</span>
                    </div>
                </div>
                <div class="print-footer">
                    <p>BarberTrack | contact@barbertrack.com | +966 12 345 6789</p>
                </div>
            </div>
        `);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => {
            printWindow.print();
            printWindow.close();
        }, 500);
    };

  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight font-headline">إدارة الرواتب</h1>
          <p className="text-muted-foreground">حساب ومراجعة رواتب الموظفين الشهرية.</p>
        </div>
         <Button onClick={handlePrint}>
            <FileDown className="ml-2 h-4 w-4" />
            تصدير كشف الرواتب
        </Button>
      </header>

      <Card>
        <CardHeader>
            <div className="flex justify-between items-center">
                <div>
                    <CardTitle>كشف رواتب الموظفين</CardTitle>
                    <CardDescription>تفاصيل رواتب الموظفين للشهر المحدد.</CardDescription>
                </div>
                <div className="flex items-center gap-4">
                    <div className="grid w-full max-w-sm items-center gap-1.5">
                        <Label htmlFor="month">الشهر</Label>
                        <Select onValueChange={setSelectedMonth} defaultValue={selectedMonth}>
                            <SelectTrigger id="month" className="w-[180px]">
                                <SelectValue placeholder="اختر شهرًا" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="2023-10">أكتوبر 2023</SelectItem>
                                <SelectItem value="2023-09">سبتمبر 2023</SelectItem>
                                <SelectItem value="2023-08">أغسطس 2023</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
            </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
                <TableHeader>
                <TableRow>
                    <TableHead className="min-w-[150px]">الموظف</TableHead>
                    <TableHead className="min-w-[150px]">الراتب الأساسي</TableHead>
                    <TableHead className="min-w-[150px]">الحوافز</TableHead>
                    <TableHead className="min-w-[150px]">الخصومات</TableHead>
                    <TableHead className="min-w-[150px]">السلفة</TableHead>
                    <TableHead className="text-left font-bold text-primary min-w-[150px]">صافي الراتب</TableHead>
                </TableRow>
                </TableHeader>
                <TableBody>
                {payrolls.map((payroll) => (
                    <TableRow key={payroll.id}>
                    <TableCell className="font-medium">{payroll.name}</TableCell>
                    <TableCell>
                        <Input 
                            type="number" 
                            placeholder="0.00"
                            className="w-28"
                            value={payroll.baseSalary || ''}
                            onChange={(e) => handleInputChange(payroll.id, 'baseSalary', e.target.value)}
                        />
                    </TableCell>
                    <TableCell>
                         <Input 
                            type="number" 
                            placeholder="0.00"
                            className="w-28"
                            value={payroll.incentives || ''}
                            onChange={(e) => handleInputChange(payroll.id, 'incentives', e.target.value)}
                        />
                    </TableCell>
                    <TableCell>
                         <Input 
                            type="number" 
                            placeholder="0.00"
                            className="w-28 text-destructive"
                            value={payroll.deductions || ''}
                            onChange={(e) => handleInputChange(payroll.id, 'deductions', e.target.value)}
                        />
                    </TableCell>
                    <TableCell>
                         <Input 
                            type="number" 
                            placeholder="0.00"
                            className="w-28 text-destructive"
                            value={payroll.advance || ''}
                            onChange={(e) => handleInputChange(payroll.id, 'advance', e.target.value)}
                        />
                    </TableCell>
                    <TableCell className="text-left font-bold text-primary">ر.س {calculateTotalPay(payroll).toFixed(2)}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
          </div>
        </CardContent>
         <CardFooter className="flex-col items-end gap-2">
            <Separator />
            <div className="flex justify-between w-full max-w-xs text-lg font-bold p-2">
                <span>الإجمالي</span>
                <span>ر.س {totalNetPay.toFixed(2)}</span>
            </div>
         </CardFooter>
      </Card>
    </div>
  );
}
