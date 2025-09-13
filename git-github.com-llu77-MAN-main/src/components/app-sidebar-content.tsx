'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Banknote,
  Award,
  ClipboardList,
  ShoppingBag,
  FileBarChart,
  LogOut,
  Receipt,
  Warehouse,
  Users,
  Settings,
  HandCoins,
  ShieldCheck,
} from 'lucide-react';

import {
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarTrigger,
  SidebarSeparator,
  SidebarGroup,
  SidebarGroupLabel,
  useSidebar,
} from '@/components/ui/sidebar';
import { Icons } from '@/components/icons';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useAuth } from '@/hooks/use-auth';


const mainNavItems = [
  { href: '/', label: 'لوحة التحكم', icon: LayoutDashboard },
  { href: '/revenue', label: 'الإيرادات', icon: Banknote },
  { href: '/expenses', label: 'المصروفات', icon: Receipt },
  { href: '/bonuses', label: 'البونص', icon: Award },
  { href: '/requests', label: 'طلبات الموظفين', icon: ClipboardList, roles: ['supervisor', 'admin'] },
  { href: '/my-requests', label: 'طلباتي', icon: ClipboardList, roles: ['employee', 'supervisor'] },
  { href: '/orders', label: 'طلبات المنتجات', icon: ShoppingBag },
  { href: '/inventory', label: 'إدارة المخزون', icon: Warehouse },
  { href: '/reports', label: 'التقارير', icon: FileBarChart },
];

const adminNavItems = [
    { href: '/payroll', label: 'الرواتب', icon: HandCoins, roles: ['admin', 'supervisor'] },
    { href: '/admin/requests', label: 'إدارة الطلبات', icon: ShieldCheck, roles: ['admin']},
    { href: '/admin/users', label: 'إدارة المستخدمين', icon: Users, roles: ['admin'] },
    { href: '/admin/settings', label: 'الإعدادات', icon: Settings, roles: ['admin'] },
]

export function AppSidebarContent() {
  const pathname = usePathname();
  const { user } = useAuth();
  const { setOpenMobile, isMobile } = useSidebar();

  const isActive = (href: string) => {
    // Make sure the comparison is strict for the homepage and loose for others.
    return href === '/' ? pathname === '/' : pathname.startsWith(href);
  };
  
  const userCanSee = (item) => !item.roles || item.roles.includes(user.role);

  const handleClick = () => {
    if (isMobile) {
      setOpenMobile(false);
    }
  }

  return (
    <>
      <SidebarHeader className="p-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <Icons.logo className="size-8 text-primary" />
          <div className="flex flex-col">
            <h2 className="text-lg font-bold tracking-tight font-headline group-data-[collapsible=icon]:hidden">BarberTrack</h2>
          </div>
        </Link>
        <SidebarTrigger className="hidden md:flex" />
      </SidebarHeader>
      <SidebarContent className="p-2">
        <SidebarMenu>
          {mainNavItems.filter(userCanSee).map((item) => (
            <SidebarMenuItem key={item.label} onClick={handleClick}>
              <Link href={item.href}>
                <SidebarMenuButton isActive={isActive(item.href)} tooltip={item.label}>
                  <item.icon />
                  <span>{item.label}</span>
                </SidebarMenuButton>
              </Link>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
        
        <SidebarSeparator className="my-2" />

        <SidebarGroup>
            <SidebarGroupLabel>الإدارة</SidebarGroupLabel>
            <SidebarMenu>
                 {adminNavItems.filter(userCanSee).map((item) => (
                    <SidebarMenuItem key={item.label} onClick={handleClick}>
                        <Link href={item.href}>
                            <SidebarMenuButton isActive={isActive(item.href)} tooltip={item.label}>
                            <item.icon />
                            <span>{item.label}</span>
                            </SidebarMenuButton>
                        </Link>
                    </SidebarMenuItem>
                ))}
            </SidebarMenu>
        </SidebarGroup>

      </SidebarContent>
      <SidebarFooter className="p-2">
        <SidebarSeparator className="my-2 bg-sidebar-border" />
        <div className="flex flex-col gap-2">
          <SidebarMenu>
            <SidebarMenuItem>
                <SidebarMenuButton>
                  <Avatar className="size-7">
                    <AvatarFallback>{user.name.substring(0,2)}</AvatarFallback>
                  </Avatar>
                  <span className="truncate">{user.name}</span>
                </SidebarMenuButton>
            </SidebarMenuItem>
             <SidebarMenuItem>
                 <SidebarMenuButton>
                    <LogOut />
                    <span>تسجيل الخروج</span>
                 </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>
      </SidebarFooter>
    </>
  );
}
