import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'API Keys | ProblemX.AI',
  description: 'Manage your API keys for programmatic access to ProblemX.AI',
  openGraph: {
    title: 'API Keys | ProblemX.AI',
    description: 'Manage your API keys for programmatic access to ProblemX.AI',
    type: 'website',
  },
};

export default async function APIKeysLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
