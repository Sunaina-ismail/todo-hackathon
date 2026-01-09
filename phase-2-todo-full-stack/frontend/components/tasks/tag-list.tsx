'use client';

import { TagWithUsage } from '@/types/task';
import { TagItem } from './tag-item';
import { TagEmpty } from './tag-empty';

interface TagListProps {
  tags: TagWithUsage[];
  selectedTags?: string[];
  onTagClick?: (tag: string) => void;
  className?: string;
}

export function TagList({ tags, selectedTags = [], onTagClick, className }: TagListProps) {
  if (tags.length === 0) {
    return (
      <div className={className}>
        <TagEmpty />
      </div>
    );
  }

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {tags.map((tag) => (
        <TagItem
          key={tag.name}
          tag={tag}
          isSelected={selectedTags.includes(tag.name)}
          onClick={onTagClick}
        />
      ))}
    </div>
  );
}
