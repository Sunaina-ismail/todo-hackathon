'use client';

import { useState, useTransition } from 'react';
import { Task } from '@/types/task';
import { toggleTaskComplete } from '@/actions/tasks';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { formatDate } from '@/lib/utils';
import { cn } from '@/lib/utils';
import { Edit, Trash2, AlertCircle } from 'lucide-react';
import { EditTaskForm } from './edit-task-form';
import { DeleteDialog } from './delete-dialog';

interface TaskItemProps {
  task: Task;
  onUpdate?: (task: Task) => void;
  onToggle?: (taskId: string, completed: boolean) => void;
}

export function TaskItem({ task, onUpdate, onToggle }: TaskItemProps) {
  // startTransition is reserved for future use with React Suspense
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_startTransition, _setTransition] = useTransition();
  const [isPending, _setPending] = useTransition();
  const [isToggling, setIsToggling] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [optimisticCompleted, setOptimisticCompleted] = useState(task.completed);

  const priorityColors = {
    High: 'bg-red-100 text-red-800',
    Medium: 'bg-yellow-100 text-yellow-800',
    Low: 'bg-green-100 text-green-800',
  };

  const handleToggle = async () => {
    setError(null);
    const newCompleted = !optimisticCompleted;

    // Optimistic update - immediately update UI
    setOptimisticCompleted(newCompleted);
    setIsToggling(true);

    try {
      const result = await toggleTaskComplete(task.id, task.completed);

      if (result.error) {
        // Revert on error
        setOptimisticCompleted(!newCompleted);
        setError(result.error);
      } else {
        // Update from response to get the server-completed state
        if (result.task) {
          setOptimisticCompleted(result.task.completed);
        }
        // Notify parent
        onToggle?.(task.id, newCompleted);
      }
    } catch (err) {
      // Revert on error
      setOptimisticCompleted(!newCompleted);
      setError('Failed to update task');
      console.error('Failed to toggle task:', err);
    } finally {
      setIsToggling(false);
    }
  };

  const handleEditSuccess = () => {
    onUpdate?.(task);
  };

  const isLoading = isPending || isToggling;

  return (
    <>
      <div
        className={cn(
          'flex items-start gap-4 p-4 bg-white border rounded-lg shadow-sm transition-all relative',
          isLoading && 'opacity-50',
          optimisticCompleted && 'bg-gray-50'
        )}
      >
        {/* Error message */}
        {error && (
          <div className="absolute top-2 right-2 flex items-center gap-1 text-xs text-red-500">
            <AlertCircle className="h-3 w-3" />
            {error}
          </div>
        )}

        {/* Checkbox */}
        <div className="flex-shrink-0 mt-1">
          <Checkbox
            checked={optimisticCompleted}
            onCheckedChange={handleToggle}
            disabled={isLoading}
          />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h3
                className={cn(
                  'font-medium truncate',
                  optimisticCompleted && 'line-through text-gray-500'
                )}
              >
                {task.title}
              </h3>

              {task.description && (
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                  {task.description}
                </p>
              )}

              <div className="flex items-center gap-3 mt-2">
                {/* Priority Badge */}
                <Badge className={priorityColors[task.priority]}>
                  {task.priority}
                </Badge>

                {/* Due Date */}
                {task.due_date && (
                  <span className="text-xs text-gray-500">
                    Due: {formatDate(task.due_date)}
                  </span>
                )}

                {/* Tags */}
                {task.tags && task.tags.length > 0 && (
                  <div className="flex gap-1 flex-wrap">
                    {task.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="outline" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {task.tags.length > 3 && (
                      <span className="text-xs text-gray-400">
                        +{task.tags.length - 3}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => setIsEditing(true)}
                disabled={isLoading}
              >
                <Edit className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-red-500 hover:text-red-600 hover:bg-red-50"
                onClick={() => setShowDeleteDialog(true)}
                disabled={isLoading}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Dialog */}
      <EditTaskForm
        task={task}
        open={isEditing}
        onOpenChange={setIsEditing}
        onSuccess={handleEditSuccess}
      />

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        taskId={task.id}
        taskTitle={task.title}
        open={showDeleteDialog}
        onOpenChange={setShowDeleteDialog}
        onSuccess={() => {}}
      />
    </>
  );
}
