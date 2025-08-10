import { agentPlaygroundFlagFrontend } from '@/flags';
import { isFlagEnabled } from '@/lib/feature-flags';
import { Metadata } from 'next';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Agent Conversation | ProblemX.AI',
  description: 'Interactive agent conversation powered by ProblemX.AI',
  openGraph: {
    title: 'Agent Conversation | ProblemX.AI',
    description: 'Interactive agent conversation powered by ProblemX.AI',
    type: 'website',
  },
};

export default async function AgentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
