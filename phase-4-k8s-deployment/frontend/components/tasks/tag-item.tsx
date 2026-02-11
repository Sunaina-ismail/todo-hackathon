'use client';

import { TagWithUsage } from '@/types/task';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Tag } from 'lucide-react';

interface TagItemProps {
  tag: TagWithUsage;
  isSelected?: boolean;
  onClick?: (tag: string) => void;
}

export function TagItem({ tag, isSelected = false, onClick }: TagItemProps) {
  return (
    <button
      type="button"
      onClick={() => onClick?.(tag.name)}
      className={cn(
        'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm transition-colors',
        isSelected
          ? 'bg-primary text-primary-foreground hover:bg-primary/90'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
        onClick && 'cursor-pointer'
      )}
    >
      <Tag className="h-3.5 w-3.5" />
      <span>{tag.name}</span>
      {tag.usage_count > 0 && (
        <Badge
          variant="secondary"
          className={cn(
            'h-5 min-w-5 px-1 text-xs',
            isSelected ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-600'
          )}
        >
          {tag.usage_count}
        </Badge>
      )}
    </button>
  );
}
