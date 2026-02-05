'use client'

import { useState, useEffect } from 'react'

/**
 * Custom hook for responsive breakpoint detection
 * Returns true if the media query matches
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)

    const mediaQuery = window.matchMedia(query)
    setMatches(mediaQuery.matches)

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches)
    }

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handler)
      return () => mediaQuery.removeEventListener('change', handler)
    }
    // Legacy browsers
    else {
      mediaQuery.addListener(handler)
      return () => mediaQuery.removeListener(handler)
    }
  }, [query])

  // Return false during SSR to prevent hydration mismatch
  if (!mounted) {
    return false
  }

  return matches
}

/**
 * Predefined breakpoint hooks for common screen sizes
 */
export function useIsMobile(): boolean {
  return useMediaQuery('(max-width: 767px)')
}

export function useIsTablet(): boolean {
  return useMediaQuery('(min-width: 768px) and (max-width: 1023px)')
}

export function useIsDesktop(): boolean {
  return useMediaQuery('(min-width: 1024px)')
}

export function useIsLargeDesktop(): boolean {
  return useMediaQuery('(min-width: 1920px)')
}

/**
 * Hook to get current breakpoint name
 */
export function useBreakpoint(): 'mobile' | 'tablet' | 'desktop' | 'largeDesktop' {
  const isMobile = useIsMobile()
  const isTablet = useIsTablet()
  const isLargeDesktop = useIsLargeDesktop()

  if (isMobile) return 'mobile'
  if (isTablet) return 'tablet'
  if (isLargeDesktop) return 'largeDesktop'
  return 'desktop'
}
