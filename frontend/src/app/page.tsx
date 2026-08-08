import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { PageContainer, Section, SectionHeader, SectionTitle, SectionDescription } from "@/components/layout/layout-foundation"
import { Button } from "@/components/ui/button"
import { Play } from "lucide-react"

export default function Home() {
  return (
    <DashboardLayout>
      <PageContainer className="py-6 sm:py-8">
        <Section className="py-0 md:py-0 lg:py-0 mb-8 sm:mb-12">
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
      </PageContainer>
    </DashboardLayout>
  )
}
