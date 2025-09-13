'use client';

import Link from 'next/link';
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
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Line, LineChart, PieChart, Pie, Cell } from 'recharts';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { FinancialReportGenerator } from './financial-report-generator';
import { Button } from '@/components/ui/button';
import { FileDown, TrendingUp, TrendingDown, Wallet, Percent, CalendarDays, User, ArrowUp, ArrowDown } from 'lucide-react';
import { monthlyChartData, expenseCategories, employeePerformance, employees } from '@/lib/data';
import { useMemo } from 'react';

const chartConfig = {
  revenue: {
    label: 'الإيرادات',
    color: 'hsl(var(--chart-1))',
  },
  expenses: {
    label: 'المصروفات',
    color: 'hsl(var(--chart-2))',
  },
  bonus: {
      label: 'بونص',
      color: 'hsl(var(--chart-3))'
  }
};

export default function ReportsPage() {

    // Calculate KPIs
    const { 
        totalRevenue, 
        totalExpenses, 
        netProfit, 
        netProfitMargin,
        avgDailyRevenue,
        revenuePerEmployee,
        highestMonth,
        lowestMonth
    } = useMemo(() => {
        const totalRevenue = monthlyChartData.reduce((acc, item) => acc + item.revenue, 0);
        const totalExpenses = monthlyChartData.reduce((acc, item) => acc + item.expenses, 0);
        const netProfit = totalRevenue - totalExpenses;
        const netProfitMargin = totalRevenue > 0 ? (netProfit / totalRevenue) * 100 : 0;

        const numberOfDaysInYear = 365;
        const avgDailyRevenue = totalRevenue / numberOfDaysInYear;
        
        const activeEmployees = employees.filter(e => e.role === 'employee' || e.role === 'supervisor').length;
        const revenuePerEmployee = activeEmployees > 0 ? totalRevenue / activeEmployees : 0;

        const sortedMonths = [...monthlyChartData].sort((a, b) => b.revenue - a.revenue);
        const highestMonth = sortedMonths[0];
        const lowestMonth = sortedMonths[sortedMonths.length - 1];

        return {
            totalRevenue,
            totalExpenses,
            netProfit,
            netProfitMargin,
            avgDailyRevenue,
            revenuePerEmployee,
            highestMonth,
            lowestMonth,
        };
    }, []);


  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start">
        <div>
            <h1 className="text-3xl font-bold tracking-tight font-headline">التقارير التحليلية</h1>
            <p className="text-muted-foreground">نظرة شاملة على الأداء المالي والتشغيلي لعملك.</p>
        </div>
         <Button asChild>
            <Link href="/reports/export">
                <FileDown className="ml-2 h-4 w-4" />
                إنشاء وتصدير تقرير
            </Link>
        </Button>
      </header>

      {/* KPIs Section */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">إجمالي الإيرادات</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">ر.س {totalRevenue.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">خلال آخر 12 شهرًا</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">إجمالي المصروفات</CardTitle>
                <TrendingDown className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">ر.س {totalExpenses.toLocaleString()}</div>
                 <p className="text-xs text-muted-foreground">خلال آخر 12 شهرًا</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">صافي الربح</CardTitle>
                <Wallet className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">ر.س {netProfit.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">الإيرادات - المصروفات</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">هامش الربح الصافي</CardTitle>
                <Percent className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{netProfitMargin.toFixed(2)}%</div>
                <p className="text-xs text-muted-foreground">مؤشر على الكفاءة</p>
            </CardContent>
        </Card>
      </div>

       <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">متوسط الإيراد اليومي</CardTitle>
                <CalendarDays className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">ر.س {avgDailyRevenue.toFixed(2)}</div>
                <p className="text-xs text-muted-foreground">متوسط الإيراد على مدار العام</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">الإيراد لكل موظف</CardTitle>
                <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">ر.س {revenuePerEmployee.toFixed(2)}</div>
                 <p className="text-xs text-muted-foreground">مؤشر على إنتاجية الموظفين</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">الشهر الأعلى أداءً</CardTitle>
                <ArrowUp className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{highestMonth.month}</div>
                <p className="text-xs text-muted-foreground">بإيرادات بلغت {highestMonth.revenue.toLocaleString()} ر.س</p>
            </CardContent>
        </Card>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">الشهر الأقل أداءً</CardTitle>
                <ArrowDown className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{lowestMonth.month}</div>
                <p className="text-xs text-muted-foreground">بإيرادات بلغت {lowestMonth.revenue.toLocaleString()} ر.س</p>
            </CardContent>
        </Card>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>أداء الإيرادات مقابل المصروفات (شهري)</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <ChartContainer config={chartConfig} className="h-[300px] w-full">
               <ResponsiveContainer>
                <LineChart data={monthlyChartData}>
                  <CartesianGrid vertical={false} strokeDasharray="3 3" />
                  <XAxis dataKey="month" tickLine={false} axisLine={false} tickMargin={8} fontSize={12} />
                  <YAxis tickLine={false} axisLine={false} tickMargin={8} tickFormatter={(value) => `ر.س ${value / 1000}k`} />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Line dataKey="revenue" type="monotone" stroke="var(--color-revenue)" strokeWidth={2} dot={false} name="الإيرادات" />
                  <Line dataKey="expenses" type="monotone" stroke="var(--color-expenses)" strokeWidth={2} dot={false} name="المصروفات" />
                </LineChart>
              </ResponsiveContainer>
            </ChartContainer>
          </CardContent>
        </Card>
        <Card>
            <CardHeader>
                <CardTitle>تحليل المصروفات</CardTitle>
                <CardDescription>توزيع المصروفات حسب الفئة لهذا الشهر.</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <ChartTooltip content={<ChartTooltipContent nameKey="category" />} />
                            <Pie data={expenseCategories} dataKey="value" nameKey="category" cx="50%" cy="50%" innerRadius={60} outerRadius={100} strokeWidth={2}>
                            {expenseCategories.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                            </Pie>
                        </PieChart>
                    </ResponsiveContainer>
                </ChartContainer>
            </CardContent>
        </Card>
      </div>
      
      <div className="grid gap-8 lg:grid-cols-3">
        <Card className="lg:col-span-2">
            <CardHeader>
                <CardTitle>أداء الموظفين</CardTitle>
                <CardDescription>تحليل إيرادات وبونص الموظفين للشهر الحالي.</CardDescription>
            </CardHeader>
            <CardContent>
                 <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>الموظف</TableHead>
                            <TableHead>الإيرادات</TableHead>
                            <TableHead className="text-left">البونص</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {employeePerformance.map((emp) => (
                            <TableRow key={emp.name}>
                                <TableCell className="font-medium flex items-center gap-3">
                                    <Avatar className="h-8 w-8">
                                        <AvatarFallback>{emp.name.substring(0,2)}</AvatarFallback>
                                    </Avatar>
                                    {emp.name}
                                </TableCell>
                                <TableCell>ر.س {emp.revenue.toFixed(2)}</TableCell>
                                <TableCell className="text-left font-bold text-primary">ر.س {emp.bonus.toFixed(2)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
        
         <div className="lg:col-span-1">
            <FinancialReportGenerator />
         </div>

      </div>
    </div>
  );
}
