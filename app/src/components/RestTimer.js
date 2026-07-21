"use client";

import { useState, useEffect, useCallback } from "react";

export default function RestTimer({ seconds = 60, onComplete, autoStart = false }) {
  const [timeLeft, setTimeLeft] = useState(seconds);
  const [isRunning, setIsRunning] = useState(autoStart);
  const [isComplete, setIsComplete] = useState(false);

  const circumference = 2 * Math.PI * 50;
  const progress = ((seconds - timeLeft) / seconds) * circumference;

  useEffect(() => {
    if (!isRunning || timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setIsRunning(false);
          setIsComplete(true);
          // Play notification sound
          try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 880;
            oscillator.type = "sine";
            gainNode.gain.value = 0.3;
            oscillator.start();
            setTimeout(() => {
              oscillator.stop();
              audioCtx.close();
            }, 300);
          } catch (e) {
            // Audio not available
          }
          if (onComplete) onComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isRunning, timeLeft, seconds, onComplete]);

  const handleStart = () => {
    if (isComplete) {
      setTimeLeft(seconds);
      setIsComplete(false);
    }
    setIsRunning(true);
  };

  const handlePause = () => setIsRunning(false);

  const handleReset = () => {
    setIsRunning(false);
    setIsComplete(false);
    setTimeLeft(seconds);
  };

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  const getColor = () => {
    if (isComplete) return "#22c55e";
    if (timeLeft <= 10) return "#ef4444";
    if (timeLeft <= 20) return "#eab308";
    return "#0d6efd";
  };

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="timer-circle">
        <svg width="120" height="120" viewBox="0 0 120 120">
          {/* Background circle */}
          <circle
            cx="60" cy="60" r="50"
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="6"
          />
          {/* Progress circle */}
          <circle
            cx="60" cy="60" r="50"
            fill="none"
            stroke={getColor()}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference - progress}
            className="progress-ring-circle"
          />
        </svg>
        <div className="timer-text" style={{ color: getColor() }}>
          {isComplete ? "✓" : formatTime(timeLeft)}
        </div>
      </div>

      <div className="flex gap-2">
        {!isRunning && !isComplete && (
          <button onClick={handleStart} className="btn-primary text-sm py-2 px-4">
            {timeLeft < seconds ? "Resume" : "Start"}
          </button>
        )}
        {isRunning && (
          <button onClick={handlePause} className="btn-secondary text-sm py-2 px-4">
            Pause
          </button>
        )}
        {(timeLeft < seconds || isComplete) && (
          <button onClick={handleReset} className="btn-secondary text-sm py-2 px-4">
            Reset
          </button>
        )}
      </div>

      <p className="text-[10px] text-slate-500 uppercase tracking-wider">Rest Timer</p>
    </div>
  );
}
