"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import DemographicsStep from "@/components/OnboardingSteps/DemographicsStep";
import MedicalHistoryStep from "@/components/OnboardingSteps/MedicalHistoryStep";
import FitnessExperienceStep from "@/components/OnboardingSteps/FitnessExperienceStep";
import EquipmentStep from "@/components/OnboardingSteps/EquipmentStep";
import ScheduleStep from "@/components/OnboardingSteps/ScheduleStep";
import { createProfile, saveMedicalHistory, generatePlan } from "@/lib/api";

const STEPS = [
  { id: "demographics", label: "About You", icon: "📋" },
  { id: "medical", label: "Medical", icon: "🩺" },
  { id: "fitness", label: "Fitness Level", icon: "🏋️" },
  { id: "equipment", label: "Equipment", icon: "🏠" },
  { id: "schedule", label: "Schedule", icon: "📅" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Profile data
  const [profile, setProfile] = useState({
    age: "",
    height_cm: "",
    weight_kg: "",
    fitness_experience: "beginner",
    time_since_last_workout_days: 0,
    available_equipment: [],
    training_environment: "home",
    weekly_frequency: 3,
    preferred_workout_days: [],
    preferred_time: "morning",
    resting_heart_rate: null,
    daily_step_count: null,
    body_fat_percentage: null,
  });

  // Medical data
  const [medical, setMedical] = useState({
    past_surgeries: [],
    transplants: [],
    chronic_diseases: [],
    pain_areas: [],
    contraindication_flags: [],
    notes: "",
  });

  const updateProfile = (updates) => setProfile((prev) => ({ ...prev, ...updates }));
  const updateMedical = (updates) => setMedical((prev) => ({ ...prev, ...updates }));

  const canProceed = () => {
    switch (currentStep) {
      case 0: return profile.age && profile.height_cm && profile.weight_kg;
      case 1: return true; // Medical history is optional
      case 2: return !!profile.fitness_experience;
      case 3: return true; // Equipment is optional (bodyweight always included)
      case 4: return profile.weekly_frequency >= 1;
      default: return false;
    }
  };

  const handleNext = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleComplete = async () => {
    setSaving(true);
    setError("");

    try {
      // 1. Create profile
      await createProfile(profile);

      // 2. Save medical history
      await saveMedicalHistory(medical);

      // 3. Generate initial workout plan
      await generatePlan({ duration_days: 30 });

      // 4. Navigate to dashboard
      router.push("/dashboard");
    } catch (err) {
      console.error("Onboarding error:", err);
      setError(
        err.response?.data?.detail ||
        "Failed to save your profile. Please try again."
      );
      setSaving(false);
    }
  };

  const isLastStep = currentStep === STEPS.length - 1;

  return (
    <main className="flex-1 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-lg relative z-10">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            {STEPS.map((step, idx) => (
              <div key={step.id} className="flex items-center">
                <div
                  className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-300 ${
                    idx < currentStep
                      ? "bg-primary-600 text-white"
                      : idx === currentStep
                      ? "bg-primary-600/20 border-2 border-primary-500 text-primary-400"
                      : "bg-white/5 text-slate-600 border border-white/10"
                  }`}
                >
                  {idx < currentStep ? (
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <span className="text-xs">{step.icon}</span>
                  )}
                </div>
                {idx < STEPS.length - 1 && (
                  <div className={`w-8 sm:w-16 h-0.5 mx-1 transition-all duration-300 ${
                    idx < currentStep ? "bg-primary-600" : "bg-white/10"
                  }`} />
                )}
              </div>
            ))}
          </div>
          <p className="text-center text-sm text-slate-500">
            Step {currentStep + 1} of {STEPS.length} — <span className="text-slate-300">{STEPS[currentStep].label}</span>
          </p>
        </div>

        {/* Step Content */}
        <div className="glass-card p-6 sm:p-8 min-h-[400px]">
          {currentStep === 0 && (
            <DemographicsStep data={profile} onUpdate={updateProfile} />
          )}
          {currentStep === 1 && (
            <MedicalHistoryStep data={medical} onUpdate={updateMedical} />
          )}
          {currentStep === 2 && (
            <FitnessExperienceStep data={profile} onUpdate={updateProfile} />
          )}
          {currentStep === 3 && (
            <EquipmentStep data={profile} onUpdate={updateProfile} />
          )}
          {currentStep === 4 && (
            <ScheduleStep data={profile} onUpdate={updateProfile} />
          )}

          {/* Error */}
          {error && (
            <div className="mt-4 p-3 rounded-lg bg-danger-500/10 border border-danger-500/20 text-danger-400 text-sm animate-fade-in">
              {error}
            </div>
          )}

          {/* Navigation */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/5">
            <button
              type="button"
              onClick={handleBack}
              disabled={currentStep === 0}
              className="btn-secondary disabled:opacity-30 disabled:cursor-not-allowed"
            >
              ← Back
            </button>

            {isLastStep ? (
              <button
                type="button"
                onClick={handleComplete}
                disabled={!canProceed() || saving}
                className="btn-primary flex items-center gap-2"
              >
                {saving ? (
                  <>
                    <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Generating Plan...
                  </>
                ) : (
                  "Generate My Plan 🚀"
                )}
              </button>
            ) : (
              <button
                type="button"
                onClick={handleNext}
                disabled={!canProceed()}
                className="btn-primary"
              >
                Next →
              </button>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
