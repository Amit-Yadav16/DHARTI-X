import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DHARTI-X — Multi-Agent AI Agriculture Platform",
  description: "Intelligence Rooted in Nature. AI Agriculture platform for Palghar district, Maharashtra.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#050f09] text-gray-100 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}

