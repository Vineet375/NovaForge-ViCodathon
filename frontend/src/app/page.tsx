import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { PageContainer, Section, SectionHeader, SectionTitle, SectionDescription } from "@/components/layout/layout-foundation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Play } from "lucide-react"
import { CandidateSelector } from "@/components/dashboard/candidate-selector"
import { CurriculumProgress } from "@/components/dashboard/curriculum-progress"
import { ActivityTimeline } from "@/components/dashboard/activity-timeline"
import { DashboardStats } from "@/components/dashboard/dashboard-stats"
import { AnalyticsChart } from "@/components/dashboard/analytics-chart"

export default function Home() {
  return (
    <DashboardLayout>
      <PageContainer className="py-6 sm:py-8 space-y-8">
        <Section className="py-0 md:py-0 lg:py-0">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <SectionHeader className="pb-0 md:pb-0">
              <SectionTitle className="text-3xl sm:text-4xl">Good morning, Alex</SectionTitle>
              <SectionDescription>
                You have an interview scheduled for tomorrow. Keep preparing!
              </SectionDescription>
            </SectionHeader>
            <div className="flex shrink-0 items-center gap-3">
              <Button size="lg" className="w-full sm:w-auto shadow-premium-sm">
                <Play className="mr-2 h-4 w-4" />
                Resume Interview
              </Button>
            </div>
          </div>
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <DashboardStats />
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <div className="grid gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-8">
              <CurriculumProgress />
              <ActivityTimeline />
            </div>
            
            <div className="space-y-8">
              <AnalyticsChart />
              <div>
                <h3 className="text-lg font-medium mb-4">Select Candidate</h3>
                <CandidateSelector />
              </div>
            </div>
          </div>
        </Section>
      </PageContainer>
    </DashboardLayout>
  )
}
