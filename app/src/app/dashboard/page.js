"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getMe, getProgress, getCurrentPlan, getPlanSummary, logout, isAuthenticated } from "@/lib/api";
import WorkoutStreaks from "@/components/WorkoutStreaks";
import ProgressBar from "@/components/ProgressBar";

const MOTIVATIONAL_QUOTES = [
  "The only bad workout is the one that didn't happen.",
  "Strength does not come from what you can do. It comes from overcoming what you couldn't.",
  "Your body can stand almost anything. It's your mind that you have to convince.",
  "Success is what comes after you stop making excuses.",
  "Push yourself because no one else is going to do it for you.",
  "Don't limit your challenges. Challenge your limits.",
];

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [progress, setProgress] = useState(null);
  const [planSummary, setPlanSummary] = useState(null);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quote] = useState(() => MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)]);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    loadDashboard();
  }, [router]);

  const loadDashboard = async () => {
    try {
      const [userData, progressData, planData] = await Promise.allSettled([
        getMe(),
        getProgress(),
        getCurrentPlan(),
      ]);

      if (userData.status === "fulfilled") setUser(userData.value);
      if (progressData.status === "fulfilled") setProgress(progressData.value);
      if (planData.status === "fulfilled") setPlan(planData.value);
    } catch (err) {
      console.error("Dashboard load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const today = new Date().toISOString().split("T")[0];
  const todayWorkout = plan?.daily_workouts?.find((d) => d.date === today);

  if (loading) {
    return (
      <main className="flex-1 flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-400">Loading your dashboard...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-5xl mx-auto w-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 animate-fade-in-up">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">
            Welcome back, <span className="text-primary-400">{user?.full_name?.split(" ")[0] || "Athlete"}</span>
          </h1>
          <p className="text-sm text-slate-500 mt-1 italic">&quot;{quote}&quot;</p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/profile" className="btn-secondary text-sm py-2 px-4 hidden sm:block">
            Profile
          </Link>
          <button onClick={logout} className="text-xs text-slate-500 hover:text-slate-300 transition-colors">
            Logout
          </button>
        </div>
      </div>

      {/* Streaks Row */}
      <div className="mb-6 animate-fade-in-up delay-100">
        <WorkoutStreaks
          currentStreak={progress?.current_streak || 0}
          longestStreak={progress?.longest_streak || 0}
          workoutsThisWeek={progress?.workouts_this_week || 0}
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Workout Card */}
        <div className="lg:col-span-2 animate-fade-in-up delay-200">
          <div className="glass-card p-6 glass-card-hover">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Today&apos;s Workout</h2>
              <span className="text-xs text-slate-500">
                {new Date().toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric" })}
              </span>
            </div>

            {todayWorkout && todayWorkout.day_type !== "Rest" ? (
              <>
                <div className="flex items-center gap-3 mb-4">
                  <span className="px-3 py-1 rounded-full text-xs font-semibold gradient-primary text-white">
                    {todayWorkout.day_type}
                  </span>
                  <span className="text-sm text-slate-400">
                    {todayWorkout.routine?.length || 0} exercises
                  </span>
                </div>

                {/* Exercise Preview */}
                <div className="space-y-2 mb-4">
                  {(todayWorkout.routine || []).slice(0, 4).map((ex, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 rounded-lg bg-white/5">
                      <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center text-xs font-medium text-slate-400">
                        {i + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-white truncate">{ex.name}</p>
                        <p className="text-xs text-slate-500">{ex.sets} × {ex.reps} reps</p>
                      </div>
                      <span className="chip text-[10px]">{ex.target_muscle_primary}</span>
                    </div>
                  ))}
                  {(todayWorkout.routine || []).length > 4 && (
                    <p className="text-xs text-slate-500 text-center">
                      +{todayWorkout.routine.length - 4} more exercises
                    </p>
                  )}
                </div>

                <Link
                  href={`/workout/${today}`}
                  className="btn-primary w-full flex items-center justify-center gap-2 text-center"
                >
                  Start Workout 🚀
                </Link>
              </>
            ) : todayWorkout?.day_type === "Rest" ? (
              <div className="text-center py-8">
                <span className="text-5xl block mb-3">😴</span>
                <h3 className="text-lg font-semibold text-white mb-1">Rest Day</h3>
                <p className="text-sm text-slate-400">Recovery is essential for progress. Take it easy today!</p>
              </div>
            ) : (
              <div className="text-center py-8">
                <span className="text-5xl block mb-3">📋</span>
                <h3 className="text-lg font-semibold text-white mb-1">No Plan Yet</h3>
                <p className="text-sm text-slate-400 mb-4">Generate a workout plan to get started.</p>
                <Link href="/onboarding" className="btn-primary">
                  Set Up Profile
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar Stats */}
        <div className="space-y-6 animate-fade-in-up delay-300">
          {/* Completion Rate */}
          <div className="glass-card p-5">
            <h3 className="text-sm font-medium text-slate-400 mb-3">Completion Rate</h3>
            <div className="flex items-center gap-4">
              {/* Circular Progress */}
              <div className="relative w-16 h-16 shrink-0">
                <svg className="w-16 h-16" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="28" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="4" />
                  <circle
                    cx="32" cy="32" r="28"
                    fill="none"
                    stroke="url(#grad)"
                    strokeWidth="4"
                    strokeLinecap="round"
                    strokeDasharray={`${2 * Math.PI * 28}`}
                    strokeDashoffset={`${2 * Math.PI * 28 * (1 - (progress?.completion_rate || 0) / 100)}`}
                    className="progress-ring-circle"
                  />
                  <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#0d6efd" />
                      <stop offset="100%" stopColor="#8b5cf6" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-bold text-white">{Math.round(progress?.completion_rate || 0)}%</span>
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold text-white">{progress?.total_workouts_completed || 0}</p>
                <p className="text-xs text-slate-500">Workouts Done</p>
              </div>
            </div>
          </div>

          {/* Plan Overview */}
          {plan && (
            <div className="glass-card p-5">
              <h3 className="text-sm font-medium text-slate-400 mb-3">Current Plan</h3>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Period</span>
                  <span className="text-white">{plan.start_date} → {plan.end_date}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Workout Days</span>
                  <span className="text-white">
                    {plan.daily_workouts?.filter(d => d.day_type !== "Rest").length || 0}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Rest Days</span>
                  <span className="text-white">
                    {plan.daily_workouts?.filter(d => d.day_type === "Rest").length || 0}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="glass-card p-5">
            <h3 className="text-sm font-medium text-slate-400 mb-3">Quick Actions</h3>
            <div className="space-y-2">
              <Link
                href="/profile"
                className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/8 transition-colors"
              >
                <span className="text-lg">👤</span>
                <span className="text-sm text-slate-300">Edit Profile</span>
              </Link>
              <Link
                href={`/workout/${today}`}
                className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/8 transition-colors"
              >
                <span className="text-lg">💪</span>
                <span className="text-sm text-slate-300">View Today&apos;s Workout</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Upcoming Workouts Calendar */}
      {plan && (
        <div className="mt-6 animate-fade-in-up delay-400">
          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Upcoming Workouts</h2>
            <div className="grid grid-cols-7 gap-2">
              {(plan.daily_workouts || []).slice(0, 14).map((day) => {
                const isToday = day.date === today;
                const isRest = day.day_type === "Rest";
                const d = new Date(day.date + "T00:00:00");

                return (
                  <Link
                    key={day.date}
                    href={isRest ? "#" : `/workout/${day.date}`}
                    className={`p-2 rounded-xl text-center transition-all duration-200 ${
                      isToday
                        ? "bg-primary-600/20 border border-primary-500/40 shadow-lg"
                        : isRest
                        ? "bg-white/3 opacity-50"
                        : "bg-white/5 hover:bg-white/8 border border-white/5"
                    }`}
                  >
                    <p className="text-[10px] text-slate-500">
                      {d.toLocaleDateString("en-US", { weekday: "short" })}
                    </p>
                    <p className={`text-sm font-semibold mt-0.5 ${isToday ? "text-primary-400" : "text-white"}`}>
                      {d.getDate()}
                    </p>
                    <p className={`text-[9px] mt-0.5 truncate ${isRest ? "text-slate-600" : "text-slate-400"}`}>
                      {isRest ? "Rest" : day.day_type}
                    </p>
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
