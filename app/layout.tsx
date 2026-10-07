import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Drone AI Control Center",
  description: "Mission planning dashboard powered by Python AI services.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
