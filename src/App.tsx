import React from 'react';
import { SectionPanel } from './components/dynamic/SectionPanel';
import { UploadAnalyzeSection } from './components/dynamic/UploadAnalyzeSection';
import { SeparationSettingsSection } from './components/dynamic/SeparationSettingsSection';
import { MusicalSettingsSection } from './components/dynamic/MusicalSettingsSection';
import { SlicingSettingsSection } from './components/dynamic/SlicingSettingsSection';
import { FXSettingsSection } from './components/dynamic/FXSettingsSection';
import { ReviewStemsSection, StemData } from './components/dynamic/ReviewStemsSection';
import { GeneratePackSection, ExportOptions } from './components/dynamic/GeneratePackSection';

function App(): React.JSX.Element {
  // State for Upload & Analyze
  const [separationMode, setSeparationMode] = React.useState<'traditional' | 'sam-audio'>('traditional');
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  
  // State for Separation Settings
  const [prompts, setPrompts] = React.useState('');
  const [preset, setPreset] = React.useState('custom');
  const [quality, setQuality] = React.useState<'fast' | 'balanced' | 'high'>('balanced');
  
  // State for Musical Settings
  const [bpm, setBpm] = React.useState(120);
  const [detectedKey, setDetectedKey] = React.useState('Not detected');
  const [harmonicRecs, setHarmonicRecs] = React.useState<string[]>([]);
  const [transpose, setTranspose] = React.useState(0);
  const [timeSignature, setTimeSignature] = React.useState('4/4');
  
  // State for Slicing Settings
  const [loopType, setLoopType] = React.useState<'1-bar' | '2-bar' | '4-bar' | 'one-shots'>('4-bar');
  const [oneShotSensitivity, setOneShotSensitivity] = React.useState(50);
  const [loopCrossfade, setLoopCrossfade] = React.useState(10);
  
  // State for FX Settings
  const [normalizePeak, setNormalizePeak] = React.useState(-1);
  const [lfoPanLevel, setLfoPanLevel] = React.useState(0);
  const [lfoFilter, setLfoFilter] = React.useState(0);
  const [oneShotShaping, setOneShotShaping] = React.useState(false);
  
  // State for Review Stems
  const [stems, setStems] = React.useState<StemData[]>([]);
  
  // State for Export Options
  const [exportOptions, setExportOptions] = React.useState<ExportOptions>({
    includeIsolatedSounds: true,
    includeTraditionalStems: true,
    includeMidi: true,
    includeSlicedLoops: true,
    includeDocumentation: true,
  });
  
  // Handlers
  const handleFileSelect = (file: File): void => {
    setSelectedFile(file);
    console.log('File selected:', file.name);
  };
  
  const handleAnalyze = (): void => {
    if (!selectedFile) return;
    
    setIsProcessing(true);
    console.log('Analyzing file:', selectedFile.name);
    
    // Simulate processing
    setTimeout(() => {
      // Mock data based on mode
      if (separationMode === 'traditional') {
        setStems([
          { name: 'Vocals', sliceCount: 24, hasMidi: true },
          { name: 'Drums', sliceCount: 32, hasMidi: false },
          { name: 'Bass', sliceCount: 16, hasMidi: true },
          { name: 'Other', sliceCount: 28, hasMidi: false },
          { name: 'Guitar', sliceCount: 20, hasMidi: true },
          { name: 'Piano', sliceCount: 18, hasMidi: true },
        ]);
      } else {
        // SAM Audio mode - dynamic based on prompts
        const promptList = prompts.split(',').map(p => p.trim()).filter(p => p);
        setStems(promptList.map(prompt => ({
          name: prompt.charAt(0).toUpperCase() + prompt.slice(1),
          sliceCount: Math.floor(Math.random() * 20) + 10,
          hasMidi: Math.random() > 0.5,
        })));
      }
      
      // Mock detected values
      setBpm(128);
      setDetectedKey('C Major');
      setHarmonicRecs(['A Minor', 'F Major', 'G Major']);
      
      setIsProcessing(false);
    }, 2000);
  };
  
  const handleSliceStem = (stemName: string): void => {
    console.log('Slicing stem:', stemName);
  };
  
  const handleGeneratePack = (): void => {
    console.log('Generating pack with options:', exportOptions);
  };
  
  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
            🎵 Loop Architect
          </h1>
          <p className="text-xl text-gray-400 font-light">
            Pro Edition
          </p>
        </header>
        
        {/* Main Content */}
        <div className="space-y-4">
          {/* Section 1: Upload & Analyze */}
          <SectionPanel title="1. Upload & Analyze" subtitle="Select your audio file and separation mode">
            <UploadAnalyzeSection
              onFileSelect={handleFileSelect}
              separationMode={separationMode}
              onModeChange={setSeparationMode}
              onAnalyze={handleAnalyze}
              isProcessing={isProcessing}
            />
          </SectionPanel>
          
          {/* Section 2: Separation Settings */}
          <SectionPanel 
            title="2. Separation Settings" 
            subtitle="Configure SAM Audio options"
            collapsible
            defaultCollapsed={separationMode !== 'sam-audio'}
          >
            <SeparationSettingsSection
              mode={separationMode}
              prompts={prompts}
              onPromptsChange={setPrompts}
              preset={preset}
              onPresetChange={setPreset}
              quality={quality}
              onQualityChange={setQuality}
            />
          </SectionPanel>
          
          {/* Section 3: Global Musical Settings */}
          <SectionPanel 
            title="3. Global Musical Settings" 
            subtitle="BPM, key, and harmonic analysis"
            collapsible
            defaultCollapsed
          >
            <MusicalSettingsSection
              bpm={bpm}
              onBpmChange={setBpm}
              detectedKey={detectedKey}
              harmonicRecs={harmonicRecs}
              transpose={transpose}
              onTransposeChange={setTranspose}
              timeSignature={timeSignature}
              onTimeSignatureChange={setTimeSignature}
            />
          </SectionPanel>
          
          {/* Section 4: Global Slicing Settings */}
          <SectionPanel 
            title="4. Global Slicing Settings" 
            subtitle="Loop type and slicing parameters"
            collapsible
            defaultCollapsed
          >
            <SlicingSettingsSection
              loopType={loopType}
              onLoopTypeChange={setLoopType}
              oneShotSensitivity={oneShotSensitivity}
              onOneShotSensitivityChange={setOneShotSensitivity}
              loopCrossfade={loopCrossfade}
              onLoopCrossfadeChange={setLoopCrossfade}
            />
          </SectionPanel>
          
          {/* Section 5: Global FX Settings */}
          <SectionPanel 
            title="5. Global FX Settings" 
            subtitle="Normalization and effects processing"
            collapsible
            defaultCollapsed
          >
            <FXSettingsSection
              normalizePeak={normalizePeak}
              onNormalizePeakChange={setNormalizePeak}
              lfoPanLevel={lfoPanLevel}
              onLfoPanLevelChange={setLfoPanLevel}
              lfoFilter={lfoFilter}
              onLfoFilterChange={setLfoFilter}
              oneShotShaping={oneShotShaping}
              onOneShotShapingChange={setOneShotShaping}
            />
          </SectionPanel>
          
          {/* Section 6: Review Stems & Slices */}
          <SectionPanel 
            title="6. Review Stems & Slices" 
            subtitle="Preview and manage isolated audio"
          >
            <ReviewStemsSection
              stems={stems}
              onSliceStem={handleSliceStem}
            />
          </SectionPanel>
          
          {/* Section 7: Generate Pack */}
          <SectionPanel 
            title="7. Generate Pack" 
            subtitle="Export your processed audio"
          >
            <GeneratePackSection
              onGeneratePack={handleGeneratePack}
              isProcessing={isProcessing}
              exportOptions={exportOptions}
              onExportOptionsChange={setExportOptions}
            />
          </SectionPanel>
        </div>
        
        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>Loop Architect Pro Edition • Powered by SAM Audio</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
