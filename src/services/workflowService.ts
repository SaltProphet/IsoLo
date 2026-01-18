/**
 * Workflow Service for IsoLo
 * 
 * This service provides TypeScript interfaces for the workflow orchestrator
 * and handles communication with the backend workflow system.
 */

/**
 * Workflow configuration matching Python WorkflowConfig
 */
export interface WorkflowConfig {
  separationMode: 'traditional' | 'sam-audio';
  samPrompts?: string[];
  manualBpm?: number;
  transposeSemitones: number;
  timeSignature: string;
  loopType: '1-bar' | '2-bar' | '4-bar' | 'one-shots';
  oneShotSensitivity: number;
  crossfadeMs: number;
  normalizePeak: number;
  applyModulation: boolean;
  modulationRate: string;
  panDepth: number;
  levelDepth: number;
  filterType: string;
  filterFreq: number;
  filterDepth: number;
  attackGain: number;
  sustainGain: number;
  includeInstrumental: boolean;
  includeMidi: boolean;
  includeLyrics: boolean;
  includeVisualizer: boolean;
  includeVideo: boolean;
  packName: string;
  artistName?: string;
  description?: string;
}

/**
 * Workflow status tracking
 */
export interface WorkflowStatus {
  currentStep: string;
  currentStepIndex: number;
  totalSteps: number;
  progressPercent: number;
  statusMessage: string;
  isComplete: boolean;
  hasError: boolean;
  errorMessage?: string;
}

/**
 * Workflow execution result
 */
export interface WorkflowResult {
  success: boolean;
  outputZip?: string;
  error?: string;
  stepsCompleted: string[];
  stepsFailed: string[];
  executionTime: number;
  generatedFiles: string[];
}

/**
 * Workflow step definition
 */
export interface WorkflowStep {
  name: string;
  description: string;
  isRequired: boolean;
  isStub: boolean;
}

/**
 * All workflow steps in order
 */
export const WORKFLOW_STEPS: WorkflowStep[] = [
  {
    name: 'Input Handler',
    description: 'Validate and prepare audio file',
    isRequired: true,
    isStub: false,
  },
  {
    name: 'Audio Analyzer',
    description: 'Detect BPM, key, and time signature',
    isRequired: true,
    isStub: false,
  },
  {
    name: 'Instrumental Builder',
    description: 'Mix non-vocal stems',
    isRequired: false,
    isStub: false,
  },
  {
    name: 'Audio Slicer',
    description: 'Generate loops and one-shots',
    isRequired: true,
    isStub: false,
  },
  {
    name: 'Lyric Extractor',
    description: 'Extract timestamped lyrics (Stub)',
    isRequired: false,
    isStub: true,
  },
  {
    name: 'Visualizer Generator',
    description: 'Create audio visualizations (Stub)',
    isRequired: false,
    isStub: true,
  },
  {
    name: 'Video Composer',
    description: 'Render video with visuals (Stub)',
    isRequired: false,
    isStub: true,
  },
  {
    name: 'Metadata Tagger',
    description: 'Tag files with BPM/key',
    isRequired: false,
    isStub: false,
  },
  {
    name: 'Pack Builder',
    description: 'Organize files into structure',
    isRequired: true,
    isStub: false,
  },
  {
    name: 'Pack Exporter',
    description: 'Create final ZIP package',
    isRequired: true,
    isStub: false,
  },
];

/**
 * Workflow Service class
 */
export class WorkflowService {
  /**
   * Base URL for backend API (reserved for future HTTP communication)
   * @private
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  private readonly baseUrl: string;
  
  constructor(baseUrl: string = 'http://localhost:7860') {
    this.baseUrl = baseUrl;
  }
  
  /**
   * Get the backend base URL (for future use)
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }
  
  /**
   * Get workflow step information
   */
  getSteps(): WorkflowStep[] {
    return WORKFLOW_STEPS;
  }
  
  /**
   * Get count of required steps
   */
  getRequiredStepCount(): number {
    return WORKFLOW_STEPS.filter(step => step.isRequired).length;
  }
  
  /**
   * Get count of stub steps
   */
  getStubStepCount(): number {
    return WORKFLOW_STEPS.filter(step => step.isStub).length;
  }
  
  /**
   * Calculate progress percentage from step index
   */
  calculateProgress(currentStepIndex: number, totalSteps: number): number {
    if (totalSteps === 0) return 0;
    return (currentStepIndex / totalSteps) * 100;
  }
  
  /**
   * Format execution time
   */
  formatExecutionTime(seconds: number): string {
    const secondsStr = seconds.toFixed(1);
    if (seconds < 60) {
      return `${secondsStr}s`;
    }
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes.toString()}m ${secs.toString()}s`;
  }
  
  /**
   * Get step status emoji
   */
  getStepStatusEmoji(status: 'pending' | 'running' | 'complete' | 'failed' | 'skipped'): string {
    const emojiMap = {
      pending: '⏳',
      running: '🔄',
      complete: '✅',
      failed: '❌',
      skipped: '⏭️',
    };
    return emojiMap[status];
  }
  
  /**
   * Validate workflow configuration
   */
  validateConfig(config: WorkflowConfig): string[] {
    const errors: string[] = [];
    
    if (!config.packName || config.packName.trim() === '') {
      errors.push('Pack name is required');
    }
    
    if (config.transposeSemitones < -12 || config.transposeSemitones > 12) {
      errors.push('Transpose must be between -12 and 12 semitones');
    }
    
    if (config.oneShotSensitivity < 0 || config.oneShotSensitivity > 1) {
      errors.push('One-shot sensitivity must be between 0 and 1');
    }
    
    if (config.separationMode === 'sam-audio' && (!config.samPrompts || config.samPrompts.length === 0)) {
      errors.push('SAM Audio mode requires at least one prompt');
    }
    
    return errors;
  }
  
  /**
   * Create default workflow configuration
   */
  createDefaultConfig(): WorkflowConfig {
    return {
      separationMode: 'traditional',
      transposeSemitones: 0,
      timeSignature: '4/4',
      loopType: '4-bar',
      oneShotSensitivity: 0.5,
      crossfadeMs: 10,
      normalizePeak: -1.0,
      applyModulation: false,
      modulationRate: '1/4',
      panDepth: 0,
      levelDepth: 0,
      filterType: 'None',
      filterFreq: 5000,
      filterDepth: 0,
      attackGain: 0,
      sustainGain: 0,
      includeInstrumental: true,
      includeMidi: true,
      includeLyrics: false,
      includeVisualizer: false,
      includeVideo: false,
      packName: 'IsoLo_Pack',
    };
  }
}

/**
 * Create a singleton instance
 */
export const workflowService = new WorkflowService();
