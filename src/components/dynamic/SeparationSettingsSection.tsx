import React from 'react';

export interface SeparationSettingsSectionProps {
  /**
   * Current separation mode
   */
  mode: 'traditional' | 'sam-audio';
  
  /**
   * Text prompts for SAM Audio mode
   */
  prompts?: string;
  
  /**
   * Callback when prompts change
   */
  onPromptsChange?: (prompts: string) => void;
  
  /**
   * Selected preset
   */
  preset?: string;
  
  /**
   * Callback when preset changes
   */
  onPresetChange?: (preset: string) => void;
  
  /**
   * Model quality selection
   */
  quality?: 'fast' | 'balanced' | 'high';
  
  /**
   * Callback when quality changes
   */
  onQualityChange?: (quality: 'fast' | 'balanced' | 'high') => void;
}

const PRESETS: Record<string, string> = {
  custom: '',
  'standard-band': 'lead vocals, electric guitar, bass guitar, drums',
  'vocal-focus': 'lead vocals, background vocals, instrumental accompaniment',
  'jazz-ensemble': 'saxophone, piano, upright bass, drums',
  'orchestra': 'string section, brass section, woodwinds, percussion',
  'nature-sounds': 'bird chirping, water flowing, wind, leaves rustling',
  'urban-environment': 'traffic, footsteps, talking, doors',
  'interview': 'host voice, guest voice, background music',
  'concert': 'lead vocals, instruments, crowd applause, crowd noise',
};

const PRESET_LABELS: Record<string, string> = {
  custom: 'Custom...',
  'standard-band': 'Standard Band',
  'vocal-focus': 'Vocal Focus',
  'jazz-ensemble': 'Jazz Ensemble',
  'orchestra': 'Orchestra',
  'nature-sounds': 'Nature Sounds',
  'urban-environment': 'Urban Environment',
  'interview': 'Interview',
  'concert': 'Concert',
};

/**
 * Separation Settings section - SAM Audio configuration
 */
export function SeparationSettingsSection(props: SeparationSettingsSectionProps): React.JSX.Element {
  const { mode, prompts = '', onPromptsChange, preset = 'custom', onPresetChange, quality = 'balanced', onQualityChange } = props;
  
  const handlePresetChange = (event: React.ChangeEvent<HTMLSelectElement>): void => {
    const selectedPreset = event.target.value;
    onPresetChange?.(selectedPreset);
    
    // Auto-fill prompts based on preset
    if (selectedPreset !== 'custom' && PRESETS[selectedPreset]) {
      onPromptsChange?.(PRESETS[selectedPreset]);
    }
  };
  
  if (mode !== 'sam-audio') {
    return (
      <div className="text-center py-8 text-gray-500">
        Switch to SAM Audio mode to configure advanced separation settings
      </div>
    );
  }
  
  return (
    <div className="space-y-4">
      {/* Preset Templates */}
      <div>
        <label htmlFor="preset-select" className="block text-sm font-medium text-gray-300 mb-2">
          Preset Templates
        </label>
        <select
          id="preset-select"
          value={preset}
          onChange={handlePresetChange}
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {Object.entries(PRESET_LABELS).map(([value, label]) => (
            <option key={value} value={value} className="bg-gray-800">
              {label}
            </option>
          ))}
        </select>
      </div>
      
      {/* Text Prompts Input */}
      <div>
        <label htmlFor="prompts-input" className="block text-sm font-medium text-gray-300 mb-2">
          Text Prompts (comma-separated)
        </label>
        <textarea
          id="prompts-input"
          value={prompts}
          onChange={(e) => onPromptsChange?.(e.target.value)}
          placeholder="e.g., lead vocals, electric guitar, bass line, drum beat"
          rows={4}
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
        <p className="text-xs text-gray-500 mt-1">
          {prompts.length} characters • {prompts.split(',').filter(p => p.trim()).length} prompts
        </p>
      </div>
      
      {/* Model Quality Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Model Quality
        </label>
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={() => onQualityChange?.('fast')}
            className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
              quality === 'fast'
                ? 'bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 text-white shadow-isolo'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-isolo-orange-600/20'
            }`}
          >
            <div className="text-lg mb-1">⚡</div>
            <div className="text-sm">Fast</div>
          </button>
          <button
            onClick={() => onQualityChange?.('balanced')}
            className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
              quality === 'balanced'
                ? 'bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 text-white shadow-isolo'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-isolo-orange-600/20'
            }`}
          >
            <div className="text-lg mb-1">⚖️</div>
            <div className="text-sm">Balanced</div>
          </button>
          <button
            onClick={() => onQualityChange?.('high')}
            className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
              quality === 'high'
                ? 'bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 text-white shadow-isolo'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-isolo-orange-600/20'
            }`}
          >
            <div className="text-lg mb-1">✓✓✓</div>
            <div className="text-sm">High Quality</div>
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          {quality === 'fast' && '⚡ Fastest processing • ~2 GB VRAM • Good quality'}
          {quality === 'balanced' && '⚖️ Medium processing • ~4 GB VRAM • Better quality'}
          {quality === 'high' && '🐌 Slower processing • ~8 GB VRAM • Best quality'}
        </div>
      </div>
    </div>
  );
}
