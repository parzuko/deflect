import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "🔎 Reflection Remover",
  description: "Fast Single Image Reflection Suppression via Convex Optimization",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
      <footer className="flex flex-col  max-w-7xl bg-[#F1F5F9]">
        <small className="text-sm font-medium leading-none py-4 px-10">
          Built by{" "}
          <a href="https://x.com/parzuko" className="text-blue-700">
            Jivansh
          </a>{" "}
          ✌️
        </small>
      </footer>
    </html>
  );
}
