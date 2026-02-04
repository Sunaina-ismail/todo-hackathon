# Client-Side Contract: Sidebar State

**Feature**: 005-modern-dashboard-redesign
**Storage**: localStorage (client-side only)

## Overview

This contract defines the client-side state management for the responsive sidebar component. State is persisted in localStorage to maintain user preferences across sessions.

---

## Storage Keys

### Primary Key: `sidebar-collapsed`

**Type**: string (boolean serialized)
**Values**: `"true"` | `"false"`
**Default**: `"false"` (expanded)

**Purpose**: Stores whether the sidebar is collapsed or expanded

**Example**:
```typescript
localStorage.setItem('sidebar-collapsed', 'true')
const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true'
```

---

### Secondary Key: `sidebar-last-toggled`

**Type**: string (ISO timestamp)
**Values**: ISO 8601 timestamp
**Default**: undefined

**Purpose**: Tracks when the sidebar was last toggled (for analytics)

**Example**:
```typescript
localStorage.setItem('sidebar-last-toggled', new Date().toISOString())
const lastToggled = localStorage.getItem('sidebar-last-toggled')
```

---

## State Management Hook

### `useSidebar()`

**Location**: `hooks/use-sidebar.ts`

**Interface**:
```typescript
interface UseSidebarReturn {
  isCollapsed: boolean      // Current collapsed state
  toggle: () => void        // Toggle function
  expand: () => void        // Explicitly expand
  collapse: () => void      // Explicitly collapse
  isHydrated: boolean       // Whether state is hydrated from localStorage
}

function useSidebar(): UseSidebarReturn
```

**Implementation**:
```typescript
import { useState, useEffect } from 'react'

const STORAGE_KEY = 'sidebar-collapsed'
const TIMESTAMP_KEY = 'sidebar-last-toggled'

export function useSidebar(): UseSidebarReturn {
  // Initialize with default to prevent hydration mismatch
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [isHydrated, setIsHydrated] = useState(false)

  // Load from localStorage after mount (client-side only)
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored !== null) {
      setIsCollapsed(stored === 'true')
    }
    setIsHydrated(true)
  }, [])

  // Save to localStorage on change
  useEffect(() => {
    if (isHydrated) {
      localStorage.setItem(STORAGE_KEY, String(isCollapsed))
      localStorage.setItem(TIMESTAMP_KEY, new Date().toISOString())
    }
  }, [isCollapsed, isHydrated])

  const toggle = () => setIsCollapsed(prev => !prev)
  const expand = () => setIsCollapsed(false)
  const collapse = () => setIsCollapsed(true)

  return { isCollapsed, toggle, expand, collapse, isHydrated }
}
```

---

## Responsive Behavior

### Desktop (> 1024px)

- **Default State**: Expanded
- **User Control**: Manual toggle via button
- **Persistence**: State persists across sessions
- **Animation**: Smooth width transition (300ms)

### Tablet (768px - 1024px)

- **Default State**: Collapsed
- **User Control**: Manual toggle via button
- **Persistence**: State persists across sessions
- **Animation**: Smooth width transition (300ms)

### Mobile (< 768px)

- **Default State**: Collapsed (icon-only)
- **User Control**: Tap to expand as overlay
- **Auto-Collapse**: Collapses after navigation
- **Animation**: Slide-in from left (300ms)

---

## State Transitions

```
Initial Load → Check localStorage → Apply State → Render
     ↓
User Toggle → Update State → Save to localStorage → Animate
     ↓
Navigation (Mobile) → Auto-Collapse → Save to localStorage → Animate
```

---

## SSR Compatibility

**Challenge**: localStorage is not available during server-side rendering

**Solution**:
1. Initialize with default value (expanded) on server
2. Load from localStorage after hydration (client-side)
3. Use `isHydrated` flag to prevent flash of incorrect state

**Example**:
```typescript
export function Sidebar() {
  const { isCollapsed, toggle, isHydrated } = useSidebar()

  // Prevent flash during hydration
  if (!isHydrated) {
    return <SidebarSkeleton />
  }

  return (
    <motion.aside
      animate={isCollapsed ? 'collapsed' : 'expanded'}
      variants={sidebarVariants}
    >
      {/* Sidebar content */}
    </motion.aside>
  )
}
```

---

## Error Handling

### localStorage Not Available

**Scenarios**:
- Private browsing mode
- Browser settings disable storage
- Storage quota exceeded

**Fallback**:
```typescript
function useSidebar(): UseSidebarReturn {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored !== null) {
        setIsCollapsed(stored === 'true')
      }
    } catch (error) {
      console.warn('localStorage not available, using session state')
    }
    setIsHydrated(true)
  }, [])

  useEffect(() => {
    if (isHydrated) {
      try {
        localStorage.setItem(STORAGE_KEY, String(isCollapsed))
      } catch (error) {
        // Silently fail, state still works in memory
      }
    }
  }, [isCollapsed, isHydrated])

  // ... rest of implementation
}
```

---

## Testing

### Test Cases

1. **Initial Load**: Sidebar expanded by default
2. **Toggle**: State updates and persists
3. **Refresh**: State restored from localStorage
4. **Private Browsing**: Graceful fallback to session state
5. **Mobile Navigation**: Auto-collapse after route change

### Example Test

```typescript
describe('useSidebar', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('initializes with expanded state', () => {
    const { result } = renderHook(() => useSidebar())
    expect(result.current.isCollapsed).toBe(false)
  })

  it('persists state to localStorage', () => {
    const { result } = renderHook(() => useSidebar())

    act(() => {
      result.current.toggle()
    })

    expect(localStorage.getItem('sidebar-collapsed')).toBe('true')
  })

  it('restores state from localStorage', () => {
    localStorage.setItem('sidebar-collapsed', 'true')

    const { result } = renderHook(() => useSidebar())

    waitFor(() => {
      expect(result.current.isCollapsed).toBe(true)
    })
  })
})
```

---

## Analytics Integration

**Optional**: Track sidebar usage for UX insights

```typescript
useEffect(() => {
  if (isHydrated) {
    // Track toggle event
    analytics.track('sidebar_toggled', {
      state: isCollapsed ? 'collapsed' : 'expanded',
      timestamp: new Date().toISOString()
    })
  }
}, [isCollapsed, isHydrated])
```

---

**Contract Status**: ✅ Complete
**Breaking Changes**: None (new feature)
**Backward Compatibility**: N/A
