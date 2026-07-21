"use client";

import { useState } from "react";

const SURGERY_OPTIONS = [
  "Knee replacement", "Hip replacement", "Shoulder surgery",
  "Spinal surgery", "ACL reconstruction", "Rotator cuff repair",
  "Heart surgery", "Hernia repair", "Appendectomy",
];

const CHRONIC_DISEASES = [
  "Hypertension", "Diabetes", "Asthma", "Arthritis",
  "Heart disease", "Osteoporosis", "Fibromyalgia", "COPD",
];

const PAIN_AREAS = [
  { id: "lower_back", label: "Lower Back", icon: "🔻" },
  { id: "upper_back", label: "Upper Back", icon: "🔼" },
  { id: "neck", label: "Neck", icon: "🦴" },
  { id: "knees", label: "Knees", icon: "🦵" },
  { id: "shoulders", label: "Shoulders", icon: "💪" },
  { id: "hips", label: "Hips", icon: "🦴" },
  { id: "wrists", label: "Wrists", icon: "🤚" },
  { id: "ankles", label: "Ankles", icon: "🦶" },
  { id: "elbows", label: "Elbows", icon: "💪" },
];

// Maps pain areas and conditions to contraindication flags
function deriveContraindicationFlags(medicalData) {
  const flags = new Set();
  const painAreas = medicalData.pain_areas || [];
  const surgeries = medicalData.past_surgeries || [];
  const diseases = medicalData.chronic_diseases || [];

  if (painAreas.includes("lower_back")) flags.add("lower_back_pain");
  if (painAreas.includes("knees")) flags.add("knee_injury");
  if (painAreas.includes("shoulders")) flags.add("shoulder_injury");
  if (painAreas.includes("wrists")) flags.add("wrist_injury");
  if (painAreas.includes("neck")) flags.add("neck_issues");
  if (painAreas.includes("hips")) flags.add("hip_replacement");
  if (painAreas.includes("ankles")) flags.add("ankle_injury");
  if (painAreas.includes("elbows")) flags.add("joint_pain");

  if (surgeries.some(s => s.toLowerCase().includes("knee"))) flags.add("knee_injury");
  if (surgeries.some(s => s.toLowerCase().includes("hip"))) flags.add("hip_replacement");
  if (surgeries.some(s => s.toLowerCase().includes("shoulder"))) flags.add("shoulder_injury");
  if (surgeries.some(s => s.toLowerCase().includes("spinal") || s.toLowerCase().includes("spine"))) flags.add("spinal_issues");
  if (surgeries.some(s => s.toLowerCase().includes("heart"))) flags.add("heart_condition");

  if (diseases.includes("Heart disease")) flags.add("heart_condition");
  if (diseases.includes("Arthritis")) flags.add("joint_pain");
  if (diseases.includes("Osteoporosis")) flags.add("spinal_issues");

  return Array.from(flags);
}

export default function MedicalHistoryStep({ data, onUpdate }) {
  const [customSurgery, setCustomSurgery] = useState("");

  const toggleArrayItem = (field, item) => {
    const current = data[field] || [];
    const updated = current.includes(item)
      ? current.filter((i) => i !== item)
      : [...current, item];

    const newData = { [field]: updated };
    // Auto-derive contraindication flags
    const fullData = { ...data, ...newData };
    newData.contraindication_flags = deriveContraindicationFlags(fullData);
    onUpdate(newData);
  };

  const addCustomSurgery = () => {
    if (customSurgery.trim()) {
      const updated = [...(data.past_surgeries || []), customSurgery.trim()];
      const newData = { past_surgeries: updated };
      const fullData = { ...data, ...newData };
      newData.contraindication_flags = deriveContraindicationFlags(fullData);
      onUpdate(newData);
      setCustomSurgery("");
    }
  };

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-danger-500/20 mb-3">
          <span className="text-2xl">🩺</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Medical History</h2>
        <p className="text-slate-400 text-sm mt-1">
          This helps us filter unsafe exercises for you
        </p>
      </div>

      {/* Privacy Notice */}
      <div className="glass-card p-3 flex items-center gap-3 text-xs text-slate-400">
        <span className="text-lg">🔒</span>
        <p>Your medical data is encrypted and never shared. It&apos;s only used to personalize your workout safety.</p>
      </div>

      {/* Pain Areas */}
      <div>
        <label className="input-label">Areas of Pain or Discomfort</label>
        <div className="grid grid-cols-3 gap-2">
          {PAIN_AREAS.map((area) => (
            <button
              key={area.id}
              type="button"
              onClick={() => toggleArrayItem("pain_areas", area.id)}
              className={`chip justify-center py-3 ${
                (data.pain_areas || []).includes(area.id) ? "selected" : ""
              }`}
            >
              <span>{area.icon}</span>
              <span>{area.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Past Surgeries */}
      <div>
        <label className="input-label">Past Surgeries</label>
        <div className="flex flex-wrap gap-2 mb-2">
          {SURGERY_OPTIONS.map((surgery) => (
            <button
              key={surgery}
              type="button"
              onClick={() => toggleArrayItem("past_surgeries", surgery)}
              className={`chip ${
                (data.past_surgeries || []).includes(surgery) ? "selected" : ""
              }`}
            >
              {surgery}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            className="input-field flex-1"
            placeholder="Add other surgery..."
            value={customSurgery}
            onChange={(e) => setCustomSurgery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addCustomSurgery())}
          />
          <button type="button" onClick={addCustomSurgery} className="btn-secondary px-4">
            Add
          </button>
        </div>
      </div>

      {/* Chronic Diseases */}
      <div>
        <label className="input-label">Chronic Conditions</label>
        <div className="flex flex-wrap gap-2">
          {CHRONIC_DISEASES.map((disease) => (
            <button
              key={disease}
              type="button"
              onClick={() => toggleArrayItem("chronic_diseases", disease)}
              className={`chip ${
                (data.chronic_diseases || []).includes(disease) ? "selected" : ""
              }`}
            >
              {disease}
            </button>
          ))}
        </div>
      </div>

      {/* Notes */}
      <div>
        <label className="input-label" htmlFor="medicalNotes">Additional Notes</label>
        <textarea
          id="medicalNotes"
          className="input-field resize-none"
          rows={3}
          placeholder="Any other medical conditions or concerns..."
          value={data.notes || ""}
          onChange={(e) => onUpdate({ notes: e.target.value })}
        />
      </div>

      {/* Derived Flags Preview */}
      {(data.contraindication_flags || []).length > 0 && (
        <div className="glass-card p-3 animate-fade-in">
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Safety Filters Active</p>
          <div className="flex flex-wrap gap-1.5">
            {data.contraindication_flags.map((flag) => (
              <span key={flag} className="px-2 py-1 rounded-full bg-danger-500/15 text-danger-400 text-[11px] font-medium">
                {flag.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
