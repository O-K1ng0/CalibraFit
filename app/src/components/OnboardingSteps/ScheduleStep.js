"use client";

const DAYS = [
  { id: "monday", label: "Mon" },
  { id: "tuesday", label: "Tue" },
  { id: "wednesday", label: "Wed" },
  { id: "thursday", label: "Thu" },
  { id: "friday", label: "Fri" },
  { id: "saturday", label: "Sat" },
  { id: "sunday", label: "Sun" },
];

const TIME_SLOTS = [
  { id: "morning", label: "Morning", time: "6AM - 12PM", icon: "🌅" },
  { id: "afternoon", label: "Afternoon", time: "12PM - 5PM", icon: "☀️" },
  { id: "evening", label: "Evening", time: "5PM - 10PM", icon: "🌙" },
];

export default function ScheduleStep({ data, onUpdate }) {
  const toggleDay = (dayId) => {
    const current = data.preferred_workout_days || [];
    const updated = current.includes(dayId)
      ? current.filter((d) => d !== dayId)
      : [...current, dayId];
    onUpdate({
      preferred_workout_days: updated,
      weekly_frequency: updated.length || data.weekly_frequency,
    });
  };

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-success-500/20 mb-3">
          <span className="text-2xl">📅</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Your Schedule</h2>
        <p className="text-slate-400 text-sm mt-1">
          When do you prefer to work out?
        </p>
      </div>

      {/* Weekly Frequency */}
      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-3">
          <label className="input-label mb-0">Workouts Per Week</label>
          <span className="text-2xl font-bold text-primary-400">
            {data.weekly_frequency || 3}
          </span>
        </div>
        <input
          type="range"
          min={1}
          max={7}
          value={data.weekly_frequency || 3}
          onChange={(e) => onUpdate({ weekly_frequency: parseInt(e.target.value) })}
          className="w-full h-2 rounded-full appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #0d6efd ${((data.weekly_frequency || 3) - 1) / 6 * 100}%, rgba(255,255,255,0.1) ${((data.weekly_frequency || 3) - 1) / 6 * 100}%)`,
          }}
        />
        <div className="flex justify-between mt-2 text-[10px] text-slate-600">
          <span>Light</span>
          <span>Moderate</span>
          <span>Intense</span>
        </div>
      </div>

      {/* Preferred Days */}
      <div>
        <label className="input-label">Preferred Days</label>
        <div className="grid grid-cols-7 gap-2">
          {DAYS.map((day) => {
            const selected = (data.preferred_workout_days || []).includes(day.id);
            return (
              <button
                key={day.id}
                type="button"
                onClick={() => toggleDay(day.id)}
                className={`py-3 rounded-xl text-center text-sm font-medium transition-all duration-200 ${
                  selected
                    ? "bg-primary-600 text-white shadow-lg shadow-primary-600/20"
                    : "bg-white/5 text-slate-500 hover:bg-white/8 hover:text-slate-300 border border-white/10"
                }`}
              >
                {day.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Preferred Time */}
      <div>
        <label className="input-label">Preferred Time</label>
        <div className="grid grid-cols-3 gap-3">
          {TIME_SLOTS.map((slot) => {
            const selected = data.preferred_time === slot.id;
            return (
              <button
                key={slot.id}
                type="button"
                onClick={() => onUpdate({ preferred_time: slot.id })}
                className={`p-4 rounded-xl border text-center transition-all duration-200 ${
                  selected
                    ? "bg-primary-600/20 border-primary-500/40"
                    : "bg-white/5 border-white/10 hover:bg-white/8"
                }`}
              >
                <span className="text-2xl block mb-1">{slot.icon}</span>
                <span className={`text-sm font-medium ${selected ? "text-white" : "text-slate-400"}`}>
                  {slot.label}
                </span>
                <p className="text-[10px] text-slate-500 mt-0.5">{slot.time}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Summary */}
      <div className="glass-card p-4 animate-fade-in">
        <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Plan Summary</p>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-primary-500" />
            <span className="text-slate-300">
              {data.weekly_frequency || 3}x per week
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-success-500" />
            <span className="text-slate-300">
              {(data.preferred_workout_days || []).length || "No"} days selected
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-energy-500" />
            <span className="text-slate-300 capitalize">
              {data.preferred_time || "morning"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
