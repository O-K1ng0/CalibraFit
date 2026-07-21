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

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col gradient-mesh">{children}</body>
    </html>
  );
}
