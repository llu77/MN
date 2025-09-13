'use client';
import { useState } from 'react';
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from '@/components/ui/dialog';
import { PlusCircle, Trash2, Edit, ShieldAlert } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';

function NewUserForm({setOpen, onAddEmployee}) {
    const { branches } = useData();
    const [role, setRole] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [branchId, setBranchId] = useState('');

    const handleSubmit = () => {
        const newEmployee = {
            id: `emp${Date.now()}`,
            name,
            email,
            branchId: role === 'admin' ? 'all' : branchId,
            role,
            avatar: '',
        };
        onAddEmployee(newEmployee);
        setOpen(false);
    };

    return (
        <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="name" className="text-right">الاسم</Label>
                <Input id="name" placeholder="اسم الموظف" className="col-span-3" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="email" className="text-right">البريد الإلكتروني</Label>
                <Input id="email" type="email" placeholder="example@domain.com" className="col-span-3" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
             <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="role" className="text-right">الدور</Label>
                 <Select onValueChange={setRole}>
                    <SelectTrigger className="col-span-3">
                        <SelectValue placeholder="اختر دورًا" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="admin">أدمن</SelectItem>
                        <SelectItem value="supervisor">مشرف</SelectItem>
                        <SelectItem value="employee">موظف</SelectItem>
                        <SelectItem value="partner">شريك</SelectItem>
                    </SelectContent>
                </Select>
            </div>
            {role !== 'admin' && (
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="branch" className="text-right">الفرع</Label>
                    <Select onValueChange={setBranchId}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="اختر فرعًا" />
                        </SelectTrigger>
                        <SelectContent>
                            {branches.map(b => <SelectItem key={b.id} value={b.id}>{b.name}</SelectItem>)}
                        </SelectContent>
                    </Select>
                </div>
            )}
             <DialogFooter>
                <Button onClick={handleSubmit}>إنشاء مستخدم</Button>
            </DialogFooter>
        </div>
    );
}

function AccessDenied() {
    return (
        <div className="flex flex-col items-center justify-center h-[50vh] gap-4 text-center">
            <ShieldAlert className="w-16 h-16 text-destructive" />
            <h1 className="text-3xl font-bold">وصول مرفوض</h1>
            <p className="text-muted-foreground">ليس لديك الصلاحية لعرض هذه الصفحة.</p>
             <Button asChild>
                <a href="/">العودة إلى لوحة التحكم</a>
            </Button>
        </div>
    )
}


export default function UsersPage() {
    const [open, setOpen] = useState(false);
    const { user } = useAuth();
    const { employees, branches, setEmployees } = useData();

    const handleAddEmployee = (newEmployee) => {
        setEmployees(prev => [newEmployee, ...prev]);
    };
    
    const handleDeleteEmployee = (id) => {
        setEmployees(prev => prev.filter(e => e.id !== id));
    }

    if (user.role !== 'admin') {
        return <AccessDenied />;
    }

  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight font-headline">إدارة المستخدمين</h1>
          <p className="text-muted-foreground">إضافة وتعديل صلاحيات المستخدمين في النظام.</p>
        </div>
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button><PlusCircle className="ml-2 h-4 w-4" />إضافة مستخدم</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>إنشاء مستخدم جديد</DialogTitle>
                    <DialogDescription>أدخل تفاصيل المستخدم الجديد لإنشاء حسابه.</DialogDescription>
                </DialogHeader>
                <NewUserForm setOpen={setOpen} onAddEmployee={handleAddEmployee} />
            </DialogContent>
        </Dialog>
      </header>

      <Card>
        <CardHeader>
          <CardTitle>قائمة المستخدمين</CardTitle>
          <CardDescription>قائمة بجميع المستخدمين المسجلين في النظام.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الاسم</TableHead>
                <TableHead>البريد الإلكتروني</TableHead>
                <TableHead>الفرع</TableHead>
                <TableHead>الدور</TableHead>
                <TableHead className="text-left">الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {employees.map((employee) => (
                <TableRow key={employee.id}>
                  <TableCell className="font-medium">{employee.name}</TableCell>
                  <TableCell>{employee.email}</TableCell>
                  <TableCell>
                    <Badge variant={employee.branchId === 'all' ? 'default' : 'secondary'}>
                      {branches.find(b => b.id === employee.branchId)?.name || 'كل الفروع'}
                    </Badge>
                  </TableCell>
                  <TableCell>{employee.role}</TableCell>
                  <TableCell className="text-left space-x-2">
                    <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-primary"><Edit className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive" onClick={() => handleDeleteEmployee(employee.id)}><Trash2 className="h-4 w-4" /></Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
