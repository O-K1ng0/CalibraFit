"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getDailyWorkout, completeWorkout, isAuthenticated } from "@/lib/api";
import ExerciseCard from "@/components/ExerciseCard";
import ProgressBar from "@/components/ProgressBar";

export default function WorkoutPage({ params }) {
  const { date } = use(params);
  const router = useRouter();
  const [workout, setWorkout] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [completedSets, setCompletedSets] = useState({}); // { exerciseId: [setIdx, ...] }
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [startTime] = useState(() => Date.now());

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    loadWorkout();
  }, [date, router]);

  const loadWorkout = async () => {
    try {
      const data = await getDailyWorkout(date);
      setWorkout(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load workout");
    } finally {
      setLoading(false);
    }
  };

  const handleSetComplete = (exerciseId, setIndex) => {
    setCompletedSets((prev) => ({
      ...prev,
      [exerciseId]: [...(prev[exerciseId] || []), setIndex],
    }));
  };

  const getTotalSets = () => {
    if (!workout?.routine) return 0;
    return workout.routine.reduce((sum, ex) => sum + (ex.sets || 3), 0);
  };

  const getCompletedCount = () => {
    return Object.values(completedSets).reduce((sum, sets) => sum + sets.length, 0);
  };

  const isAllComplete = () => {
    if (!workout?.routine) return false;
    return workout.routine.every((ex) => {
      const done = (completedSets[ex.exercise_id] || []).length;
      return done >= (ex.sets || 3);
    });
  };

  const handleCompleteWorkout = async () => {
    setSubmitting(true);
    try {
      const durationMinutes = Math.round((Date.now() - startTime) / 60000);
      const setsData = [];
      for (const [exerciseId, sets] of Object.entries(completedSets)) {
        for (const setIdx of sets) {
          const ex = workout.routine.find((e) => e.exercise_id === parseInt(exerciseId));
          setsData.push({
            exercise_id: parseInt(exerciseId),
            set_number: setIdx + 1,
            reps_done: ex?.reps || 10,
          });
        }
      }

      await completeWorkout({
        daily_workout_id: workout.daily_workout_id,
        sets_completed: setsData,
        duration_minutes: durationMinutes,
      });

      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save workout");
    } finally {
      setSubmitting(false);
    }
  };

  const formattedDate = new Date(date + "T00:00:00").toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  if (loading) {
    return (
      <main className="flex-1 flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-400">Loading workout...</p>
        </div>
      </main>
    );
  }

  if (error && !workout) {
    return (
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="text-center glass-card p-8 max-w-md">
          <span className="text-5xl block mb-4">😕</span>
          <h2 className="text-xl font-bold text-white mb-2">Workout Not Found</h2>
          <p className="text-sm text-slate-400 mb-4">{error}</p>
          <Link href="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </main>
    );
  }

  if (submitted) {
    return (
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="text-center glass-card p-8 max-w-md animate-fade-in-up">
          <div className="text-6xl mb-4 animate-streak-fire">🎉</div>
          <h2 className="text-2xl font-bold text-white mb-2">Workout Complete!</h2>
          <p className="text-sm text-slate-400 mb-2">
            Great job finishing your {workout?.day_type} workout.
          </p>
          <p className="text-sm text-slate-500 mb-6">
            Duration: {Math.round((Date.now() - startTime) / 60000)} minutes
          </p>
          <div className="flex gap-3 justify-center">
            <Link href="/dashboard" className="btn-primary">
              Back to Dashboard
            </Link>
          </div>
        </div>
      </main>
    );
  }

  if (workout?.day_type === "Rest") {
    return (
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="text-center glass-card p-8 max-w-md">
          <span className="text-5xl block mb-4">😴</span>
          <h2 className="text-xl font-bold text-white mb-2">Rest Day</h2>
          <p className="text-sm text-slate-400 mb-4">
            {formattedDate} is a rest day. Recovery is essential for progress!
          </p>
          <Link href="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-3xl mx-auto w-full">
      {/* Header */}
      <div className="mb-6 animate-fade-in-up">
        <Link href="/dashboard" className="text-sm text-slate-500 hover:text-slate-300 transition-colors mb-2 inline-block">
          ← Back to Dashboard
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{workout?.day_type} Day</h1>
            <p className="text-sm text-slate-400 mt-1">{formattedDate}</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => window.print()}
              className="btn-secondary text-xs py-1.5 px-3 flex items-center gap-1"
            >
              <span>📄</span>
              <span className="hidden sm:inline">Download PDF</span>
            </button>
            <span className="px-3 py-1 rounded-full text-xs font-semibold gradient-primary text-white">
              {workout?.routine?.length || 0} exercises
            </span>
          </div>
        </div>
      </div>

      {/* Overall Progress */}
      <div className="glass-card p-4 mb-6 animate-fade-in-up delay-100">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">Overall Progress</span>
          <span className="text-sm font-medium text-white">
            {getCompletedCount()} / {getTotalSets()} sets
          </span>
        </div>
        <ProgressBar
          value={getCompletedCount()}
          max={getTotalSets()}
          size="md"
          color={isAllComplete() ? "success" : "primary"}
          showLabel={false}
        />
      </div>

      {/* Exercise List */}
      <div className="space-y-3 mb-6">
        {(workout?.routine || []).map((exercise, index) => (
          <div key={exercise.exercise_id} className="animate-fade-in-up" style={{ animationDelay: `${0.15 + index * 0.05}s` }}>
            <ExerciseCard
              exercise={exercise}
              index={index}
              onSetComplete={handleSetComplete}
              completedSets={completedSets[exercise.exercise_id] || []}
            />
          </div>
        ))}
      </div>

      {/* Complete Button */}
      {getCompletedCount() > 0 && (
        <div className="sticky bottom-4 animate-fade-in-up">
          <button
            onClick={handleCompleteWorkout}
            disabled={submitting}
            className={`w-full py-4 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
              isAllComplete()
                ? "gradient-success shadow-lg shadow-success-500/20 animate-pulse-glow"
                : "gradient-primary shadow-lg shadow-primary-600/20"
            }`}
          >
            {submitting ? (
              <>
                <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Saving...
              </>
            ) : isAllComplete() ? (
              "Complete Workout 🏆"
            ) : (
              `Save Progress (${getCompletedCount()}/${getTotalSets()} sets)`
            )}
          </button>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-4 p-3 rounded-lg bg-danger-500/10 border border-danger-500/20 text-danger-400 text-sm">
          {error}
        </div>
      )}
    </main>
  );
}
