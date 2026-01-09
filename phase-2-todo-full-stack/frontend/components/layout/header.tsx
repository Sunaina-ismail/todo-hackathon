'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { signOutAction } from '@/actions/auth';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export function Header() {
  const pathname = usePathname();

  const navItems = [
    { href: '/dashboard', label: 'Tasks' },
    { href: '/dashboard/tags', label: 'Tags' },
  ];

  return (
    <header className="bg-white border-b shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/dashboard" className="text-xl font-bold text-primary">
            Todo App
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-4">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href as `/dashboard` | `/dashboard/tags`}
                className={cn(
                  'text-sm font-medium transition-colors hover:text-primary',
                  pathname === item.href
                    ? 'text-primary'
                    : 'text-muted-foreground'
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* User Menu */}
          <form action={signOutAction}>
            <Button type="submit" variant="outline" size="sm">
              Sign Out
            </Button>
          </form>
        </div>
      </div>
    </header>
  );
}
