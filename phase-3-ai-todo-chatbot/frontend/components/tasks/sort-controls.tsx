'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ArrowUpDown, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { TaskSortBy, TaskSortDirection } from '@/types/task';

interface SortControlsProps {
  className?: string;
}

const sortOptions: { value: TaskSortBy; label: string }[] = [
  { value: 'created', label: 'Date Created' },
  { value: 'due_date', label: 'Due Date' },
  { value: 'priority', label: 'Priority' },
  { value: 'title', label: 'Title' },
];

export function SortControls({ className }: SortControlsProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const currentSortBy = (searchParams.get('sort_by') as TaskSortBy) || 'created';
  const currentDirection = (searchParams.get('sort_direction') as TaskSortDirection) || 'desc';

  const handleSortChange = (sortBy: TaskSortBy) => {
    const params = new URLSearchParams(searchParams.toString());

    // Toggle direction if clicking the same sort field
    if (currentSortBy === sortBy) {
      const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
      params.set('sort_direction', newDirection);
    } else {
      // New field, default to descending
      params.set('sort_by', sortBy);
      params.set('sort_direction', 'desc');
    }

    router.push(`/dashboard/tasks?${params.toString()}`);
  };

  const selectedLabel = sortOptions.find((s) => s.value === currentSortBy)?.label || 'Sort By';

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className={cn('gap-2', className)}>
          <ArrowUpDown className="h-4 w-4" />
          <span className="hidden sm:inline">{selectedLabel}</span>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {sortOptions.map((option) => (
          <DropdownMenuItem
            key={option.value}
            onClick={() => handleSortChange(option.value)}
            className={cn(
              currentSortBy === option.value && 'bg-accent font-medium'
            )}
          >
            <span>{option.label}</span>
            {currentSortBy === option.value && (
              <span className="ml-2 text-xs text-gray-500">
                {currentDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
