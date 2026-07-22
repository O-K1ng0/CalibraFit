"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getProgress, getFeedbacks, isAuthenticated } from "@/lib/api";
import WorkoutStreaks from "@/components/WorkoutStreaks";

export default function ProgressPage() {
  const router = useRouter();
  const [progress, setProgress] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    loadData();
  }, [router]);

  const loadData = async () => {
    try {
      const [progressData, feedbackRes] = await Promise.allSettled([
        getProgress(),
        getFeedbacks(),
      ]);

      if (progressData.status === "fulfilled") setProgress(progressData.value);
      if (feedbackRes.status === "fulfilled") setFeedbacks(feedbackRes.value);
    } catch (err) {
      console.error("Progress page load error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="flex-1 flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-400">Loading progress data...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-5xl mx-auto w-full">
      <div className="mb-8 animate-fade-in-up">
        <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">My Progress</h1>
        <p className="text-sm text-slate-400">
          Track your consistency and review your weekly check-ins.
        </p>
      </div>

      {/* Streaks Row */}
      <div className="mb-8 animate-fade-in-up delay-100">
        <WorkoutStreaks
          currentStreak={progress?.current_streak || 0}
          longestStreak={progress?.longest_streak || 0}
          workoutsThisWeek={progress?.workouts_this_week || 0}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in-up delay-200 mb-8">
        {/* Completion Rate */}
        <div className="glass-card p-6">
          <h3 className="text-sm font-medium text-slate-400 mb-4">Plan Completion</h3>
          <div className="flex items-center gap-6">
            {/* Circular Progress */}
            <div className="relative w-20 h-20 shrink-0">
              <svg className="w-20 h-20" viewBox="0 0 64 64">
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
              <p className="text-3xl font-bold text-white mb-1">{progress?.total_workouts_completed || 0}</p>
              <p className="text-xs text-slate-500">Total Workouts Completed</p>
            </div>
          </div>
        </div>

        {/* Feedback Summary Card */}
        <div className="glass-card p-6 lg:col-span-2">
          <h3 className="text-sm font-medium text-slate-400 mb-4">Check-In Insights</h3>
          <p className="text-sm text-slate-300">
            You&apos;ve completed <span className="font-bold text-primary-400">{feedbacks.length}</span> weekly check-ins.
            Our adaptive algorithm uses this data to calibrate the difficulty of your future blocks and avoid aggravating any reported pain areas.
          </p>
        </div>
      </div>

      {/* Previous Feedbacks History */}
      {feedbacks.length > 0 ? (
        <div className="animate-fade-in-up delay-300">
          <h2 className="text-lg font-semibold text-white mb-4">📊 Weekly Feedback History</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {feedbacks.map((fb) => (
              <div key={fb.feedback_id} className="p-4 rounded-xl bg-white/5 border border-white/10 glass-card-hover">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-semibold text-primary-400 bg-primary-600/10 px-2 py-1 rounded">Week {fb.week_number}</span>
                  <span className="text-xs font-medium text-slate-400">
                    {fb.difficulty_rating === 1 ? "😎 Easy" : fb.difficulty_rating === 2 ? "💪 Right" : "😰 Hard"}
                  </span>
                </div>
                <div className="flex gap-1 mb-3 bg-black/20 p-2 rounded-lg justify-center">
                  {[1, 2, 3, 4, 5].map((s) => (
                    <span key={s} className="text-sm">{s <= (fb.overall_satisfaction || 0) ? "⭐" : "☆"}</span>
                  ))}
                </div>
                {fb.pros && (
                  <div className="mb-2">
                    <p className="text-[10px] uppercase text-success-500 font-semibold mb-0.5">Pros</p>
                    <p className="text-xs text-slate-300 line-clamp-2">{fb.pros}</p>
                  </div>
                )}
                {fb.cons && (
                  <div>
                    <p className="text-[10px] uppercase text-danger-500 font-semibold mb-0.5">Cons</p>
                    <p className="text-xs text-slate-300 line-clamp-2">{fb.cons}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="glass-card p-8 text-center animate-fade-in-up delay-300">
          <span className="text-4xl block mb-3">📝</span>
          <h3 className="text-lg font-semibold text-white mb-2">No Feedback Yet</h3>
          <p className="text-sm text-slate-400 max-w-md mx-auto">
            Complete your first week of training to submit your first check-in. Your feedback history will appear here.
          </p>
        </div>
      )}
    </main>
  );
}
