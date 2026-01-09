import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

export function TaskEmpty() {
  return (
    <div className="text-center py-12">
      <div className="mb-4">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-1">
        No tasks yet
      </h3>
      <p className="text-gray-500 mb-4">
        Get started by creating your first task.
      </p>
      <Button>
        <Plus className="mr-2 h-4 w-4" />
        Create your first task
      </Button>
    </div>
  );
}
