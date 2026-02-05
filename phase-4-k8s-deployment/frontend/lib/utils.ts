import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow, parseISO, isValid } from 'date-fns';

/**
 * Merge Tailwind CSS classes with proper precedence
 * Used by Shadcn UI components
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format ISO date string to readable format
 * @param isoString - ISO date string from backend
 * @param formatString - date-fns format string (default: 'MMM d, yyyy')
 * @returns Formatted date string or empty string if invalid
 */
export function formatDate(isoString?: string, formatString = 'MMM d, yyyy'): string {
  if (!isoString) return '';

  try {
    const date = parseISO(isoString);
    if (!isValid(date)) return '';
    return format(date, formatString);
  } catch {
    return '';
  }
}

/**
 * Format ISO date string to relative time (e.g., "2 hours ago")
 * @param isoString - ISO date string from backend
 * @returns Relative time string or empty string if invalid
 */
export function formatRelativeTime(isoString?: string): string {
  if (!isoString) return '';

  try {
    const date = parseISO(isoString);
    if (!isValid(date)) return '';
    return formatDistanceToNow(date, { addSuffix: true });
  } catch {
    return '';
  }
}

/**
 * Format date for input[type="date"] (YYYY-MM-DD)
 * @param isoString - ISO date string from backend
 * @returns Date string in YYYY-MM-DD format or empty string if invalid
 */
export function formatDateForInput(isoString?: string): string {
  if (!isoString) return '';

  try {
    const date = parseISO(isoString);
    if (!isValid(date)) return '';
    return format(date, 'yyyy-MM-dd');
  } catch {
    return '';
  }
}

/**
 * Check if a date is in the past
 * @param isoString - ISO date string from backend
 * @returns true if date is in the past, false otherwise
 */
export function isPastDate(isoString?: string): boolean {
  if (!isoString) return false;

  try {
    const date = parseISO(isoString);
    if (!isValid(date)) return false;
    return date < new Date();
  } catch {
    return false;
  }
}
