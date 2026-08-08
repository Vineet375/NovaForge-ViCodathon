import { fetchApi } from "./api"

export interface StatCard {
  title: string
  value: string
  subtitle: string
}

export interface ActivityItem {
  id: string
  title: string
  description: string
  time: string
  type: string
}

export interface DashboardData {
  stats: StatCard[]
  activities: ActivityItem[]
}

export const DashboardAPI = {
  getData: () => fetchApi<DashboardData>("/dashboard"),
}
