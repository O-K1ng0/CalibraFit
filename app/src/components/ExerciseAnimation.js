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

  // Fallback to dynamic YouTube search for exercise tutorial
  if (!animationUrl || error) {
    const searchQuery = encodeURIComponent(`${exerciseName} exercise form tutorial`);
    return (
      <div className="w-full h-48 rounded-xl overflow-hidden bg-black/50 border border-white/5">
        <iframe
          width="100%"
          height="100%"
          src={`https://www.youtube.com/embed?listType=search&list=${searchQuery}`}
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          title={`How to do ${exerciseName}`}
        ></iframe>
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
