"use client";

import { useState } from "react";
import ExerciseAnimation from "./ExerciseAnimation";
import RestTimer from "./RestTimer";

const DIFFICULTY_LABELS = {
  1: { label: "Beginner", color: "text-green-400", bg: "bg-green-500/15" },
  2: { label: "Moderate", color: "text-blue-400", bg: "bg-blue-500/15" },
  3: { label: "Advanced", color: "text-orange-400", bg: "bg-orange-500/15" },
};

export default function ExerciseCard({
  exercise,
  index,
  onSetComplete,
  completedSets = [],
}) {
  const [expanded, setExpanded] = useState(false);
  const [showTimer, setShowTimer] = useState(false);

  const diff = DIFFICULTY_LABELS[exercise.difficulty] || DIFFICULTY_LABELS[1];
  const totalSets = exercise.sets || 3;
  const completedCount = completedSets.length;
  const allDone = completedCount >= totalSets;

  return (
    <div
      className={`glass-card overflow-hidden transition-all duration-300 ${
        allDone ? "opacity-60" : ""
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      {/* Header */}
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left p-4 flex items-center gap-4 hover:bg-white/5 transition-colors"
      >
        {/* Exercise Number */}
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-sm font-bold shrink-0 ${
          allDone ? "gradient-success text-white" : "bg-white/10 text-slate-300"
        }`}>
          {allDone ? "✓" : index + 1}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-white text-sm truncate">{exercise.name}</h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs text-slate-400">
              {exercise.sets} × {exercise.reps} reps
            </span>
            <span className="text-slate-700">•</span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-medium ${diff.color} ${diff.bg}`}>
              {diff.label}
            </span>
          </div>
        </div>

        {/* Progress */}
        <div className="text-right shrink-0">
          <p className="text-xs text-slate-500">{completedCount}/{totalSets} sets</p>
          <div className="w-16 h-1.5 rounded-full bg-white/5 mt-1 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-primary-500 to-success-500 transition-all duration-300"
              style={{ width: `${(completedCount / totalSets) * 100}%` }}
            />
          </div>
        </div>

        {/* Chevron */}
        <svg
          className={`w-4 h-4 text-slate-500 shrink-0 transition-transform duration-200 ${
            expanded ? "rotate-180" : ""
          }`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Expanded Content */}
      {expanded && (
        <div className="px-4 pb-4 space-y-4 animate-fade-in border-t border-white/5 pt-4">
          {/* Animation */}
          <ExerciseAnimation
            animationUrl={exercise.animation_url}
            exerciseName={exercise.name}
          />

          {/* Description */}
          {exercise.description && (
            <p className="text-sm text-slate-400">{exercise.description}</p>
          )}

          {/* Muscle Tags */}
          <div className="flex flex-wrap gap-1.5">
            <span className="chip selected text-[10px]">{exercise.target_muscle_primary}</span>
            {(exercise.target_muscle_secondary || []).map((m) => (
              <span key={m} className="chip text-[10px]">{m}</span>
            ))}
          </div>

          {/* Equipment */}
          {(exercise.equipment_required || []).length > 0 && (
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span>🔧</span>
              <span>{exercise.equipment_required.join(", ")}</span>
            </div>
          )}

          {/* Set Tracking */}
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Track Sets</p>
            <div className="flex gap-2 flex-wrap">
              {Array.from({ length: totalSets }, (_, i) => {
                const done = completedSets.includes(i);
                return (
                  <button
                    key={i}
                    type="button"
                    onClick={() => {
                      if (!done && onSetComplete) {
                        onSetComplete(exercise.exercise_id, i);
                        setShowTimer(true);
                      }
                    }}
                    disabled={done}
                    className={`w-12 h-12 rounded-xl flex flex-col items-center justify-center text-xs font-medium transition-all duration-200 ${
                      done
                        ? "bg-success-500/20 text-success-400 border border-success-500/30"
                        : "bg-white/5 text-slate-400 border border-white/10 hover:bg-primary-600/20 hover:border-primary-500/30 hover:text-primary-400"
                    }`}
                  >
                    {done ? "✓" : `Set ${i + 1}`}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Rest Timer */}
          {showTimer && !allDone && (
            <div className="flex justify-center pt-2">
              <RestTimer
                seconds={exercise.rest_seconds || 60}
                onComplete={() => setShowTimer(false)}
                autoStart={true}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
