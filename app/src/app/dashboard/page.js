"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  getMe, getProgress, getCurrentPlan, getPlanSummary,
  getFullProfile, getFeedbacks, submitFeedback, logout, isAuthenticated,
} from "@/lib/api";
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

const PAIN_AREA_OPTIONS = [
  "knees", "shoulders", "back", "wrists", "hips", "neck", "ankles", "elbows",
];

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [progress, setProgress] = useState(null);
  const [planSummary, setPlanSummary] = useState(null);
  const [plan, setPlan] = useState(null);
  const [profileData, setProfileData] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quote] = useState(() => MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)]);

  // Weekly Feedback Form State
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackForm, setFeedbackForm] = useState({
    difficulty_rating: 2,
    energy_level: 3,
    pros: "",
    cons: "",
    new_pain_areas: [],
    overall_satisfaction: 3,
  });
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    loadDashboard();
  }, [router]);

  const loadDashboard = async () => {
    try {
      const [userData, progressData, planData, profileRes, feedbackRes] = await Promise.allSettled([
        getMe(),
        getProgress(),
        getCurrentPlan(),
        getFullProfile(),
        getFeedbacks(),
      ]);

      if (userData.status === "fulfilled") setUser(userData.value);
      if (progressData.status === "fulfilled") setProgress(progressData.value);
      if (planData.status === "fulfilled") setPlan(planData.value);
      if (profileRes.status === "fulfilled") setProfileData(profileRes.value);
      if (feedbackRes.status === "fulfilled") setFeedbacks(feedbackRes.value);
    } catch (err) {
      console.error("Dashboard load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const today = new Date().toISOString().split("T")[0];
  const todayWorkout = plan?.daily_workouts?.find((d) => d.date === today);

  // ── Nutrition Calculations (Mifflin-St Jeor) ──
  const profile = profileData?.profile || {};
  const weight = parseFloat(profile.weight_kg) || 70;
  const height = parseFloat(profile.height_cm) || 170;
  const age = parseInt(profile.age) || 25;
  const bmr = Math.round(10 * weight + 6.25 * height - 5 * age + 5); // Male default
  const activityMultiplier = profile.fitness_experience === "expert" ? 1.725 : profile.fitness_experience === "moderate" ? 1.55 : 1.375;
  const tdee = Math.round(bmr * activityMultiplier);
  const todayExerciseCount = todayWorkout?.routine?.length || 0;
  const estimatedCalsBurned = Math.round(todayExerciseCount * 5.5 * (weight / 70) * 8); // ~8 min per exercise, MET ~5.5

  const proteinG = Math.round(weight * 1.8);
  const fatG = Math.round((tdee * 0.25) / 9);
  const carbG = Math.round((tdee - proteinG * 4 - fatG * 9) / 4);

  // ── Weekly Feedback Logic ──
  const currentWeek = plan ? Math.ceil((new Date(today) - new Date(plan.start_date)) / (7 * 24 * 60 * 60 * 1000)) : 0;
  const alreadySubmitted = feedbacks.some((f) => f.week_number === currentWeek);
  const showCheckIn = plan && currentWeek >= 1 && !alreadySubmitted;

  const handleFeedbackSubmit = async () => {
    setFeedbackSubmitting(true);
    try {
      await submitFeedback({
        plan_id: plan.plan_id,
        week_number: currentWeek,
        ...feedbackForm,
      });
      setFeedbackSubmitted(true);
      setShowFeedback(false);
      const updated = await getFeedbacks();
      setFeedbacks(updated);
    } catch (err) {
      console.error("Feedback submit error:", err);
    } finally {
      setFeedbackSubmitting(false);
    }
  };

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


      {/* Weekly Check-In Banner */}
      {showCheckIn && !feedbackSubmitted && (
        <div className="mb-6 animate-fade-in-up delay-150">
          <div className="glass-card p-5 border border-primary-500/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📋</span>
                <div>
                  <h3 className="text-sm font-semibold text-white">Week {currentWeek} Check-In</h3>
                  <p className="text-xs text-slate-400">How was your training this week? Your feedback adapts future plans.</p>
                </div>
              </div>
              <button onClick={() => setShowFeedback(!showFeedback)} className="btn-secondary text-xs py-2 px-4">
                {showFeedback ? "Close" : "Give Feedback"}
              </button>
            </div>

            {showFeedback && (
              <div className="mt-4 space-y-4 border-t border-white/10 pt-4 animate-fade-in">
                {/* Difficulty Rating */}
                <div>
                  <label className="input-label">How did the difficulty feel?</label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { val: 1, label: "Too Easy", icon: "😎" },
                      { val: 2, label: "Just Right", icon: "💪" },
                      { val: 3, label: "Too Hard", icon: "😰" },
                    ].map((opt) => (
                      <button key={opt.val} type="button"
                        onClick={() => setFeedbackForm({ ...feedbackForm, difficulty_rating: opt.val })}
                        className={`p-3 rounded-xl border text-center transition-all ${feedbackForm.difficulty_rating === opt.val ? "bg-primary-600/20 border-primary-500/40" : "bg-white/5 border-white/10"}`}
                      >
                        <span className="text-xl block">{opt.icon}</span>
                        <span className="text-xs text-white">{opt.label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Energy Level */}
                <div>
                  <label className="input-label">Energy Level (1-5)</label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map((n) => (
                      <button key={n} type="button"
                        onClick={() => setFeedbackForm({ ...feedbackForm, energy_level: n })}
                        className={`w-10 h-10 rounded-xl border text-sm font-medium transition-all ${feedbackForm.energy_level === n ? "bg-primary-600 border-primary-500 text-white" : "bg-white/5 border-white/10 text-slate-400"}`}
                      >
                        {n}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Satisfaction Stars */}
                <div>
                  <label className="input-label">Overall Satisfaction</label>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button key={star} type="button"
                        onClick={() => setFeedbackForm({ ...feedbackForm, overall_satisfaction: star })}
                        className="text-2xl transition-transform hover:scale-110"
                      >
                        {star <= (feedbackForm.overall_satisfaction || 0) ? "⭐" : "☆"}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Pros & Cons */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="input-label" htmlFor="feedbackPros">Pros</label>
                    <textarea id="feedbackPros" className="input-field resize-none" rows={2}
                      placeholder="What went well..."
                      value={feedbackForm.pros}
                      onChange={(e) => setFeedbackForm({ ...feedbackForm, pros: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="input-label" htmlFor="feedbackCons">Cons</label>
                    <textarea id="feedbackCons" className="input-field resize-none" rows={2}
                      placeholder="What felt off or painful..."
                      value={feedbackForm.cons}
                      onChange={(e) => setFeedbackForm({ ...feedbackForm, cons: e.target.value })}
                    />
                  </div>
                </div>

                {/* New Pain Areas */}
                <div>
                  <label className="input-label">Any new pain areas?</label>
                  <div className="flex flex-wrap gap-2">
                    {PAIN_AREA_OPTIONS.map((area) => (
                      <button key={area} type="button"
                        onClick={() => {
                          const current = feedbackForm.new_pain_areas || [];
                          setFeedbackForm({
                            ...feedbackForm,
                            new_pain_areas: current.includes(area) ? current.filter(a => a !== area) : [...current, area],
                          });
                        }}
                        className={`chip ${(feedbackForm.new_pain_areas || []).includes(area) ? "selected" : ""}`}
                      >
                        {area}
                      </button>
                    ))}
                  </div>
                </div>

                <button onClick={handleFeedbackSubmit} disabled={feedbackSubmitting} className="btn-primary w-full">
                  {feedbackSubmitting ? "Submitting..." : "Submit Week " + currentWeek + " Feedback ✓"}
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {feedbackSubmitted && (
        <div className="mb-6 p-3 rounded-lg bg-success-500/10 border border-success-500/20 text-success-400 text-sm animate-fade-in">
          ✓ Week {currentWeek} feedback submitted! Your next plan will adapt to your responses.
        </div>
      )}

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
                  {estimatedCalsBurned > 0 && (
                    <span className="text-sm text-energy-400">
                      ~{estimatedCalsBurned} cal
                    </span>
                  )}
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

