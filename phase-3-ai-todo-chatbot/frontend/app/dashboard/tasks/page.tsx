import { Suspense } from 'react'
import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { TaskList } from '@/components/tasks/task-list'
import { TaskSkeleton } from '@/components/tasks/task-skeleton'
import { TaskEmpty } from '@/components/tasks/task-empty'
import { TaskError } from '@/components/tasks/task-error'
import { SearchInput } from '@/components/tasks/search-input'
import { PriorityFilter } from '@/components/tasks/priority-filter'
import { TagFilter } from '@/components/tasks/tag-filter'
import { SortControls } from '@/components/tasks/sort-controls'
import { PaginationControls } from '@/components/tasks/pagination-controls'
import { AddTaskButton } from '@/components/tasks/add-task-button'
import { fetchTasks, fetchTags } from '@/actions/tasks'

// Force dynamic rendering to avoid static generation (requires authenticated user)
export const dynamic = 'force-dynamic'

interface TasksPageProps {
  searchParams: Promise<{
    search?: string
    status?: string
    priority?: string
    tags?: string
    sort_by?: string
    sort_direction?: string
    offset?: string
  }>
}

export default async function TasksPage({ searchParams }: TasksPageProps) {
  // Get authenticated user
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session?.user) {
    redirect('/sign-in')
  }

  const params = await searchParams

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            My Tasks
          </h1>
          <p className="text-forest-gray mt-1">
            Manage and organize your tasks efficiently
          </p>
        </div>
        <AddTaskButton />
      </div>

      {/* Search and Filters */}
      <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-4">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <SearchInput />
          </div>
          <div className="flex flex-wrap gap-2">
            <PriorityFilter />
            <SortControls />
          </div>
        </div>
      </div>

      {/* Task List */}
      <Suspense fallback={<TaskListSkeleton />}>
        <TaskListWrapper searchParams={params} />
      </Suspense>
    </div>
  )
}

async function TaskListWrapper({
  searchParams,
}: {
  searchParams: {
    search?: string
    status?: string
    priority?: string
    tags?: string
    sort_by?: string
    sort_direction?: string
    offset?: string
  }
}) {
  try {
    // Parse filter parameters
    const search = searchParams.search
    const status = searchParams.status || 'all'
    const priority = searchParams.priority as 'High' | 'Medium' | 'Low' | 'all' | undefined
    const tags = searchParams.tags?.split(',').filter(Boolean)
    const sortBy = searchParams.sort_by as 'created' | 'due_date' | 'priority' | 'title' | undefined
    const sortDirection = searchParams.sort_direction as 'asc' | 'desc' | undefined
    const offset = searchParams.offset ? parseInt(searchParams.offset, 10) : undefined

    // Fetch filtered tasks
    const response = await fetchTasks({
      search,
      status,
      priority: priority || 'all',
      tags,
      sort_by: sortBy || 'created',
      sort_direction: sortDirection || 'desc',
      limit: 10,
      offset: offset || 0,
    })

    // Handle error
    if (response.error) {
      return <TaskError message={response.error} />
    }

    // Get available tags for filter dropdown
    let availableTags: string[] = []
    try {
      const tagsResponse = await fetchTags()
      if (tagsResponse.tags) {
        availableTags = tagsResponse.tags.map((t) => t.name)
      }
    } catch {
      // Ignore tag fetch errors
    }

    if (!response.tasks || response.tasks.length === 0) {
      return <TaskEmpty />
    }

    return (
      <>
        <TaskList initialTasks={response.tasks} />

        {/* Tag Filter (show when tags are available) */}
        {availableTags.length > 0 && (
          <div className="mt-4">
            <TagFilter availableTags={availableTags} />
          </div>
        )}

        {/* Pagination */}
        {response.total && (
          <PaginationControls
            currentPage={(offset || 0) / 10 + 1}
            totalPages={Math.ceil((response.total || 0) / 10)}
          />
        )}
      </>
    )
  } catch (error) {
    console.error('Error loading tasks:', error)
    return <TaskError />
  }
}

function TaskListSkeleton() {
  return (
    <div className="space-y-4">
      <TaskSkeleton />
      <TaskSkeleton />
      <TaskSkeleton />
    </div>
  )
}
