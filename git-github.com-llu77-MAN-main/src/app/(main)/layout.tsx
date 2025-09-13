'use client';
import { SidebarProvider, Sidebar, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebarContent } from '@/components/app-sidebar-content';
import { Button } from '@/components/ui/button';
import { Bell } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { notifications } from '@/lib/data';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { AuthProvider } from '@/hooks/use-auth';
import { DataProvider } from '@/hooks/use-data';

function NotificationsPopover() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {notifications.length > 0 && (
            <span className="absolute top-1 right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-primary/90"></span>
            </span>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0">
        <div className="p-4">
          <h4 className="font-medium text-lg">الإشعارات</h4>
          <p className="text-sm text-muted-foreground">لديك {notifications.length} إشعارات غير مقروءة.</p>
        </div>
        <Separator />
        <div className="max-h-96 overflow-y-auto">
          {notifications.map(notification => (
            <div key={notification.id} className="flex items-start gap-4 p-4 hover:bg-muted/50">
               <Avatar className="h-9 w-9 border">
                    <AvatarFallback>{notification.sender.substring(0, 2)}</AvatarFallback>
                </Avatar>
              <div className="grid gap-1 text-sm">
                <p className="font-semibold">{notification.sender}</p>
                <p className="text-muted-foreground">{notification.message}</p>
                <p className="text-xs text-muted-foreground">{notification.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
        {notifications.length > 0 && (
          <>
            <Separator />
            <div className="p-2">
              <Button variant="ghost" className="w-full">مسح كل الإشعارات</Button>
            </div>
          </>
        )}
      </PopoverContent>
    </Popover>
  );
}


export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      <DataProvider>
        <SidebarProvider>
          <Sidebar>
            <AppSidebarContent />
          </Sidebar>
          <div className="flex flex-col">
            <header className="sticky top-0 z-10 flex h-[57px] items-center justify-between gap-1 border-b bg-background px-4">
              <div className="flex items-center gap-1">
                <SidebarTrigger className="md:hidden" />
                <h1 className="text-xl font-semibold">BarberTrack</h1>
              </div>
              <div className="flex items-center gap-2">
                <NotificationsPopover />
              </div>
            </header>
            <SidebarInset>
                <div className="min-h-screen p-4 sm:p-6 lg:p-8">{children}</div>
            </SidebarInset>
          </div>
        </SidebarProvider>
      </DataProvider>
    </AuthProvider>
  );
}
