import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "CalibraFit — Virtual Personal Trainer",
  description:
    "AI-powered fitness companion that creates personalized 30-day workout plans based on your medical history, fitness level, and goals.",
  keywords: "fitness, workout, personal trainer, exercise, health, medical safety",
};

import NavBar from "@/components/NavBar";

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col gradient-mesh">
        <NavBar />
        {/* pb-24 adds padding at the bottom on mobile to ensure content isn't hidden behind the fixed bottom bar */}
        <div className="flex-1 flex flex-col pb-24 md:pb-0">
          {children}
        </div>
      </body>
    </html>
  );
}
