"use client"
import * as React from "react"
import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Monitor, Server, Sparkles, Code2, AlertCircle, CheckCircle2 } from "lucide-react"
import { fetchApi } from "@/lib/api"
import { useTheme } from "next-themes"

export default function SettingsPage() {
  const { theme, setTheme } = useTheme()
  const [backendStatus, setBackendStatus] = React.useState<"checking" | "connected" | "error">("checking")
  
  React.useEffect(() => {
    fetchApi<unknown>("/health")
      .then(() => setBackendStatus("connected"))
      .catch(() => setBackendStatus("error"))
  }, [])

  return (
    <DashboardLayout>
      <div className="p-8 max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Settings</h1>
          <p className="text-muted-foreground">
            Manage application preferences and monitor system health.
          </p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2">
          {/* Theme Settings */}
          <Card className="shadow-premium">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Monitor className="h-5 w-5 text-primary" />
                Appearance
              </CardTitle>
              <CardDescription>Customize the application theme.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-4">
                <button 
                  onClick={() => setTheme("light")}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${theme === "light" ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"}`}
                >
                  <Monitor className="h-6 w-6 mx-auto mb-2 text-foreground" />
                  <div className="text-sm font-medium">Light Mode</div>
                </button>
                <button 
                  onClick={() => setTheme("dark")}
                  className={`flex-1 p-4 rounded-xl border-2 transition-all ${theme === "dark" ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"}`}
                >
                  <Monitor className="h-6 w-6 mx-auto mb-2 text-muted-foreground" />
                  <div className="text-sm font-medium">Dark Mode</div>
                </button>
              </div>
            </CardContent>
          </Card>

          {/* System Health */}
          <Card className="shadow-premium">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="h-5 w-5 text-primary" />
                System Health
              </CardTitle>
              <CardDescription>Real-time status of NovaForge services.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Server className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Backend API</p>
                    <p className="text-xs text-muted-foreground">FastAPI Server</p>
                  </div>
                </div>
                {backendStatus === "checking" && <Badge variant="secondary">Checking...</Badge>}
                {backendStatus === "connected" && <Badge className="bg-green-500/10 text-green-500 hover:bg-green-500/20 border-green-500/20"><CheckCircle2 className="w-3 h-3 mr-1"/> Connected</Badge>}
                {backendStatus === "error" && <Badge variant="destructive"><AlertCircle className="w-3 h-3 mr-1"/> Unavailable</Badge>}
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Sparkles className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Gemini AI Service</p>
                    <p className="text-xs text-muted-foreground">Model Context Protocol</p>
                  </div>
                </div>
                {backendStatus === "connected" 
                  ? <Badge className="bg-green-500/10 text-green-500 hover:bg-green-500/20 border-green-500/20"><CheckCircle2 className="w-3 h-3 mr-1"/> Connected</Badge>
                  : <Badge variant="secondary">Unknown</Badge>
                }
              </div>
            </CardContent>
          </Card>

          {/* Application Info */}
          <Card className="shadow-premium md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code2 className="h-5 w-5 text-primary" />
                About NovaForge
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-xl border border-border/50">
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Version</p>
                  <p className="text-sm font-semibold">1.0.0-rc.1</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Environment</p>
                  <p className="text-sm font-semibold capitalize">{process.env.NODE_ENV || 'development'}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Frontend</p>
                  <p className="text-sm font-semibold">Next.js 15</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Backend</p>
                  <p className="text-sm font-semibold">FastAPI</p>
                </div>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                NovaForge is a next-generation AI interviewing platform built for ViCodathon 2026. 
                It leverages advanced Retrieval-Augmented Generation (RAG) and Google&apos;s Gemini models 
                to conduct intelligent, adaptive technical interviews.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
