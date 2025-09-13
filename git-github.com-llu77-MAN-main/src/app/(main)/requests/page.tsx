'use client';
import { useState, useMemo } from 'react';
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
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { CheckCircle, XCircle, AlertTriangle, ShieldCheck, UserCheck, ShieldAlert, Eye } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { useAuth } from '@/hooks/use-auth';
import { useData } from '@/hooks/use-data';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogFooter, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { format } from 'date-fns';


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
};

function RequestDetailsDialog({ request, onOpenChange }) {
    if (!request) return null;
    
    const detailFields = {
        'طلب سلفة': { 'المبلغ المطلوب': `ر.س ${request.details.amount}` },
        'طلب صرف متأخرات': { 'المبلغ المطلوب': `ر.س ${request.details.amount}` },
        'طلب إجازة': { 'سبب الإجازة': request.details.leaveReason, 'تفاصيل إضافية': request.details.details },
        'طلب استقالة': { 'خطاب الاستقالة': request.details.resignationReason },
        'طلب صيانة': { 'تفاصيل الصيانة': request.details.maintenanceDetails, 'تفاصيل إضافية': request.details.details },
        'طلب مراجعة فاتورة': { 'رقم الفاتورة': request.details.invoiceNumber, 'تاريخ الفاتورة': format(new Date(request.details.invoiceDate), "PPP") },
    };

    const detailsToShow = detailFields[request.type] || {};

    return (
        <Dialog open={!!request} onOpenChange={onOpenChange}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>تفاصيل الطلب - {request.id}</DialogTitle>
                    <DialogDescription>مقدم من: {request.employee}</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-3 gap-2 items-center">
                        <Label>نوع الطلب:</Label>
                        <span className="col-span-2">{request.type}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 items-center">
                        <Label>التاريخ:</Label>
                        <span className="col-span-2">{request.date}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 items-center">
                        <Label>الحالة:</Label>
                         <Badge variant="outline" className={cn("gap-1.5 whitespace-nowrap col-span-2", getStatusVariant(request.status))}>
                            {statusIcons[request.status]}
                            {request.status}
                        </Badge>
                    </div>
                    {Object.entries(detailsToShow).map(([label, value]) => value && (
                         <div key={label} className="grid grid-cols-3 gap-2 items-start">
                            <Label>{label}:</Label>
                            <p className="col-span-2 text-sm text-muted-foreground whitespace-pre-wrap">{value}</p>
                        </div>
                    ))}
                </div>
                 <DialogFooter>
                    <Button variant="outline" onClick={() => onOpenChange(false)}>إغلاق</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}


function AccessDenied() {
    return (
        <div className="flex flex-col items-center justify-center h-[50vh] gap-4 text-center">
            <ShieldAlert className="w-16 h-16 text-destructive" />
            <h1 className="text-3xl font-bold">وصول مرفوض</h1>
            <p className="text-muted-foreground">هذه الصفحة مخصصة للمشرفين فقط. إذا كنت أدمن، يرجى استخدام صفحة إدارة الطلبات.</p>
             <Button asChild>
                <a href="/">العودة إلى لوحة التحكم</a>
            </Button>
        </div>
    )
}

export default function RequestsPage() {
  const { user } = useAuth();
  const { employeeRequests, updateRequestStatus, employees, requestTypes } = useData();
  const [selectedRequest, setSelectedRequest] = useState(null);
  const allRequestTypes = ['الكل', ...requestTypes];

  const supervisorBranchId = useMemo(() => employees.find(e => e.id === user.id)?.branchId, [user.id, employees]);
  
  const filteredRequests = useMemo(() => {
    if (user.role !== 'supervisor') return [];
    
    const branchEmployeeNames = employees.filter(e => e.branchId === supervisorBranchId).map(e => e.name);
    
    return employeeRequests.filter(req => {
        return branchEmployeeNames.includes(req.employee) && req.status === 'قيد انتظار موافقة المشرف';
    });
  }, [employeeRequests, user.role, supervisorBranchId, employees]);


  const handleUpdateRequestStatus = (id: string, newStatus: 'approve' | 'reject') => {
      updateRequestStatus(id, newStatus);
  }

  if (user.role !== 'supervisor') {
      return <AccessDenied />
  }

  return (
    <div className="flex flex-col gap-8">
      <header className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight font-headline">مراجعة طلبات الموظفين</h1>
          <p className="text-muted-foreground">مراجعة الطلبات المعلقة من موظفي فرعك.</p>
        </div>
      </header>
       <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>مرحلة مراجعة المشرف</AlertTitle>
          <AlertDescription>
            أنت في المرحلة الأولى من المراجعة. بمجرد موافقتك، سيتم إرسال الطلب إلى الأدمن للموافقة النهائية.
          </AlertDescription>
        </Alert>

      <Card>
        <CardContent className="p-0">
          <Tabs defaultValue="الكل">
            <TabsList className="p-2 h-auto flex-wrap justify-start bg-transparent">
              {allRequestTypes.map(type => (
                <TabsTrigger key={type} value={type} className="m-1">{type}</TabsTrigger>
              ))}
            </TabsList>
            
            <TabsContent value="الكل" className="p-0">
               <div className="overflow-x-auto">
                <Table>
                    <TableHeader>
                    <TableRow>
                        <TableHead>الموظف</TableHead>
                        <TableHead>النوع</TableHead>
                        <TableHead>التاريخ</TableHead>
                        <TableHead>الحالة</TableHead>
                        <TableHead className="text-left">الإجراءات</TableHead>
                    </TableRow>
                    </TableHeader>
                    <TableBody>
                    {filteredRequests.length > 0 ? filteredRequests.map(req => (
                        <TableRow key={req.id}>
                        <TableCell className="font-medium flex items-center gap-3">
                            <Avatar className="h-8 w-8">
                            <AvatarFallback>{req.employee.substring(0, 2)}</AvatarFallback>
                            </Avatar>
                            {req.employee}
                        </TableCell>
                        <TableCell>{req.type}</TableCell>
                        <TableCell>{req.date}</TableCell>
                        <TableCell>
                            <Badge variant="outline" className={cn("gap-1.5 whitespace-nowrap", getStatusVariant(req.status))}>
                            {statusIcons[req.status]}
                            {req.status}
                            </Badge>
                        </TableCell>
                        <TableCell className="text-left">
                            {(req.status === 'قيد انتظار موافقة المشرف') && (
                                <div className="flex items-center justify-start space-x-1">
                                    <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-primary" onClick={() => setSelectedRequest(req)}>
                                        <Eye className="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="icon" className="text-green-400 hover:text-green-300" onClick={() => handleUpdateRequestStatus(req.id, 'approve')}>
                                        <CheckCircle className="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="icon" className="text-red-400 hover:text-red-300" onClick={() => handleUpdateRequestStatus(req.id, 'reject')}>
                                        <XCircle className="h-4 w-4" />
                                    </Button>
                                </div>
                            )}
                        </TableCell>
                        </TableRow>
                    )) : (
                        <TableRow>
                            <TableCell colSpan={5} className="text-center text-muted-foreground p-8">
                                لا توجد طلبات معلقة للمراجعة في فرعك حاليًا.
                            </TableCell>
                        </TableRow>
                    )}
                    </TableBody>
                </Table>
               </div>
            </TabsContent>
            
            {requestTypes.map(type => (
                 <TabsContent key={type} value={type} className="p-0">
                     <div className="overflow-x-auto">
                        <Table>
                            <TableHeader>
                            <TableRow>
                                <TableHead>الموظف</TableHead>
                                <TableHead>النوع</TableHead>
                                <TableHead>التاريخ</TableHead>
                                <TableHead>الحالة</TableHead>
                                <TableHead className="text-left">الإجراءات</TableHead>
                            </TableRow>
                            </TableHeader>
                            <TableBody>
                            {filteredRequests.filter(r => r.type === type).length > 0 ? (
                                filteredRequests.filter(r => r.type === type).map(req => (
                                    <TableRow key={req.id}>
                                        <TableCell className="font-medium flex items-center gap-3">
                                            <Avatar className="h-8 w-8">
                                            <AvatarFallback>{req.employee.substring(0,2)}</AvatarFallback>
                                            </Avatar>
                                            {req.employee}
                                        </TableCell>
                                        <TableCell>{req.type}</TableCell>
                                        <TableCell>{req.date}</TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className={cn("gap-1.5 whitespace-nowrap", getStatusVariant(req.status))}>
                                            {statusIcons[req.status]}
                                            {req.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-left">
                                            {(req.status === 'قيد انتظار موافقة المشرف') && (
                                                <div className="flex items-center justify-start space-x-1">
                                                     <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-primary" onClick={() => setSelectedRequest(req)}>
                                                        <Eye className="h-4 w-4" />
                                                    </Button>
                                                    <Button variant="ghost" size="icon" className="text-green-400 hover:text-green-300" onClick={() => handleUpdateRequestStatus(req.id, 'approve')}>
                                                        <CheckCircle className="h-4 w-4" />
                                                    </Button>
                                                    <Button variant="ghost" size="icon" className="text-red-400 hover:text-red-300" onClick={() => handleUpdateRequestStatus(req.id, 'reject')}>
                                                        <XCircle className="h-4 w-4" />
                                                    </Button>
                                                </div>
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={5} className="text-center text-muted-foreground p-8">
                                         لا توجد طلبات من نوع "{type}" للمراجعة حاليًا.
                                    </TableCell>
                                </TableRow>
                            )}
                           </TableBody>
                        </Table>
                     </div>
                 </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>
      
      <RequestDetailsDialog request={selectedRequest} onOpenChange={() => setSelectedRequest(null)} />
    </div>
  );
}
