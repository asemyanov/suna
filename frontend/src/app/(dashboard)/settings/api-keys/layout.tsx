import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'API Keys | MEVO',
  description: 'Manage your API keys for programmatic access to MEVO',
  openGraph: {
    title: 'API Keys | MEVO',
    description: 'Manage your API keys for programmatic access to MEVO',
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
