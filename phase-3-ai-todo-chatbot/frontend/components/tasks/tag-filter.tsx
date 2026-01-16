'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tag, X, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';

interface TagFilterProps {
  availableTags: string[];
  className?: string;
}

export function TagFilter({ availableTags, className }: TagFilterProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isOpen, setIsOpen] = useState(false);

  const selectedTags = searchParams.get('tags')?.split(',').filter(Boolean) || [];

  const handleTagToggle = (tag: string) => {
    const params = new URLSearchParams(searchParams.toString());
    const currentTags = selectedTags;

    let newTags: string[];
    if (currentTags.includes(tag)) {
      newTags = currentTags.filter((t) => t !== tag);
    } else {
      newTags = [...currentTags, tag];
    }

    if (newTags.length > 0) {
      params.set('tags', newTags.join(','));
    } else {
      params.delete('tags');
    }

    // Reset to first page when filtering
    params.delete('offset');

    router.push(`/dashboard?${params.toString()}`);
  };

  const handleClearAll = () => {
    const params = new URLSearchParams(searchParams.toString());
    params.delete('tags');
    params.delete('offset');
    router.push(`/dashboard?${params.toString()}`);
  };

  const selectedCount = selectedTags.length;

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className={cn('gap-2', className)}>
          <Tag className="h-4 w-4" />
          <span className="hidden sm:inline">Tags</span>
          {selectedCount > 0 && (
            <Badge variant="secondary" className="h-5 px-1.5 text-xs">
              {selectedCount}
            </Badge>
          )}
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        {availableTags.length === 0 ? (
          <div className="p-2 text-sm text-gray-500 text-center">
            No tags available
          </div>
        ) : (
          <>
            {availableTags.map((tag) => (
              <DropdownMenuCheckboxItem
                key={tag}
                checked={selectedTags.includes(tag)}
                onCheckedChange={() => handleTagToggle(tag)}
              >
                <Badge variant="outline" className="mr-2 text-xs">
                  {tag}
                </Badge>
              </DropdownMenuCheckboxItem>
            ))}
            {selectedCount > 0 && (
              <>
                <div className="border-t my-1" />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleClearAll}
                  className="w-full justify-center text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <X className="h-4 w-4 mr-2" />
                  Clear all tags
                </Button>
              </>
            )}
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
