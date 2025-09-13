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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { PlusCircle, Trash2, ShieldAlert } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';

// Re-using the NewUserForm from the users page for consistency
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

export default function SettingsPage() {
  const { user } = useAuth();
  const { 
    employees, 
    branches, 
    productCatalog, 
    expenseCategoryList,
    setEmployees,
    setBranches,
    setProductCatalog,
    setExpenseCategoryList
  } = useData();

  const [isEmployeeDialogOpen, setEmployeeDialogOpen] = useState(false);
  const [isBranchDialogOpen, setBranchDialogOpen] = useState(false);
  const [isProductDialogOpen, setProductDialogOpen] = useState(false);
  const [isExpenseItemDialogOpen, setExpenseItemDialogOpen] = useState(false);

  // Form states
  const [branchName, setBranchName] = useState('');
  const [supervisorName, setSupervisorName] = useState('');
  const [productName, setProductName] = useState('');
  const [productPrice, setProductPrice] = useState('');
  const [expenseItemName, setExpenseItemName] = useState('');


  const handleAddEmployee = (newEmployee) => {
    setEmployees(prev => [newEmployee, ...prev]);
  };

  const handleDeleteEmployee = (id) => {
    setEmployees(prev => prev.filter(e => e.id !== id));
  }

  const handleAddBranch = () => {
    const newBranch = {
        id: `branch${Date.now()}`,
        name: branchName,
        supervisor: supervisorName,
    };
    setBranches(prev => [newBranch, ...prev]);
    setBranchDialogOpen(false);
    setBranchName('');
    setSupervisorName('');
  };

  const handleDeleteBranch = (id) => {
    setBranches(prev => prev.filter(b => b.id !== id));
  }
  
  const handleAddProduct = () => {
    const newProduct = {
        id: `prod${Date.now()}`,
        name: productName,
        price: parseFloat(productPrice) || 0,
    };
    setProductCatalog(prev => [newProduct, ...prev]);
    setProductDialogOpen(false);
    setProductName('');
    setProductPrice('');
  };

  const handleDeleteProduct = (id) => {
    setProductCatalog(prev => prev.filter(p => p.id !== id));
  }

  const handleAddExpenseItem = () => {
    if (expenseItemName && !expenseCategoryList.includes(expenseItemName)) {
        setExpenseCategoryList(prev => [expenseItemName, ...prev]);
    }
    setExpenseItemDialogOpen(false);
    setExpenseItemName('');
  };

  const handleDeleteExpenseItem = (itemName) => {
    setExpenseCategoryList(prev => prev.filter(item => item !== itemName));
  }
  
  if (user.role !== 'admin') {
    return <AccessDenied />;
  }

  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold tracking-tight font-headline">الإعدادات</h1>
        <p className="text-muted-foreground">إدارة الإعدادات الأساسية للنظام.</p>
      </header>

      <Tabs defaultValue="employees">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="employees">الموظفين</TabsTrigger>
          <TabsTrigger value="branches">الفروع</TabsTrigger>
          <TabsTrigger value="products">المنتجات</TabsTrigger>
          <TabsTrigger value="expense_items">أصناف المصروفات</TabsTrigger>
        </TabsList>

        <TabsContent value="employees">
            <Card>
                <CardHeader className="flex-row items-center justify-between">
                    <div>
                        <CardTitle>إدارة الموظفين</CardTitle>
                        <CardDescription>إضافة وتعديل وحذف الموظفين في النظام.</CardDescription>
                    </div>
                    <Dialog open={isEmployeeDialogOpen} onOpenChange={setEmployeeDialogOpen}>
                      <DialogTrigger asChild>
                        <Button><PlusCircle className="ml-2 h-4 w-4" /> إضافة موظف</Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                            <DialogTitle>إنشاء مستخدم جديد</DialogTitle>
                            <DialogDescription>أدخل تفاصيل المستخدم الجديد لإنشاء حسابه.</DialogDescription>
                        </DialogHeader>
                        <NewUserForm setOpen={setEmployeeDialogOpen} onAddEmployee={handleAddEmployee} />
                      </DialogContent>
                    </Dialog>
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
                                    <TableCell>{branches.find(b => b.id === employee.branchId)?.name || 'كل الفروع'}</TableCell>
                                    <TableCell>{employee.role}</TableCell>
                                    <TableCell className="text-left">
                                        <Button variant="ghost" size="icon" onClick={() => handleDeleteEmployee(employee.id)}><Trash2 className="h-4 w-4 text-destructive" /></Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </TabsContent>
        
        <TabsContent value="branches">
          <Card>
            <CardHeader  className="flex-row items-center justify-between">
                <div>
                    <CardTitle>إدارة الفروع</CardTitle>
                    <CardDescription>إضافة فروع جديدة وتعيين مشرفين.</CardDescription>
                </div>
                 <Dialog open={isBranchDialogOpen} onOpenChange={setBranchDialogOpen}>
                  <DialogTrigger asChild>
                    <Button><PlusCircle className="ml-2 h-4 w-4" /> إضافة فرع</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>إضافة فرع جديد</DialogTitle>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="branch-name" className="text-right">اسم الفرع</Label>
                        <Input id="branch-name" className="col-span-3" value={branchName} onChange={e => setBranchName(e.target.value)} />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="supervisor-name" className="text-right">المشرف</Label>
                        <Input id="supervisor-name" className="col-span-3" value={supervisorName} onChange={e => setSupervisorName(e.target.value)} />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button onClick={handleAddBranch}>إضافة</Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
            </CardHeader>
            <CardContent>
                 <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>اسم الفرع</TableHead>
                            <TableHead>المشرف</TableHead>
                            <TableHead className="text-left">الإجراءات</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {branches.map((branch) => (
                            <TableRow key={branch.id}>
                                <TableCell>{branch.name}</TableCell>
                                <TableCell>{branch.supervisor}</TableCell>
                                <TableCell className="text-left">
                                     <Button variant="ghost" size="icon" onClick={() => handleDeleteBranch(branch.id)}><Trash2 className="h-4 w-4 text-destructive" /></Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="products">
          <Card>
            <CardHeader className="flex-row items-center justify-between">
                <div>
                    <CardTitle>إدارة المنتجات</CardTitle>
                    <CardDescription>إدارة كتالوج المنتجات والأسعار.</CardDescription>
                </div>
                 <Dialog open={isProductDialogOpen} onOpenChange={setProductDialogOpen}>
                    <DialogTrigger asChild>
                        <Button><PlusCircle className="ml-2 h-4 w-4" /> إضافة منتج</Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>إضافة منتج جديد</DialogTitle>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="product-name" className="text-right">اسم المنتج</Label>
                                <Input id="product-name" className="col-span-3" value={productName} onChange={e => setProductName(e.target.value)} />
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="product-price" className="text-right">السعر (ر.س)</Label>
                                <Input id="product-price" type="number" className="col-span-3" value={productPrice} onChange={e => setProductPrice(e.target.value)} />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button onClick={handleAddProduct}>إضافة</Button>
                        </DialogFooter>
                    </DialogContent>
                 </Dialog>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>اسم المنتج</TableHead>
                            <TableHead>السعر</TableHead>
                             <TableHead className="text-left">الإجراءات</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {productCatalog.map((product) => (
                            <TableRow key={product.id}>
                                <TableCell>{product.name}</TableCell>
                                <TableCell>ر.س {product.price.toFixed(2)}</TableCell>
                                <TableCell className="text-left">
                                     <Button variant="ghost" size="icon" onClick={() => handleDeleteProduct(product.id)}><Trash2 className="h-4 w-4 text-destructive" /></Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="expense_items">
          <Card>
            <CardHeader className="flex-row items-center justify-between">
                <div>
                    <CardTitle>أصناف المصروفات</CardTitle>
                    <CardDescription>إدارة فئات المصروفات التي يمكن للمشرفين استخدامها.</CardDescription>
                </div>
                <Dialog open={isExpenseItemDialogOpen} onOpenChange={setExpenseItemDialogOpen}>
                    <DialogTrigger asChild>
                        <Button><PlusCircle className="ml-2 h-4 w-4" /> إضافة صنف</Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>إضافة صنف مصروف جديد</DialogTitle>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="item-name" className="text-right">اسم الصنف</Label>
                                <Input id="item-name" className="col-span-3" value={expenseItemName} onChange={e => setExpenseItemName(e.target.value)} />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button onClick={handleAddExpenseItem}>إضافة</Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </CardHeader>
            <CardContent>
               <div className="flex flex-wrap gap-3">
                    {expenseCategoryList.map((category) => (
                        <div key={category} className="flex items-center gap-2 rounded-md border p-2 pl-3">
                            <span>{category}</span>
                            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => handleDeleteExpenseItem(category)}><Trash2 className="h-4 w-4 text-destructive" /></Button>
                        </div>
                    ))}
               </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );

    

}
