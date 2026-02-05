'use client';

import { useState } from 'react';
import { Task } from '@/types/task';
import { TaskItem } from './task-item';

interface TaskListProps {
  initialTasks: Task[];
}

export function TaskList({ initialTasks }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);

  const handleToggle = (taskId: string, completed: boolean) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, completed } : t))
    );
  };

  const handleUpdate = (updatedTask: Task) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
  };

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdate={handleUpdate}
          onToggle={handleToggle}
        />
      ))}

      {tasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No tasks found. Create your first task!
        </div>
      )}
    </div>
  );
}
