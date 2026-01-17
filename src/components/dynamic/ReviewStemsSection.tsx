import React from 'react';

export interface StemData {
  /**
   * Name of the stem
   */
  name: string;
  
  /**
   * Audio data or URL
   */
  audioUrl?: string;
  
  /**
   * Number of slices generated
   */
  sliceCount?: number;
  
  /**
   * Whether MIDI was generated
   */
  hasMidi?: boolean;
}

export interface ReviewStemsSectionProps {
  /**
   * Array of stems to display
   */
  stems: StemData[];
  
  /**
   * Callback when a stem is selected for slicing
   */
  onSliceStem?: (stemName: string) => void;
  
  /**
   * Currently active stem tab
   */
  activeTab?: number;
  
  /**
   * Callback when tab changes
   */
  onTabChange?: (index: number) => void;
}

/**
 * Review Stems & Slices section with dynamic tabs
 */
export function ReviewStemsSection(props: ReviewStemsSectionProps): React.JSX.Element {
  const { stems, onSliceStem, activeTab = 0, onTabChange } = props;
  const [currentTab, setCurrentTab] = React.useState(activeTab);
  
  const handleTabChange = (index: number): void => {
    setCurrentTab(index);
    onTabChange?.(index);
  };
  
  if (stems.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="text-4xl mb-4">🎵</div>
        <p>No stems available yet. Upload and analyze audio to get started.</p>
      </div>
    );
  }
  
  const activeStem = stems[currentTab];
  
  if (!activeStem) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="text-4xl mb-4">🎵</div>
        <p>No stems available yet. Upload and analyze audio to get started.</p>
      </div>
    );
  }
  
  return (
    <div className="space-y-4">
      {/* Tab Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-white/10 pb-2">
        {stems.map((stem, index) => (
          <button
            key={index}
            onClick={() => {
              handleTabChange(index);
            }}
            className={`px-4 py-2 rounded-t-lg font-medium transition-all duration-200 ${
              currentTab === index
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            {stem.name}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <div className="space-y-4">
        {/* Waveform Preview Placeholder */}
        <div className="bg-white/5 border border-white/10 rounded-lg p-6">
          <div className="flex items-center justify-center h-32 text-gray-500">
            <div className="text-center">
              <div className="text-2xl mb-2">📊</div>
              <p className="text-sm">Waveform preview: {activeStem.name}</p>
            </div>
          </div>
        </div>
        
        {/* Audio Player Placeholder */}
        <div className="bg-white/5 border border-white/10 rounded-lg p-4">
          <div className="flex items-center gap-4">
            <button className="w-12 h-12 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center hover:shadow-lg transition-shadow">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </button>
            <div className="flex-1">
              <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500" style={{ width: '0%' }} />
              </div>
            </div>
            <span className="text-sm text-gray-400">0:00 / 0:00</span>
          </div>
        </div>
        
        {/* Stem Info */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white/5 border border-white/10 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Generated Slices</div>
            <div className="text-2xl font-semibold text-blue-400">
              {activeStem.sliceCount ?? 0}
            </div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">MIDI Generated</div>
            <div className="text-2xl font-semibold">
              {activeStem.hasMidi ? '✅' : '❌'}
            </div>
          </div>
        </div>
        
        {/* Slice Button */}
        <button
          onClick={() => onSliceStem?.(activeStem.name)}
          className="w-full px-6 py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-lg font-semibold transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          🔪 Slice This {activeStem.name}
        </button>
      </div>
    </div>
  );
}
