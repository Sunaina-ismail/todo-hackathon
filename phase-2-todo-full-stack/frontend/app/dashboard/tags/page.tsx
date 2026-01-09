import { Suspense } from 'react';
import { TagList } from '@/components/tasks/tag-list';
import { TagSkeleton } from '@/components/tasks/tag-skeleton';
import { fetchTags } from '@/actions/tasks';

// Force dynamic rendering to avoid static generation (requires authenticated user)
export const dynamic = 'force-dynamic';

export default async function TagsPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Tags</h1>
        <p className="text-muted-foreground mt-1">
          View and manage all your task tags
        </p>
      </div>

      {/* Tag List */}
      <Suspense fallback={<TagsSkeleton />}>
        <TagsListWrapper />
      </Suspense>
    </div>
  );
}

async function TagsListWrapper() {
  try {
    const tagsResponse = await fetchTags();

    if (tagsResponse.error) {
      return (
        <div className="border rounded-lg bg-card p-6">
          <div className="text-center text-destructive">
            {tagsResponse.error}
          </div>
        </div>
      );
    }

    const tags = tagsResponse.tags || [];

    if (tags.length === 0) {
      return (
        <div className="border rounded-lg bg-card">
          <div className="p-6 text-center text-muted-foreground">
            No tags yet
          </div>
        </div>
      );
    }

    return (
      <div className="border rounded-lg bg-card p-6">
        <TagList tags={tags} className="mt-4" />
      </div>
    );
  } catch (error) {
    console.error('Error loading tags:', error);
    return (
      <div className="border rounded-lg bg-card p-6">
        <div className="text-center text-destructive">
          Failed to load tags. Please try again.
        </div>
      </div>
    );
  }
}

function TagsSkeleton() {
  return (
    <div className="border rounded-lg bg-card p-6">
      <div className="flex flex-wrap gap-2">
        <TagSkeleton />
        <TagSkeleton />
        <TagSkeleton />
        <TagSkeleton />
      </div>
    </div>
  );
}
