"use client";

const EQUIPMENT_LIST = [
  { id: "dumbbells", label: "Dumbbells", icon: "🏋️" },
  { id: "barbell", label: "Barbell", icon: "🏗️" },
  { id: "bench", label: "Bench", icon: "🪑" },
  { id: "pull_up_bar", label: "Pull-Up Bar", icon: "🔩" },
  { id: "resistance_bands", label: "Resistance Bands", icon: "🔗" },
  { id: "kettlebell", label: "Kettlebell", icon: "🔔" },
  { id: "squat_rack", label: "Squat Rack", icon: "🏗️" },
  { id: "cable_machine", label: "Cable Machine", icon: "⚙️" },
  { id: "leg_press_machine", label: "Leg Press", icon: "🦿" },
  { id: "leg_curl_machine", label: "Leg Curl Machine", icon: "🦵" },
  { id: "ab_wheel", label: "Ab Wheel", icon: "🎡" },
  { id: "jump_rope", label: "Jump Rope", icon: "🪢" },
  { id: "yoga_mat", label: "Yoga Mat", icon: "🧘" },
  { id: "foam_roller", label: "Foam Roller", icon: "🧻" },
];

export default function EquipmentStep({ data, onUpdate }) {
  const toggleEquipment = (id) => {
    const current = data.available_equipment || [];
    const updated = current.includes(id)
      ? current.filter((e) => e !== id)
      : [...current, id];
    onUpdate({ available_equipment: updated });
  };

  const isGym = data.training_environment === "gym";

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-energy-500/20 mb-3">
          <span className="text-2xl">🏠</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Equipment & Environment</h2>
        <p className="text-slate-400 text-sm mt-1">
          Where do you work out and what do you have access to?
        </p>
      </div>

      {/* Environment Toggle */}
      <div className="glass-card p-4">
        <label className="input-label mb-3">Training Environment</label>
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => onUpdate({ training_environment: "home" })}
            className={`p-4 rounded-xl border transition-all duration-200 text-center ${
              !isGym
                ? "bg-primary-600/20 border-primary-500/40 shadow-lg shadow-primary-600/10"
                : "bg-white/5 border-white/10 hover:bg-white/8"
            }`}
          >
            <span className="text-3xl block mb-2">🏠</span>
            <span className="font-semibold text-white text-sm">Home</span>
            <p className="text-[10px] text-slate-400 mt-1">Workout from home</p>
          </button>
          <button
            type="button"
            onClick={() => onUpdate({ training_environment: "gym" })}
            className={`p-4 rounded-xl border transition-all duration-200 text-center ${
              isGym
                ? "bg-primary-600/20 border-primary-500/40 shadow-lg shadow-primary-600/10"
                : "bg-white/5 border-white/10 hover:bg-white/8"
            }`}
          >
            <span className="text-3xl block mb-2">🏢</span>
            <span className="font-semibold text-white text-sm">Gym</span>
            <p className="text-[10px] text-slate-400 mt-1">Full gym access</p>
          </button>
        </div>
      </div>

      {/* Equipment Grid */}
      <div>
        <label className="input-label">
          Available Equipment
          <span className="text-slate-600 ml-1 normal-case">
            ({(data.available_equipment || []).length} selected)
          </span>
        </label>
        <div className="grid grid-cols-2 gap-2">
          {EQUIPMENT_LIST.map((equip) => {
            const selected = (data.available_equipment || []).includes(equip.id);
            return (
              <button
                key={equip.id}
                type="button"
                onClick={() => toggleEquipment(equip.id)}
                className={`flex items-center gap-3 p-3 rounded-xl border transition-all duration-200 ${
                  selected
                    ? "bg-primary-600/15 border-primary-500/30"
                    : "bg-white/5 border-white/10 hover:bg-white/8"
                }`}
              >
                <span className="text-xl">{equip.icon}</span>
                <span className={`text-sm ${selected ? "text-white font-medium" : "text-slate-400"}`}>
                  {equip.label}
                </span>
                {selected && (
                  <svg className="w-4 h-4 text-primary-400 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bodyweight note */}
      <p className="text-xs text-slate-500 text-center">
        💡 Bodyweight exercises are always included regardless of equipment selection
      </p>
    </div>
  );
}
