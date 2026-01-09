'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface TaskErrorProps {
  message?: string;
}

export function TaskError({ message = 'Failed to load tasks' }: TaskErrorProps) {
  const router = useRouter();
  const [isRetrying, setIsRetrying] = useState(false);

  const handleRetry = () => {
    setIsRetrying(true);
    router.refresh();
  };

  return (
    <div className="flex flex-col items-center justify-center py-8 text-center">
      <div className="flex items-center gap-2 text-red-500 mb-4">
        <AlertCircle className="h-6 w-6" />
        <span className="font-medium">{message}</span>
      </div>

      <Button onClick={handleRetry} variant="outline" className="gap-2" disabled={isRetrying}>
        <RefreshCw className={`h-4 w-4 ${isRetrying ? 'animate-spin' : ''}`} />
        {isRetrying ? 'Retrying...' : 'Try Again'}
      </Button>
    </div>
  );
}
