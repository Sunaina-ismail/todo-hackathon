'use client';

import { useState, useTransition } from 'react';
import { Task } from '@/types/task';
import { updateTask } from '@/actions/tasks';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Loader2 } from 'lucide-react';

interface EditTaskFormProps {
  task: Task;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export function EditTaskForm({
  task,
  open,
  onOpenChange,
  onSuccess,
}: EditTaskFormProps) {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const formData = new FormData(event.currentTarget);
    const title = formData.get('title') as string;
    const description = formData.get('description') as string | null;
    const priority = formData.get('priority') as 'High' | 'Medium' | 'Low' | null;
    const dueDate = formData.get('due_date') as string | null;
    const tagsStr = formData.get('tags') as string | null;

    // Parse tags
    const tags = tagsStr
      ? tagsStr.split(',').map((t) => t.trim()).filter((t) => t.length > 0)
      : undefined;

    startTransition(async () => {
      const result = await updateTask(task.id, {
        title: title.trim(),
        description: description?.trim() || undefined,
        priority: priority || 'Medium',
        due_date: dueDate || undefined,
        tags,
      });

      if (result?.error) {
        setError(result.error);
      } else {
        onOpenChange(false);
        onSuccess?.();
      }
    });
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
          <DialogDescription>
            Make changes to your task here. Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded-md">
              {error}
            </div>
          )}

          {/* Title - Required */}
          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              name="title"
              defaultValue={task.title}
              placeholder="Enter task title"
              required
              disabled={isPending}
              maxLength={200}
            />
          </div>

          {/* Description - Optional */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              defaultValue={task.description || ''}
              placeholder="Enter task description (optional)"
              disabled={isPending}
              rows={3}
            />
          </div>

          {/* Priority and Due Date - Row */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="priority">Priority</Label>
              <Select
                name="priority"
                defaultValue={task.priority}
                disabled={isPending}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="High">High</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="Low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="due_date">Due Date</Label>
              <Input
                id="due_date"
                name="due_date"
                type="date"
                defaultValue={task.due_date || ''}
                disabled={isPending}
              />
            </div>
          </div>

          {/* Tags - Optional */}
          <div className="space-y-2">
            <Label htmlFor="tags">Tags</Label>
            <Input
              id="tags"
              name="tags"
              defaultValue={task.tags?.join(', ') || ''}
              placeholder="work, home, urgent (comma-separated)"
              disabled={isPending}
            />
            <p className="text-xs text-gray-500">Separate tags with commas</p>
          </div>

          {/* Submit Button */}
          <DialogFooter className="sm:justify-end">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isPending}>
              {isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                'Save Changes'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
