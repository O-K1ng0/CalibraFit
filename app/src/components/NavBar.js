"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Apple, TrendingUp, User } from "lucide-react";

export default function NavBar() {
  const pathname = usePathname();

  // Hide the NavBar on the login and onboarding screens
  if (pathname === "/" || pathname.startsWith("/onboarding")) {
    return null;
  }

  const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: Home },
    { name: "Nutrition", href: "/nutrition", icon: Apple },
    { name: "Progress", href: "/progress", icon: TrendingUp },
    { name: "Profile", href: "/profile", icon: User },
  ];

  return (
    <>
      {/* 
        Desktop Top Navigation 
        Hidden on mobile, sticky at top on desktop
      */}
      <nav className="hidden md:flex sticky top-0 z-50 w-full bg-surface-900/80 backdrop-blur-xl border-b border-white/10 py-4 px-6 md:px-12 items-center justify-between transition-all">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-primary-600 flex items-center justify-center text-white font-bold text-xl">
            C
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-accent-400">
            CalibraFit
          </span>
        </div>
        
        <div className="flex items-center gap-8">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-2 text-sm font-medium transition-all hover:scale-105 ${
                  isActive ? "text-primary-400" : "text-slate-400 hover:text-white"
                }`}
              >
                <Icon size={18} className={isActive ? "drop-shadow-[0_0_8px_rgba(82,180,255,0.5)]" : ""} />
                {item.name}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* 
        Mobile Bottom Tab Bar 
        Hidden on desktop, fixed at bottom on mobile
      */}
      <nav className="md:hidden fixed bottom-0 inset-x-0 z-50 bg-surface-900/90 backdrop-blur-2xl border-t border-white/10 pb-[env(safe-area-inset-bottom)] pt-2 px-2">
        <div className="flex items-center justify-around">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                href={item.href}
                className="flex flex-col items-center justify-center w-full py-2 gap-1"
              >
                <div
                  className={`p-1.5 rounded-xl transition-all duration-300 ${
                    isActive ? "bg-primary-600/20 text-primary-400" : "text-slate-500"
                  }`}
                >
                  <Icon size={24} className={isActive ? "drop-shadow-[0_0_10px_rgba(82,180,255,0.6)]" : ""} />
                </div>
                <span
                  className={`text-[10px] font-medium transition-all ${
                    isActive ? "text-primary-400" : "text-slate-500"
                  }`}
                >
                  {item.name}
                </span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
