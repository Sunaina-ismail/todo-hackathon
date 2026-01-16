import { Task } from './task';

/**
 * Task filter parameters for API queries
 */
export interface TaskFilters {
  /** Filter by completion status */
  completed?: boolean;
  /** Search text for title/description matching */
  search?: string;
  /** Filter by priority level */
  priority?: 'High' | 'Medium' | 'Low' | 'all';
  /** Filter by tag names (AND/OR logic per API) */
  tags?: string[];
  /** Sort field */
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'due_date' | 'priority';
  /** Sort direction */
  sort_direction?: 'asc' | 'desc';
  /** Number of results per page, default: 50 */
  limit?: number;
  /** Pagination offset, default: 0 */
  offset?: number;
}

/**
 * Pagination response metadata
 */
export interface PaginationMeta {
  /** Total number of tasks matching filters */
  total: number;
  /** Current offset */
  offset: number;
  /** Current limit */
  limit: number;
  /** Whether more results exist */
  has_more: boolean;
}

/**
 * Paginated task response
 */
export interface TaskListResponse {
  /** Array of tasks */
  tasks: Task[];
  /** Pagination metadata */
  meta: PaginationMeta;
}
