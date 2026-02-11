'use client';

import { Tag } from 'lucide-react';

export function TagEmpty() {
  return (
    <div className="flex flex-col items-center justify-center py-8 text-center">
      <Tag className="h-8 w-8 text-gray-300 mb-2" />
      <p className="text-sm text-gray-500">No tags yet</p>
      <p className="text-xs text-gray-400 mt-1">
        Add tags to your tasks to see them here
      </p>
    </div>
  );
}
