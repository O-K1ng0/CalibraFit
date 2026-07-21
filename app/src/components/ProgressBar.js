"use client";

export default function ProgressBar({ value = 0, max = 100, size = "md", color = "primary", showLabel = true }) {
  const percentage = Math.min(Math.round((value / max) * 100), 100);

  const heights = { sm: "h-1.5", md: "h-2.5", lg: "h-4" };
  const gradients = {
    primary: "from-primary-500 to-primary-400",
    success: "from-success-500 to-green-400",
    energy: "from-energy-500 to-yellow-400",
    accent: "from-accent-500 to-purple-400",
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between mb-1">
          <span className="text-xs text-slate-500">{percentage}%</span>
        </div>
      )}
      <div className={`w-full ${heights[size]} rounded-full bg-white/5 overflow-hidden`}>
        <div
          className={`${heights[size]} rounded-full bg-gradient-to-r ${gradients[color]} transition-all duration-700 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
