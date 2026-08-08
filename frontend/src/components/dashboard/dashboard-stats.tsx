"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Target, TrendingUp, Zap, Clock } from "lucide-react"
import { useDashboard } from "@/hooks/useDashboard"

export function DashboardStats() {
  const { data, loading, error } = useDashboard()

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <div className="h-4 w-24 bg-muted rounded"></div>
              <div className="h-4 w-4 bg-muted rounded-full"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 w-16 bg-muted rounded mb-2"></div>
              <div className="h-3 w-32 bg-muted rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="p-4 border border-red-500/20 bg-red-500/10 rounded-lg text-red-500 text-sm text-center">
        Failed to load dashboard statistics.
      </div>
    )
  }

  const icons = [Target, TrendingUp, Zap, Clock]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {data.stats.map((stat, index) => {
        const Icon = icons[index % icons.length]
        return (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">
                {stat.subtitle}
              </p>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
