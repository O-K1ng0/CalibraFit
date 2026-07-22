"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getFullProfile, getCurrentPlan, isAuthenticated } from "@/lib/api";

export default function NutritionPage() {
  const router = useRouter();
  const [profileData, setProfileData] = useState(null);
  const [plan, setPlan] = useState(null);
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
      const [profileRes, planRes] = await Promise.allSettled([
        getFullProfile(),
        getCurrentPlan(),
      ]);

      if (profileRes.status === "fulfilled") setProfileData(profileRes.value);
      if (planRes.status === "fulfilled") setPlan(planRes.value);
    } catch (err) {
      console.error("Nutrition page load error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="flex-1 flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-400">Loading nutrition data...</p>
        </div>
      </main>
    );
  }

  // ── Nutrition Calculations (Mifflin-St Jeor) ──
  const profile = profileData?.profile || {};
  const weight = parseFloat(profile.weight_kg) || 70;
  const height = parseFloat(profile.height_cm) || 170;
  const age = parseInt(profile.age) || 25;
  const bmr = Math.round(10 * weight + 6.25 * height - 5 * age + 5);
  const activityMultiplier = profile.fitness_experience === "expert" ? 1.725 : profile.fitness_experience === "moderate" ? 1.55 : 1.375;
  const tdee = Math.round(bmr * activityMultiplier);
  
  const today = new Date().toISOString().split("T")[0];
  const todayWorkout = plan?.daily_workouts?.find((d) => d.date === today);
  const todayExerciseCount = todayWorkout?.routine?.length || 0;
  const estimatedCalsBurned = Math.round(todayExerciseCount * 5.5 * (weight / 70) * 8);

  const proteinG = Math.round(weight * 1.8);
  const fatG = Math.round((tdee * 0.25) / 9);
  const carbG = Math.round((tdee - proteinG * 4 - fatG * 9) / 4);

  return (
    <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-3xl mx-auto w-full">
      <div className="mb-8 animate-fade-in-up">
        <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">Nutrition & Recovery</h1>
        <p className="text-sm text-slate-400">
          Personalized macros and calorie targets based on your profile and daily plan.
        </p>
      </div>

      <div className="grid gap-6 animate-fade-in-up delay-100">
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Daily Energy Targets</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
              <div>
                <p className="text-sm font-medium text-slate-300">Basal Metabolic Rate (BMR)</p>
                <p className="text-xs text-slate-500">Calories burned at rest</p>
              </div>
              <span className="text-white font-bold">{bmr} cal</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-primary-600/10 border border-primary-500/20">
              <div>
                <p className="text-sm font-medium text-primary-400">Total Daily Target (TDEE)</p>
                <p className="text-xs text-primary-500/70">Maintenance calories</p>
              </div>
              <span className="text-primary-400 font-bold text-lg">{tdee} cal</span>
            </div>
            {estimatedCalsBurned > 0 && (
              <div className="flex justify-between items-center p-3 rounded-lg bg-energy-500/10 border border-energy-500/20">
                <div>
                  <p className="text-sm font-medium text-energy-400">Today&apos;s Workout Est.</p>
                  <p className="text-xs text-energy-500/70">Estimated burn from {todayWorkout?.day_type} day</p>
                </div>
                <span className="text-energy-400 font-bold">~{estimatedCalsBurned} cal</span>
              </div>
            )}
          </div>
        </div>

        <div className="glass-card p-6 animate-fade-in-up delay-200">
          <h2 className="text-lg font-semibold text-white mb-4">Recommended Macro Split</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 text-center">
              <p className="text-2xl font-bold text-blue-400 mb-1">{proteinG}g</p>
              <p className="text-sm font-medium text-slate-300">Protein</p>
              <p className="text-[10px] text-slate-500 mt-2">Muscle repair & growth</p>
            </div>
            <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
              <p className="text-2xl font-bold text-amber-400 mb-1">{carbG}g</p>
              <p className="text-sm font-medium text-slate-300">Carbohydrates</p>
              <p className="text-[10px] text-slate-500 mt-2">Primary energy source</p>
            </div>
            <div className="p-4 rounded-xl bg-pink-500/10 border border-pink-500/20 text-center">
              <p className="text-2xl font-bold text-pink-400 mb-1">{fatG}g</p>
              <p className="text-sm font-medium text-slate-300">Healthy Fats</p>
              <p className="text-[10px] text-slate-500 mt-2">Hormone regulation</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
