"use client"
import * as React from "react"
import { SidebarContainer, SidebarHeader, SidebarContent, SidebarItem } from "./sidebar"
import { NavbarContainer, NavbarBrand, NavbarNav } from "./navbar"
import { ThemeToggle } from "@/components/theme-toggle"
import { LayoutDashboard, Users, BookOpen, Settings, Briefcase } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname()
  
  return (
    <div className="flex min-h-screen w-full flex-col bg-background">
      <NavbarContainer>
        <NavbarBrand>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Briefcase className="h-5 w-5" />
            </div>
            <span className="text-xl">NovaForge</span>
          </div>
        </NavbarBrand>
        <NavbarNav>
          <ThemeToggle />
        </NavbarNav>
      </NavbarContainer>

      <div className="flex flex-1">
        <SidebarContainer className="hidden sm:block sm:translate-x-0 relative h-auto z-0 border-r-0 border-r-border/0 pr-0">
          <div className="sticky top-16 h-[calc(100vh-4rem)] w-64 border-r border-border bg-background">
            <SidebarContent>
              <Link href="/" passHref legacyBehavior>
                <SidebarItem active={pathname === "/"}>
                  <LayoutDashboard className="mr-2 h-4 w-4" />
                  Dashboard
                </SidebarItem>
              </Link>
              <Link href="/candidates" passHref legacyBehavior>
                <SidebarItem active={pathname?.startsWith("/candidates")}>
                  <Users className="mr-2 h-4 w-4" />
                  Candidates
                </SidebarItem>
              </Link>
              <Link href="/curriculum" passHref legacyBehavior>
                <SidebarItem active={pathname?.startsWith("/curriculum")}>
                  <BookOpen className="mr-2 h-4 w-4" />
                  Curriculum
                </SidebarItem>
              </Link>
              <Link href="/settings" passHref legacyBehavior>
                <SidebarItem active={pathname?.startsWith("/settings")}>
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </SidebarItem>
              </Link>
            </SidebarContent>
          </div>
        </SidebarContainer>

        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  )
}
