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
import { Input } from '@/components/ui/input';
import { productCatalog } from '@/lib/data';
import { cn } from '@/lib/utils';
import { Search } from 'lucide-react';

const REORDER_THRESHOLD = 10;

export default function InventoryPage() {
  const [searchTerm, setSearchTerm] = useState('');
  
  // In a real app, inventory would be fetched and would be different from the catalog
  const inventoryData = productCatalog.map(p => ({
    ...p,
    stock: Math.floor(Math.random() * 50) + 1, // Random stock for demo
  }));

  const filteredProducts = inventoryData.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold tracking-tight font-headline">إدارة المخزون</h1>
        <p className="text-muted-foreground">تتبع كميات المنتجات المتوفرة لديك.</p>
      </header>

      <Card>
        <CardHeader>
          <CardTitle>مخزون المنتجات</CardTitle>
          <CardDescription>قائمة بجميع المنتجات في المخزون والكميات المتاحة.</CardDescription>
          <div className="relative pt-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="ابحث عن منتج..."
              className="pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المنتج</TableHead>
                <TableHead>سعر الوحدة</TableHead>
                <TableHead>الكمية في المخزون</TableHead>
                <TableHead className="text-left">الحالة</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredProducts.map((product) => (
                <TableRow key={product.id}>
                  <TableCell className="font-medium">{product.name}</TableCell>
                  <TableCell>ر.س {product.price.toFixed(2)}</TableCell>
                  <TableCell>{product.stock}</TableCell>
                  <TableCell className="text-left">
                    <Badge variant="outline" className={cn(
                        product.stock > REORDER_THRESHOLD && 'text-green-400 border-green-500/30',
                        product.stock <= REORDER_THRESHOLD && product.stock > 0 && 'text-yellow-400 border-yellow-500/30',
                        product.stock === 0 && 'text-red-400 border-red-500/30'
                    )}>
                      {product.stock > REORDER_THRESHOLD ? 'متوفر' : product.stock > 0 ? 'كمية منخفضة' : 'نفذ المخزون'}
                    </Badge>
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
