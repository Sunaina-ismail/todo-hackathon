# Quickstart Guide: Modern Dashboard UI Redesign

**Feature**: 005-modern-dashboard-redesign
**Date**: 2026-01-26
**Target**: Developers implementing the Forest & Neon themed dashboard

## Overview

This guide provides step-by-step instructions for implementing the modern dashboard UI redesign with Forest & Neon color scheme. Follow these steps in order to ensure proper setup and integration.

---

## Prerequisites

- Node.js 18+ installed
- Existing Phase 3 Todo application running
- Access to the codebase at `phase-3-ai-todo-chatbot/frontend/`
- Basic knowledge of Next.js 16, TypeScript, and Tailwind CSS

---

## Step 1: Install Dependencies

Navigate to the frontend directory and install required packages:

```bash
cd phase-3-ai-todo-chatbot/frontend

# Install animation library
npm install framer-motion

# Install chart library
npm install recharts

# Install React Query for data fetching (if not already installed)
npm install @tanstack/react-query
```

---

## Step 2: Install shadcn/ui Components

Use the shadcn CLI to install required UI components:

```bash
# Install sidebar component
npx shadcn@latest add sidebar

# Install chart component
npx shadcn@latest add chart

# Install card component (if not already installed)
npx shadcn@latest add card

# Install skeleton component (if not already installed)
npx shadcn@latest add skeleton

# Install button component (if not already installed)
npx shadcn@latest add button

# Install input component (if not already installed)
npx shadcn@latest add input

# Install dialog component (if not already installed)
npx shadcn@latest add dialog

# Install dropdown-menu component (if not already installed)
npx shadcn@latest add dropdown-menu
```

---

## Step 3: Configure Tailwind with Forest & Neon Theme

Update `tailwind.config.ts` to include the Forest & Neon color palette:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          black: '#090E0C',
          charcoal: '#111814',
          gray: '#64748B',
        },
        neon: {
          lime: '#BEF264',
        },
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
```

Update `app/globals.css` with CSS variables:

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 9 14 12;           /* #090E0C */
    --foreground: 0 0% 100%;
    --card: 17 24 20;                /* #111814 */
    --card-foreground: 0 0% 100%;
    --primary: 84 81% 69%;           /* #BEF264 */
    --primary-foreground: 0 0% 0%;
    --muted: 215 20% 45%;            /* #64748B */
    --muted-foreground: 215 20% 45%;

    --sidebar-background: 17 24 20;
    --sidebar-foreground: 0 0% 100%;
    --sidebar-primary: 84 81% 69%;
    --sidebar-primary-foreground: 0 0% 0%;
    --sidebar-accent: 84 81% 69%;
    --sidebar-accent-foreground: 0 0% 0%;
  }

  body {
    @apply bg-forest-black text-white;
  }
}
```

---

## Step 4: Create Animation Variants Library

Create reusable Framer Motion animation variants:

```typescript
// lib/animations.ts
export const sidebarVariants = {
  expanded: {
    width: '240px',
    transition: { duration: 0.3, ease: 'easeInOut' }
  },
  collapsed: {
    width: '64px',
    transition: { duration: 0.3, ease: 'easeInOut' }
  }
}

export const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.2, ease: 'easeIn' }
  }
}

export const staggerVariants = {
  container: {
    animate: { transition: { staggerChildren: 0.05 } }
  },
  item: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 }
  }
}

export const fadeInVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.2 } }
}
```

---

## Step 5: Create Sidebar State Hook

Implement the sidebar state management hook:

```typescript
// hooks/use-sidebar.ts
import { useState, useEffect } from 'react'

const STORAGE_KEY = 'sidebar-collapsed'

export function useSidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored !== null) {
        setIsCollapsed(stored === 'true')
      }
    } catch (error) {
      console.warn('localStorage not available')
    }
    setIsHydrated(true)
  }, [])

  useEffect(() => {
    if (isHydrated) {
      try {
        localStorage.setItem(STORAGE_KEY, String(isCollapsed))
      } catch (error) {
        // Silently fail
      }
    }
  }, [isCollapsed, isHydrated])

  const toggle = () => setIsCollapsed(prev => !prev)
  const expand = () => setIsCollapsed(false)
  const collapse = () => setIsCollapsed(true)

  return { isCollapsed, toggle, expand, collapse, isHydrated }
}
```

---

## Step 6: Create Responsive Sidebar Component

Implement the animated sidebar:

```typescript
// components/layout/sidebar.tsx
'use client'

import { motion } from 'framer-motion'
import { useSidebar } from '@/hooks/use-sidebar'
import { sidebarVariants } from '@/lib/animations'
import { Home, CheckSquare, Tag, Settings, Menu } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function Sidebar() {
  const { isCollapsed, toggle, isHydrated } = useSidebar()
  const pathname = usePathname()

  if (!isHydrated) {
    return <div className="w-60 bg-forest-charcoal" />
  }

  const navItems = [
    { href: '/dashboard', icon: Home, label: 'Dashboard' },
    { href: '/dashboard/tasks', icon: CheckSquare, label: 'Tasks' },
    { href: '/dashboard/tags', icon: Tag, label: 'Tags' },
    { href: '/dashboard/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <motion.aside
      layout
      variants={sidebarVariants}
      animate={isCollapsed ? 'collapsed' : 'expanded'}
      className="bg-forest-charcoal border-r border-forest-gray/20 flex flex-col"
    >
      <div className="p-4 flex items-center justify-between">
        {!isCollapsed && <h2 className="text-xl font-bold">Todo</h2>}
        <button
          onClick={toggle}
          className="p-2 hover:bg-neon-lime/10 rounded-lg transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
      </div>

      <nav className="flex-1 px-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                flex items-center gap-3 px-3 py-2 rounded-lg transition-colors
                ${isActive
                  ? 'bg-neon-lime text-black'
                  : 'hover:bg-forest-gray/10 text-white'
                }
              `}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!isCollapsed && <span>{item.label}</span>}
            </Link>
          )
        })}
      </nav>
    </motion.aside>
  )
}
```

---

## Step 7: Create Chart Components

Implement Recharts components with Forest & Neon styling:

```typescript
// components/dashboard/completion-chart.tsx
'use client'

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface CompletionChartProps {
  data: Array<{ date: string; value: number; label: string }>
}

export function CompletionChart({ data }: CompletionChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="neonLimeGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#BEF264" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#BEF264" stopOpacity={0.1}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#64748B" opacity={0.2} />
        <XAxis dataKey="label" stroke="#64748B" />
        <YAxis stroke="#64748B" />
        <Tooltip
          contentStyle={{
            backgroundColor: '#111814',
            border: '1px solid #BEF264',
            borderRadius: '8px',
            color: '#FFFFFF'
          }}
        />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#BEF264"
          strokeWidth={2}
          fillOpacity={1}
          fill="url(#neonLimeGradient)"
          animationDuration={800}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
```

---

## Step 8: Add Loading States

Create loading.tsx files for all routes:

```typescript
// app/dashboard/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Skeleton key={i} className="h-32 bg-forest-charcoal" />
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Skeleton className="h-80 bg-forest-charcoal" />
        <Skeleton className="h-80 bg-forest-charcoal" />
      </div>
    </div>
  )
}
```

---

## Step 9: Integrate ChatKit

Copy ChatKit templates and customize with Forest & Neon theme:

```typescript
// components/chat/chat-button.tsx
'use client'

import { motion } from 'framer-motion'
import { MessageCircle } from 'lucide-react'
import { useState } from 'react'
import { ChatContainer } from './chat-container'

export function ChatButton() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-neon-lime text-black shadow-lg hover:shadow-xl z-50"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <MessageCircle className="w-6 h-6 mx-auto" />
      </motion.button>

      <ChatContainer isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}
```

---

## Step 10: Test Responsive Behavior

Test the implementation at all breakpoints:

```bash
# Start development server
npm run dev

# Test at different screen sizes:
# - Mobile: 375px
# - Tablet: 768px
# - Desktop: 1024px
# - Large Desktop: 1920px
```

**Testing Checklist**:
- [ ] Sidebar collapses to icons on mobile
- [ ] Sidebar toggles smoothly on all devices
- [ ] Charts are responsive and readable
- [ ] Loading states appear during navigation
- [ ] ChatKit button is accessible on all pages
- [ ] Colors match Forest & Neon palette exactly

---

## Common Issues & Solutions

### Issue: Hydration Mismatch

**Symptom**: Console warning about server/client mismatch

**Solution**: Ensure `isHydrated` flag is used before rendering dynamic content

```typescript
if (!isHydrated) {
  return <Skeleton />
}
```

### Issue: Charts Not Responsive

**Symptom**: Charts overflow container or don't resize

**Solution**: Ensure parent container has defined height

```typescript
<div className="h-80">
  <ResponsiveContainer width="100%" height="100%">
    {/* Chart */}
  </ResponsiveContainer>
</div>
```

### Issue: Animations Janky

**Symptom**: Sidebar animation stutters

**Solution**: Use `layout` prop and GPU-accelerated properties

```typescript
<motion.aside layout className="will-change-[width]">
```

---

## Next Steps

After completing this quickstart:

1. Run `/sp.tasks` to generate implementation tasks
2. Review tasks and prioritize by user story (P1-P5)
3. Begin implementation with P1 (Dashboard Visualization)
4. Test each component as you build
5. Run `/sp.implement` when ready to execute tasks

---

## Resources

- [Next.js 16 Documentation](https://nextjs.org/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Recharts Documentation](https://recharts.org)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

**Quickstart Status**: ✅ Complete
**Estimated Setup Time**: 30-45 minutes
**Ready for Implementation**: Yes
