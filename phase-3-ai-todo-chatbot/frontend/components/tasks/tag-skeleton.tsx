'use client';

export function TagSkeleton() {
  return (
    <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-gray-100 animate-pulse">
      <div className="h-3.5 w-3.5 bg-gray-200 rounded" />
      <div className="h-4 w-16 bg-gray-200 rounded" />
      <div className="h-5 w-5 bg-gray-200 rounded-full" />
    </div>
  );
}
