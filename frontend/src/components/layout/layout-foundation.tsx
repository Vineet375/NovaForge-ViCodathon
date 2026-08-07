import * as React from "react"
import { cn } from "@/lib/utils"

const PageContainer = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8", className)}
    {...props}
  />
))
PageContainer.displayName = "PageContainer"

const Section = React.forwardRef<
  HTMLElement,
  React.HTMLAttributes<HTMLElement>
>(({ className, ...props }, ref) => (
  <section
    ref={ref}
    className={cn("py-8 md:py-12 lg:py-16", className)}
    {...props}
  />
))
Section.displayName = "Section"

const SectionHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-2 pb-6 md:pb-8", className)}
    {...props}
  />
))
SectionHeader.displayName = "SectionHeader"

const SectionTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h2
    ref={ref}
    className={cn("text-2xl font-semibold tracking-tight sm:text-3xl", className)}
    {...props}
  />
))
SectionTitle.displayName = "SectionTitle"

const SectionDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-muted-foreground max-w-2xl text-base sm:text-lg", className)}
    {...props}
  />
))
SectionDescription.displayName = "SectionDescription"

export {
  PageContainer,
  Section,
  SectionHeader,
  SectionTitle,
  SectionDescription
}
