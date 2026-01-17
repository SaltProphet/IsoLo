import React from 'react';

export interface MusicalSettingsSectionProps {
  /**
   * BPM (Beats Per Minute)
   */
  bpm?: number;
  
  /**
   * Callback when BPM changes
   */
  onBpmChange?: (bpm: number) => void;
  
  /**
   * Detected musical key
   */
  detectedKey?: string;
  
  /**
   * Harmonic recommendations
   */
  harmonicRecs?: string[];
  
  /**
   * Transpose in semitones
   */
  transpose?: number;
  
  /**
   * Callback when transpose changes
   */
  onTransposeChange?: (transpose: number) => void;
  
  /**
   * Time signature
   */
  timeSignature?: string;
  
  /**
   * Callback when time signature changes
   */
  onTimeSignatureChange?: (timeSignature: string) => void;
}

/**
 * Global Musical Settings section
 */
export function MusicalSettingsSection(props: MusicalSettingsSectionProps): React.JSX.Element {
  const { 
    bpm = 120, 
    onBpmChange, 
    detectedKey = 'Not detected', 
    harmonicRecs = [], 
    transpose = 0, 
    onTransposeChange,
    timeSignature = '4/4',
    onTimeSignatureChange 
  } = props;
  
  return (
    <div className="space-y-4">
      {/* BPM */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="bpm-input" className="block text-sm font-medium text-gray-300 mb-2">
            BPM (Beats Per Minute)
          </label>
          <input
            id="bpm-input"
            type="number"
            value={bpm}
            onChange={(e) => onBpmChange?.(Number(e.target.value))}
            min={20}
            max={300}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">Auto-detected, editable</p>
        </div>
        
        <div>
          <label htmlFor="time-signature" className="block text-sm font-medium text-gray-300 mb-2">
            Time Signature
          </label>
          <select
            id="time-signature"
            value={timeSignature}
            onChange={(e) => onTimeSignatureChange?.(e.target.value)}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="4/4" className="bg-gray-800">4/4</option>
            <option value="3/4" className="bg-gray-800">3/4</option>
            <option value="6/8" className="bg-gray-800">6/8</option>
            <option value="5/4" className="bg-gray-800">5/4</option>
            <option value="7/8" className="bg-gray-800">7/8</option>
          </select>
        </div>
      </div>
      
      {/* Detected Key */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Detected Key
        </label>
        <div className="px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-200">
          {detectedKey}
        </div>
      </div>
      
      {/* Harmonic Recommendations */}
      {harmonicRecs.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Harmonic Recommendations
          </label>
          <div className="flex flex-wrap gap-2">
            {harmonicRecs.map((rec, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-sm text-blue-300"
              >
                {rec}
              </span>
            ))}
          </div>
        </div>
      )}
      
      {/* Transpose */}
      <div>
        <label htmlFor="transpose-input" className="block text-sm font-medium text-gray-300 mb-2">
          Transpose (Semitones): {transpose > 0 ? `+${String(transpose)}` : String(transpose)}
        </label>
        <input
          id="transpose-input"
          type="range"
          value={transpose}
          onChange={(e) => onTransposeChange?.(Number(e.target.value))}
          min={-12}
          max={12}
          step={1}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>-12</span>
          <span>0</span>
          <span>+12</span>
        </div>
      </div>
    </div>
  );
}
