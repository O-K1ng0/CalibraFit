"use client";

export default function WorkoutStreaks({ currentStreak = 0, longestStreak = 0, workoutsThisWeek = 0 }) {
  return (
    <div className="grid grid-cols-3 gap-3">
      {/* Current Streak */}
      <div className="glass-card p-4 text-center glass-card-hover">
        <div className={`text-3xl mb-1 ${currentStreak > 0 ? "animate-streak-fire" : ""}`}>
          🔥
        </div>
        <p className="text-2xl font-bold text-white">{currentStreak}</p>
        <p className="text-[10px] text-slate-500 uppercase tracking-wider mt-1">Day Streak</p>
      </div>

      {/* Longest Streak */}
      <div className="glass-card p-4 text-center glass-card-hover">
        <div className="text-3xl mb-1">🏆</div>
        <p className="text-2xl font-bold text-white">{longestStreak}</p>
        <p className="text-[10px] text-slate-500 uppercase tracking-wider mt-1">Best Streak</p>
      </div>

      {/* This Week */}
      <div className="glass-card p-4 text-center glass-card-hover">
        <div className="text-3xl mb-1">📊</div>
        <p className="text-2xl font-bold text-white">{workoutsThisWeek}</p>
        <p className="text-[10px] text-slate-500 uppercase tracking-wider mt-1">This Week</p>
      </div>
    </div>
  );
}
