'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Filter, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

type Priority = 'High' | 'Medium' | 'Low' | 'all';

interface PriorityFilterProps {
  className?: string;
}

const priorities: { value: Priority; label: string }[] = [
  { value: 'all', label: 'All Priorities' },
  { value: 'High', label: 'High' },
  { value: 'Medium', label: 'Medium' },
  { value: 'Low', label: 'Low' },
];

export function PriorityFilter({ className }: PriorityFilterProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const currentPriority = (searchParams.get('priority') as Priority) || 'all';

  const handlePriorityChange = (priority: Priority) => {
    const params = new URLSearchParams(searchParams.toString());

    if (priority === 'all') {
      params.delete('priority');
    } else {
      params.set('priority', priority);
    }

    // Reset to first page when filtering
    params.delete('offset');

    router.push(`/dashboard?${params.toString()}`);
  };

  const selectedLabel = priorities.find((p) => p.value === currentPriority)?.label || 'Priority';

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className={cn('gap-2', className)}>
          <Filter className="h-4 w-4" />
          <span className="hidden sm:inline">{selectedLabel}</span>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {priorities.map((priority) => (
          <DropdownMenuItem
            key={priority.value}
            onClick={() => handlePriorityChange(priority.value)}
            className={cn(
              currentPriority === priority.value && 'bg-accent font-medium'
            )}
          >
            {priority.label}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
