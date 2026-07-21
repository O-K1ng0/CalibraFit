"use client";

import { useState } from "react";

export default function DemographicsStep({ data, onUpdate }) {
  const bmi =
    data.height_cm && data.weight_kg
      ? (data.weight_kg / ((data.height_cm / 100) ** 2)).toFixed(1)
      : null;

  const getBmiCategory = (bmi) => {
    if (!bmi) return null;
    const v = parseFloat(bmi);
    if (v < 18.5) return { label: "Underweight", color: "text-blue-400", bg: "bg-blue-500/20" };
    if (v < 25) return { label: "Normal", color: "text-success-400", bg: "bg-success-500/20" };
    if (v < 30) return { label: "Overweight", color: "text-energy-400", bg: "bg-energy-500/20" };
    return { label: "Obese", color: "text-danger-400", bg: "bg-danger-500/20" };
  };

  const bmiCat = getBmiCategory(bmi);

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary-600/20 mb-3">
          <span className="text-2xl">📋</span>
        </div>
        <h2 className="text-2xl font-bold text-white">About You</h2>
        <p className="text-slate-400 text-sm mt-1">Let&apos;s start with some basic information</p>
      </div>

      <div>
        <label className="input-label" htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          className="input-field"
          placeholder="25"
          min={13}
          max={120}
          value={data.age || ""}
          onChange={(e) => onUpdate({ age: parseInt(e.target.value) || "" })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="input-label" htmlFor="height">Height (cm)</label>
          <input
            id="height"
            type="number"
            className="input-field"
            placeholder="175"
            min={100}
            max={250}
            step={0.1}
            value={data.height_cm || ""}
            onChange={(e) => onUpdate({ height_cm: parseFloat(e.target.value) || "" })}
          />
        </div>
        <div>
          <label className="input-label" htmlFor="weight">Weight (kg)</label>
          <input
            id="weight"
            type="number"
            className="input-field"
            placeholder="70"
            min={30}
            max={300}
            step={0.1}
            value={data.weight_kg || ""}
            onChange={(e) => onUpdate({ weight_kg: parseFloat(e.target.value) || "" })}
          />
        </div>
      </div>

      {/* BMI Display */}
      {bmi && (
        <div className="glass-card p-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">Your BMI</p>
              <p className="text-2xl font-bold text-white mt-1">{bmi}</p>
            </div>
            {bmiCat && (
              <span className={`px-3 py-1.5 rounded-full text-xs font-semibold ${bmiCat.color} ${bmiCat.bg}`}>
                {bmiCat.label}
              </span>
            )}
          </div>
          {/* BMI Bar */}
          <div className="mt-3 h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${Math.min((parseFloat(bmi) / 40) * 100, 100)}%`,
                background: `linear-gradient(90deg, #3b82f6, #22c55e, #eab308, #ef4444)`,
              }}
            />
          </div>
          <div className="flex justify-between mt-1 text-[10px] text-slate-600">
            <span>Underweight</span>
            <span>Normal</span>
            <span>Overweight</span>
            <span>Obese</span>
          </div>
        </div>
      )}
    </div>
  );
}
