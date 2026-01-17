import React from 'react';

export interface SlicingSettingsSectionProps {
  /**
   * Loop type selection
   */
  loopType?: '1-bar' | '2-bar' | '4-bar' | 'one-shots';
  
  /**
   * Callback when loop type changes
   */
  onLoopTypeChange?: (loopType: '1-bar' | '2-bar' | '4-bar' | 'one-shots') => void;
  
  /**
   * One-shot sensitivity (0-100)
   */
  oneShotSensitivity?: number;
  
  /**
   * Callback when one-shot sensitivity changes
   */
  onOneShotSensitivityChange?: (sensitivity: number) => void;
  
  /**
   * Loop crossfade in milliseconds
   */
  loopCrossfade?: number;
  
  /**
   * Callback when loop crossfade changes
   */
  onLoopCrossfadeChange?: (crossfade: number) => void;
}

/**
 * Global Slicing Settings section
 */
export function SlicingSettingsSection(props: SlicingSettingsSectionProps): React.JSX.Element {
  const {
    loopType = '4-bar',
    onLoopTypeChange,
    oneShotSensitivity = 50,
    onOneShotSensitivityChange,
    loopCrossfade = 10,
    onLoopCrossfadeChange
  } = props;
  
  return (
    <div className="space-y-4">
      {/* Loop Type */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Loop Type
        </label>
        <div className="grid grid-cols-4 gap-2">
          {(['1-bar', '2-bar', '4-bar', 'one-shots'] as const).map((type) => (
            <button
              key={type}
              onClick={() => onLoopTypeChange?.(type)}
              className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                loopType === type
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                  : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-white/10'
              }`}
            >
              {type === 'one-shots' ? 'One-Shots' : type.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
      
      {/* One-Shot Sensitivity */}
      <div>
        <label htmlFor="oneshot-sensitivity" className="block text-sm font-medium text-gray-300 mb-2">
          One-Shot Sensitivity: {oneShotSensitivity}%
        </label>
        <input
          id="oneshot-sensitivity"
          type="range"
          value={oneShotSensitivity}
          onChange={(e) => onOneShotSensitivityChange?.(Number(e.target.value))}
          min={0}
          max={100}
          step={1}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-purple-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Less sensitive</span>
          <span>More sensitive</span>
        </div>
      </div>
      
      {/* Loop Crossfade */}
      <div>
        <label htmlFor="loop-crossfade" className="block text-sm font-medium text-gray-300 mb-2">
          Loop Crossfade: {loopCrossfade}ms
        </label>
        <input
          id="loop-crossfade"
          type="range"
          value={loopCrossfade}
          onChange={(e) => onLoopCrossfadeChange?.(Number(e.target.value))}
          min={0}
          max={100}
          step={5}
          className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-blue-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>0ms</span>
          <span>50ms</span>
          <span>100ms</span>
        </div>
      </div>
    </div>
  );
}
