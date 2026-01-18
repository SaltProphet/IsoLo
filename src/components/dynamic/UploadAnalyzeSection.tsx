import React from 'react';

export interface UploadAnalyzeSectionProps {
  /**
   * Callback when file is selected
   */
  onFileSelect?: (file: File) => void;
  
  /**
   * Current separation mode
   */
  separationMode: 'traditional' | 'sam-audio';
  
  /**
   * Callback when separation mode changes
   */
  onModeChange: (mode: 'traditional' | 'sam-audio') => void;
  
  /**
   * Callback when analyze button is clicked
   */
  onAnalyze?: () => void;
  
  /**
   * Whether processing is in progress
   */
  isProcessing?: boolean;
}

/**
 * Upload & Analyze section component.
 * Allows users to upload audio files and choose separation mode.
 */
export function UploadAnalyzeSection(props: UploadAnalyzeSectionProps): React.JSX.Element {
  const { onFileSelect, separationMode, onModeChange, onAnalyze, isProcessing = false } = props;
  const [selectedFileName, setSelectedFileName] = React.useState<string>('');
  const fileInputRef = React.useRef<HTMLInputElement>(null);
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFileName(file.name);
      onFileSelect?.(file);
    }
  };
  
  const handleUploadClick = (): void => {
    fileInputRef.current?.click();
  };
  
  return (
    <div className="space-y-4">
      {/* File Upload */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Upload Song
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          className="hidden"
          aria-label="Upload audio file"
        />
        <button
          onClick={handleUploadClick}
          className="w-full px-4 py-3 bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 hover:from-isolo-orange-500 hover:to-isolo-red-500 text-white rounded-lg font-medium transition-all duration-200 shadow-isolo hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isProcessing}
        >
          {selectedFileName ? `Selected: ${selectedFileName}` : '📁 Choose Audio File'}
        </button>
      </div>
      
      {/* Separation Mode Toggle */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Separation Mode
        </label>
        <div className="flex gap-2">
          <button
            onClick={() => {
              onModeChange('traditional');
            }}
            className={`flex-1 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
              separationMode === 'traditional'
                ? 'bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 text-white shadow-isolo'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-isolo-orange-600/20'
            }`}
            disabled={isProcessing}
          >
            Traditional Stems
          </button>
          <button
            onClick={() => {
              onModeChange('sam-audio');
            }}
            className={`flex-1 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
              separationMode === 'sam-audio'
                ? 'bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 text-white shadow-isolo'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 border border-isolo-orange-600/20'
            }`}
            disabled={isProcessing}
          >
            SAM Audio
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {separationMode === 'traditional' 
            ? 'Fixed categories: vocals, drums, bass, other, guitar, piano'
            : 'Flexible sound isolation using text descriptions'}
        </p>
      </div>
      
      {/* Analyze Button */}
      <button
        onClick={onAnalyze}
        disabled={!selectedFileName || isProcessing}
        className="w-full px-6 py-4 bg-gradient-to-r from-isolo-orange-600 to-isolo-red-600 hover:from-isolo-orange-500 hover:to-isolo-red-500 text-white rounded-lg font-semibold text-lg transition-all duration-200 shadow-isolo hover:shadow-2xl hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-700 disabled:to-gray-800 disabled:hover:scale-100"
      >
        {isProcessing ? '⏳ Processing...' : '🎵 Separate Stems & Analyze'}
      </button>
    </div>
  );
}
