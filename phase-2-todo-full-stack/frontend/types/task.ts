/**
 * Task entity from the FastAPI backend
 */
export interface Task {
  /** UUID from backend database */
  id: string;
  /** Better Auth UUID of task owner */
  user_id: string;
  /** Task title, max 200 characters */
  title: string;
  /** Task description, max 1000 characters, optional */
  description?: string;
  /** Completion status */
  completed: boolean;
  /** Priority level */
  priority: 'High' | 'Medium' | 'Low';
  /** Due date in ISO format, optional */
  due_date?: string;
  /** Array of tag names */
  tags: string[];
  /** Creation timestamp ISO string */
  created_at: string;
  /** Last update timestamp ISO string */
  updated_at: string;
}

/**
 * Tag from backend
 */
export interface Tag {
  id: string;
  name: string;
}

/**
 * Tag with usage count from backend
 */
export interface TagWithUsage {
  /** Tag name */
  name: string;
  /** Number of tasks using this tag */
  usage_count: number;
}

/**
 * Task creation payload
 */
export interface TaskCreate {
  /** Task title, required, max 200 characters */
  title: string;
  /** Optional description, max 1000 characters */
  description?: string;
  /** Priority level, default: Medium */
  priority: 'High' | 'Medium' | 'Low';
  /** Optional due date in YYYY-MM-DD format */
  due_date?: string;
  /** Optional array of tag names */
  tags?: string[];
}

/**
 * Task update payload (partial update) */
export interface TaskUpdate {
  /** Optional title update */
  title?: string;
  /** Optional description update */
  description?: string;
  /** Optional completion status update */
  completed?: boolean;
  /** Optional priority update */
  priority?: 'High' | 'Medium' | 'Low';
  /** Optional due date update */
  due_date?: string;
  /** Optional tags update (replaces all) */
  tags?: string[];
}
