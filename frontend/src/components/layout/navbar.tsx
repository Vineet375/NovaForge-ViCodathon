"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

const NavbarContainer = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <header
    ref={ref}
    className={cn(
      "sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-border bg-background/80 px-4 backdrop-blur-sm sm:px-6",
      className
    )}
    {...props}
  />
))
NavbarContainer.displayName = "NavbarContainer"

const NavbarBrand = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center space-x-2 font-bold tracking-tight", className)}
    {...props}
  />
))
NavbarBrand.displayName = "NavbarBrand"

const NavbarNav = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <nav
    ref={ref}
    className={cn("hidden md:flex items-center space-x-4 lg:space-x-6", className)}
    {...props}
  />
))
NavbarNav.displayName = "NavbarNav"

export {
  NavbarContainer,
  NavbarBrand,
  NavbarNav
}
