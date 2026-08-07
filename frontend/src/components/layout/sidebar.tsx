"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

const SidebarContainer = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "fixed left-0 top-0 z-40 h-screen w-64 -translate-x-full border-r border-border bg-background transition-transform sm:translate-x-0",
      className
    )}
    {...props}
  />
))
SidebarContainer.displayName = "SidebarContainer"

const SidebarHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex h-16 items-center border-b border-border px-6", className)}
    {...props}
  />
))
SidebarHeader.displayName = "SidebarHeader"

const SidebarContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1 overflow-y-auto px-4 py-6", className)}
    {...props}
  />
))
SidebarContent.displayName = "SidebarContent"

const SidebarItem = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { active?: boolean }
>(({ className, active, ...props }, ref) => (
  <button
    ref={ref}
    className={cn(
      "flex w-full items-center justify-start rounded-md px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      active 
        ? "bg-primary text-primary-foreground shadow-premium-sm" 
        : "text-muted-foreground hover:bg-muted hover:text-foreground",
      className
    )}
    {...props}
  />
))
SidebarItem.displayName = "SidebarItem"

export {
  SidebarContainer,
  SidebarHeader,
  SidebarContent,
  SidebarItem
}
