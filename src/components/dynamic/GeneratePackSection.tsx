import React from 'react';

export interface ExportOptions {
  includeIsolatedSounds: boolean;
  includeTraditionalStems: boolean;
  includeMidi: boolean;
  includeSlicedLoops: boolean;
  includeDocumentation: boolean;
}

export interface GeneratePackSectionProps {
  /**
   * Callback when generate pack is clicked
   */
  onGeneratePack?: () => void;
  
  /**
   * Whether processing is in progress
   */
  isProcessing?: boolean;
  
  /**
   * Export options
   */
  exportOptions?: ExportOptions;
  
  /**
   * Callback when export options change
   */
  onExportOptionsChange?: (options: ExportOptions) => void;
}

/**
 * Generate Pack section for final export
 */
export function GeneratePackSection(props: GeneratePackSectionProps): React.JSX.Element {
  const { 
    onGeneratePack, 
    isProcessing = false,
    exportOptions = {
      includeIsolatedSounds: true,
      includeTraditionalStems: true,
      includeMidi: true,
      includeSlicedLoops: true,
      includeDocumentation: true,
    },
    onExportOptionsChange
  } = props;
  
  const handleOptionChange = (option: string, value: boolean): void => {
    const newOptions: ExportOptions = {
      ...exportOptions,
      [option]: value,
    };
    onExportOptionsChange?.(newOptions);
  };
  
  return (
    <div className="space-y-4">
      {/* Export Options */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300 mb-3">
          Export Options
        </label>
        
        {[
          { key: 'includeIsolatedSounds', label: 'Include Isolated Sounds', icon: '🎵' },
          { key: 'includeTraditionalStems', label: 'Include Traditional Stems', icon: '🎼' },
          { key: 'includeMidi', label: 'Include MIDI Files', icon: '🎹' },
          { key: 'includeSlicedLoops', label: 'Include Sliced Loops', icon: '🔪' },
          { key: 'includeDocumentation', label: 'Include Documentation', icon: '📄' },
        ].map(({ key, label, icon }) => (
          <label
            key={key}
            className="flex items-center justify-between cursor-pointer bg-white/5 border border-isolo-orange-600/20 rounded-lg px-4 py-3 hover:bg-white/10 hover:border-isolo-orange-500/30 transition-colors"
          >
            <span className="text-sm text-gray-300 flex items-center gap-2">
              <span>{icon}</span>
              {label}
            </span>
            <input
              type="checkbox"
              checked={exportOptions[key as keyof typeof exportOptions]}
              onChange={(e) => {
                handleOptionChange(key, e.target.checked);
              }}
              className="w-5 h-5 rounded border-isolo-orange-600/20 bg-white/5 text-isolo-orange-500 focus:ring-2 focus:ring-isolo-orange-500 focus:ring-offset-0"
            />
          </label>
        ))}
      </div>
      
      {/* Generate Pack Button */}
      <button
        onClick={onGeneratePack}
        disabled={isProcessing}
        className="w-full px-6 py-6 bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 hover:from-isolo-orange-500 hover:to-isolo-red-500 text-white rounded-lg font-bold text-xl transition-all duration-200 shadow-isolo hover:shadow-2xl hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-700 disabled:to-gray-800 disabled:hover:scale-100"
      >
        {isProcessing ? '⏳ Generating Pack...' : '📦 SLICE ALL & GENERATE PACK'}
      </button>
      
      {/* Info Message */}
      <div className="text-center text-sm text-gray-500">
        <p>All selected content will be packaged into a downloadable ZIP file</p>
      </div>
    </div>
  );
}
