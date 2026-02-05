// Framer Motion animation variants for Modern Dashboard UI Redesign

import { Variants } from 'framer-motion'

// Sidebar collapse/expand animations
export const sidebarVariants: Variants = {
  expanded: {
    width: '240px',
    transition: { duration: 0.3, ease: 'easeInOut' }
  },
  collapsed: {
    width: '64px',
    transition: { duration: 0.3, ease: 'easeInOut' }
  }
}

// Page transition animations
export const pageVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.2, ease: 'easeIn' }
  }
}

// Stagger list animations
export const staggerVariants = {
  container: {
    initial: {},
    animate: {
      transition: {
        staggerChildren: 0.05
      }
    }
  } as Variants,
  item: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 }
  } as Variants
}

// Fade in animation
export const fadeInVariants: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.2 } }
}

// Card hover animation
export const cardHoverVariants: Variants = {
  initial: { scale: 1 },
  hover: {
    scale: 1.02,
    transition: { duration: 0.2, ease: 'easeOut' }
  }
}

// Modal/Dialog animations
export const modalVariants: Variants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.2, ease: 'easeOut' }
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: { duration: 0.15, ease: 'easeIn' }
  }
}

// Slide in from right (for chat widget)
export const slideInRightVariants: Variants = {
  initial: { opacity: 0, x: 400 },
  animate: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.3, ease: 'easeInOut' }
  },
  exit: {
    opacity: 0,
    x: 400,
    transition: { duration: 0.3, ease: 'easeInOut' }
  }
}

// Slide in from left (for mobile sidebar)
export const slideInLeftVariants: Variants = {
  initial: { opacity: 0, x: -300 },
  animate: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.3, ease: 'easeInOut' }
  },
  exit: {
    opacity: 0,
    x: -300,
    transition: { duration: 0.3, ease: 'easeInOut' }
  }
}

// Skeleton pulse animation
export const skeletonPulseVariants: Variants = {
  initial: { opacity: 0.6 },
  animate: {
    opacity: [0.6, 1, 0.6],
    transition: {
      duration: 1.5,
      repeat: Infinity,
      ease: 'easeInOut'
    }
  }
}
