import React from 'react';

export interface FXSettingsSectionProps {
  /**
   * Normalize peak level in dBFS
   */
  normalizePeak?: number;
  
  /**
   * Callback when normalize peak changes
   */
  onNormalizePeakChange?: (peak: number) => void;
  
  /**
   * LFO modulation for pan/level (0-100)
   */
  lfoPanLevel?: number;
  
  /**
   * Callback when LFO pan/level changes
   */
  onLfoPanLevelChange?: (value: number) => void;
  
  /**
   * LFO modulation for filter (0-100)
   */
  lfoFilter?: number;
  
  /**
   * Callback when LFO filter changes
   */
  onLfoFilterChange?: (value: number) => void;
  
  /**
   * One-shot shaping enabled
   */
  oneShotShaping?: boolean;
  
  /**
   * Callback when one-shot shaping changes
   */
  onOneShotShapingChange?: (enabled: boolean) => void;
}

/**
 * Global FX Settings section
 */
export function FXSettingsSection(props: FXSettingsSectionProps): React.JSX.Element {
  const {
    normalizePeak = -1,
    onNormalizePeakChange,
    lfoPanLevel = 0,
    onLfoPanLevelChange,
    lfoFilter = 0,
    onLfoFilterChange,
    oneShotShaping = false,
    onOneShotShapingChange
  } = props;
  
  return (
    <div className="space-y-4">
      {/* Normalize Peak */}
      <div>
        <label htmlFor="normalize-peak" className="block text-sm font-medium text-gray-300 mb-2">
          Normalize Peak: {normalizePeak} dBFS
        </label>
        <input
          id="normalize-peak"
          type="range"
          value={normalizePeak}
          onChange={(e) => onNormalizePeakChange?.(Number(e.target.value))}
          min={-12}
          max={0}
          step={0.5}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-green-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>-12 dB</span>
          <span>-6 dB</span>
          <span>0 dB</span>
        </div>
      </div>
      
      {/* LFO Pan/Level Modulation */}
      <div>
        <label htmlFor="lfo-pan-level" className="block text-sm font-medium text-gray-300 mb-2">
          LFO Modulation (Pan/Level): {lfoPanLevel}%
        </label>
        <input
          id="lfo-pan-level"
          type="range"
          value={lfoPanLevel}
          onChange={(e) => onLfoPanLevelChange?.(Number(e.target.value))}
          min={0}
          max={100}
          step={1}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Off</span>
          <span>Moderate</span>
          <span>Max</span>
        </div>
      </div>
      
      {/* LFO Filter Modulation */}
      <div>
        <label htmlFor="lfo-filter" className="block text-sm font-medium text-gray-300 mb-2">
          LFO Modulation (Filter): {lfoFilter}%
        </label>
        <input
          id="lfo-filter"
          type="range"
          value={lfoFilter}
          onChange={(e) => onLfoFilterChange?.(Number(e.target.value))}
          min={0}
          max={100}
          step={1}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Off</span>
          <span>Moderate</span>
          <span>Max</span>
        </div>
      </div>
      
      {/* One-Shot Shaping */}
      <div>
        <label className="flex items-center justify-between cursor-pointer">
          <span className="text-sm font-medium text-gray-300">
            One-Shot Shaping
          </span>
          <button
            onClick={() => onOneShotShapingChange?.(!oneShotShaping)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
              oneShotShaping ? 'bg-blue-500' : 'bg-white/10'
            }`}
            role="switch"
            aria-checked={oneShotShaping}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                oneShotShaping ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </label>
        <p className="text-xs text-gray-500 mt-1">
          Apply envelope shaping to one-shot samples
        </p>
      </div>
    </div>
  );
}
