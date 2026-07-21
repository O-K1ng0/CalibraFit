"use client";

import dynamic from "next/dynamic";
import { useState } from "react";

// Dynamically import lottie-react to avoid SSR issues
const Lottie = dynamic(() => import("lottie-react"), { ssr: false });

export default function ExerciseAnimation({ animationUrl, exerciseName }) {
  const [error, setError] = useState(false);
  const [animationData, setAnimationData] = useState(null);
  const [loading, setLoading] = useState(!!animationUrl);

  // Load animation data from URL
  if (animationUrl && !animationData && !error && loading) {
    fetch(animationUrl)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load");
        return res.json();
      })
      .then((data) => {
        setAnimationData(data);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }

  // Fallback placeholder when no animation is available
  if (!animationUrl || error) {
    return (
      <div className="w-full h-40 rounded-xl bg-gradient-to-br from-primary-600/10 to-accent-500/10 flex flex-col items-center justify-center border border-white/5">
        <span className="text-4xl mb-2">🏋️</span>
        <p className="text-xs text-slate-500">{exerciseName}</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="w-full h-40 rounded-xl bg-white/5 flex items-center justify-center">
        <div className="animate-spin w-6 h-6 border-2 border-primary-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="w-full h-40 rounded-xl bg-white/5 overflow-hidden flex items-center justify-center">
      {animationData && (
        <Lottie
          animationData={animationData}
          loop
          style={{ height: "100%", width: "100%" }}
        />
      )}
    </div>
  );
}
