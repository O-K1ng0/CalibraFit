"use client";

const LEVELS = [
  {
    id: "beginner",
    title: "Beginner",
    subtitle: "New to fitness",
    description: "Little to no workout experience. We'll start you with foundational exercises.",
    icon: "🌱",
    gradient: "from-green-500/20 to-emerald-500/20",
    border: "border-green-500/30",
  },
  {
    id: "moderate",
    title: "Moderate",
    subtitle: "Some experience",
    description: "Worked out before but not consistently. Ready for moderate intensity.",
    icon: "💪",
    gradient: "from-primary-500/20 to-blue-500/20",
    border: "border-primary-500/30",
  },
  {
    id: "expert",
    title: "Expert",
    subtitle: "Experienced lifter",
    description: "Consistent workout history. Ready for advanced exercises and higher volume.",
    icon: "🔥",
    gradient: "from-orange-500/20 to-red-500/20",
    border: "border-orange-500/30",
  },
];

export default function FitnessExperienceStep({ data, onUpdate }) {
  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-accent-500/20 mb-3">
          <span className="text-2xl">🏋️</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Fitness Level</h2>
        <p className="text-slate-400 text-sm mt-1">
          This determines exercise difficulty and volume
        </p>
      </div>

      {/* Experience Level Cards */}
      <div className="space-y-3">
        {LEVELS.map((level) => (
          <button
            key={level.id}
            type="button"
            onClick={() => onUpdate({ fitness_experience: level.id })}
            className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
              data.fitness_experience === level.id
                ? `bg-gradient-to-r ${level.gradient} ${level.border} scale-[1.02] shadow-lg`
                : "bg-white/5 border-white/10 hover:bg-white/8 hover:border-white/15"
            }`}
          >
            <div className="flex items-center gap-4">
              <span className="text-3xl">{level.icon}</span>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-white">{level.title}</h3>
                  <span className="text-xs text-slate-500">— {level.subtitle}</span>
                </div>
                <p className="text-sm text-slate-400 mt-0.5">{level.description}</p>
              </div>
              {data.fitness_experience === level.id && (
                <svg className="w-5 h-5 text-primary-400 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              )}
            </div>
          </button>
        ))}
      </div>

      {/* Time Since Last Workout */}
      <div>
        <label className="input-label" htmlFor="lastWorkout">Time Since Last Workout</label>
        <select
          id="lastWorkout"
          className="input-field"
          value={data.time_since_last_workout_days || 0}
          onChange={(e) => onUpdate({ time_since_last_workout_days: parseInt(e.target.value) })}
        >
          <option value={0}>Currently active</option>
          <option value={7}>Less than a week</option>
          <option value={30}>About a month</option>
          <option value={60}>1–3 months</option>
          <option value={135}>3–6 months</option>
          <option value={270}>6–12 months</option>
          <option value={545}>1–2 years</option>
          <option value={1000}>More than 2 years</option>
        </select>
      </div>

      {/* Optional Metrics */}
      <div>
        <h3 className="input-label mb-3">Optional Health Metrics</h3>
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-[10px] text-slate-500 mb-1" htmlFor="restingHr">Resting HR (bpm)</label>
            <input
              id="restingHr"
              type="number"
              className="input-field text-sm py-2"
              placeholder="65"
              min={30}
              max={220}
              value={data.resting_heart_rate || ""}
              onChange={(e) => onUpdate({ resting_heart_rate: parseInt(e.target.value) || null })}
            />
          </div>
          <div>
            <label className="block text-[10px] text-slate-500 mb-1" htmlFor="dailySteps">Daily Steps</label>
            <input
              id="dailySteps"
              type="number"
              className="input-field text-sm py-2"
              placeholder="8000"
              min={0}
              value={data.daily_step_count || ""}
              onChange={(e) => onUpdate({ daily_step_count: parseInt(e.target.value) || null })}
            />
          </div>
          <div>
            <label className="block text-[10px] text-slate-500 mb-1" htmlFor="bodyFat">Body Fat %</label>
            <input
              id="bodyFat"
              type="number"
              className="input-field text-sm py-2"
              placeholder="20"
              min={1}
              max={70}
              step={0.1}
              value={data.body_fat_percentage || ""}
              onChange={(e) => onUpdate({ body_fat_percentage: parseFloat(e.target.value) || null })}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
