'use client';

import { useState, useTransition } from 'react';
import { deleteTask } from '@/actions/tasks';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Loader2, Trash2, AlertTriangle } from 'lucide-react';

interface DeleteDialogProps {
  taskId: string;
  taskTitle: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export function DeleteDialog({
  taskId,
  taskTitle,
  open,
  onOpenChange,
  onSuccess,
}: DeleteDialogProps) {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleDelete() {
    setError(null);
    startTransition(async () => {
      const result = await deleteTask(taskId);

      if (result?.error) {
        setError(result.error);
      } else if (result?.success) {
        onOpenChange(false);
        onSuccess?.();
      }
    });
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[400px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            Delete Task
          </DialogTitle>
          <DialogDescription>
            Are you sure you want to delete &quot;{taskTitle}&quot;? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        {error && (
          <div className="p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded-md">
            {error}
          </div>
        )}

        <DialogFooter className="sm:justify-end">
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isPending}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={handleDelete}
            disabled={isPending}
          >
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Deleting...
              </>
            ) : (
              <>
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
