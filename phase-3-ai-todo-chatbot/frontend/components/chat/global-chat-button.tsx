/**
 * Global Chat Button Component
 *
 * Professional floating chat button with purple theme matching the website design.
 * Opens a chat modal overlay with ChatKitWidget when clicked.
 *
 * Features:
 * - Fixed position floating button at bottom-right corner with gradient purple styling
 * - Opens modal overlay with ChatKit widget
 * - PERSISTS chat state when closed (widget stays mounted, just hidden)
 * - Checks auth before showing (only for authenticated users)
 * - Hidden on public routes (landing, sign-in, sign-up)
 * - Smooth animations for open/close transitions
 * - Body scroll lock when chat is open (prevents background scrolling)
 * - Professional design matching purple theme (#A855F7)
 * - Accessible with proper ARIA attributes
 * - Glassmorphism effects and modern UI patterns
 */

"use client";

import { useState, useEffect } from "react";
import { MessageCircle, X, Sparkles } from "lucide-react";
import { ChatKitWidget } from "./chatkit-widget";
import { cn } from "@/lib/utils";
import { authClient } from "@/lib/auth-client";
import { usePathname } from "next/navigation";

export function GlobalChatButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasBeenOpened, setHasBeenOpened] = useState(false);
  const pathname = usePathname();

  // Routes where the chat button should NOT appear
  const hiddenRoutes = ["/", "/sign-in", "/sign-up", "/chat"];
  const shouldShow = !hiddenRoutes.includes(pathname);

  useEffect(() => {
    async function checkAuth() {
      try {
        const session = await authClient.getSession();
        if (session?.data?.user) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error("Failed to check auth:", error);
        setIsAuthenticated(false);
      }
    }

    if (shouldShow) {
      checkAuth();
    }
  }, [shouldShow]);

  // Lock body scroll when chat is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      document.body.style.position = "fixed";
      document.body.style.width = "100%";
      document.body.style.height = "100%";
    } else {
      document.body.style.overflow = "";
      document.body.style.position = "";
      document.body.style.width = "";
      document.body.style.height = "";
    }

    // Cleanup on unmount
    return () => {
      document.body.style.overflow = "";
      document.body.style.position = "";
      document.body.style.width = "";
      document.body.style.height = "";
    };
  }, [isOpen]);

  // Track if chat has been opened at least once (to mount widget)
  const handleOpen = () => {
    setIsOpen(true);
    setHasBeenOpened(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  // Don't render if on hidden routes or not authenticated
  if (!shouldShow || !isAuthenticated) {
    return null;
  }

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={handleOpen}
        className={cn(
          "fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50",
          "w-14 h-14 sm:w-16 sm:h-16 rounded-full",
          // Neon Lime gradient background
          "bg-gradient-to-br from-neon-lime via-neon-lime/90 to-neon-lime/80",
          "hover:from-neon-lime/90 hover:via-neon-lime/80 hover:to-neon-lime/70",
          // Glow effect with Neon Lime
          "shadow-[0_8px_32px_rgba(190,242,100,0.4)]",
          "hover:shadow-[0_12px_40px_rgba(190,242,100,0.6)]",
          "text-forest-black",
          "flex items-center justify-center",
          "transition-all duration-300",
          "hover:scale-105 active:scale-95",
          "focus:outline-none focus:ring-2 focus:ring-neon-lime focus:ring-offset-2 focus:ring-offset-forest-black",
          "border-2 border-neon-lime/30",
          isOpen && "scale-0 opacity-0"
        )}
        aria-label="Open AI chat assistant"
      >
        {/* Icon with glow */}
        <div className="relative">
          <div className="absolute inset-0 bg-forest-black/20 blur-xl rounded-full" />
          <MessageCircle className="relative w-6 h-6 sm:w-7 sm:h-7" />
        </div>
      </button>

      {/* Backdrop - only visible when open */}
      <div
        className={cn(
          "fixed inset-0 z-[9998] bg-black/60 backdrop-blur-md transition-opacity duration-300",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={handleClose}
        aria-hidden="true"
      />

      {/* Chat Modal - stays mounted after first open, just hidden */}
      <div
        className={cn(
          "fixed z-[9999]",
          // Mobile: full height with padding
          "inset-2 sm:inset-4",
          // Desktop: fixed size at bottom-right
          "lg:inset-auto lg:bottom-6 lg:right-6",
          "lg:w-[420px] lg:max-w-[calc(100vw-4rem)]",
          "lg:h-[580px] lg:max-h-[calc(100vh-4rem)]",
          "flex flex-col",
          "transition-all duration-300",
          isOpen ? "opacity-100 scale-100" : "opacity-0 scale-95 pointer-events-none"
        )}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="chat-title"
      >
        {/* Only render content after first open to avoid initial load */}
        {hasBeenOpened && (
          <div className="bg-forest-black/95 backdrop-blur-xl border border-neon-lime/30 rounded-2xl shadow-2xl shadow-neon-lime/20 flex-1 flex flex-col overflow-hidden">
            {/* Header with gradient */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-neon-lime/20 bg-gradient-to-r from-neon-lime/10 via-neon-lime/5 to-neon-lime/10">
              <div className="flex items-center gap-2 sm:gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-neon-lime/30 blur-xl rounded-full animate-pulse" />
                  <div className="relative w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-neon-lime to-neon-lime/80 flex items-center justify-center border border-neon-lime/30 shadow-lg shadow-neon-lime/30">
                    <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-forest-black" />
                  </div>
                </div>
                <div>
                  <h3 id="chat-title" className="text-sm sm:text-base lg:text-lg font-bold text-white">
                    AI Assistant
                  </h3>
                  <p className="text-[10px] sm:text-xs text-neon-lime/80">
                    Powered by Todo AI
                  </p>
                </div>
              </div>
              <button
                onClick={handleClose}
                className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-neon-lime/30 transition-all duration-200 group"
                aria-label="Close chat"
              >
                <X className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
              </button>
            </div>

            {/* Chat Widget - stays mounted, preserves conversation */}
            <div className="flex-1 overflow-hidden bg-forest-black">
              <ChatKitWidget className="h-full w-full" />
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default GlobalChatButton;
