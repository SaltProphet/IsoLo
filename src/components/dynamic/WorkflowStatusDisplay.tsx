import React from 'react';
import { workflowService, type WorkflowStatus, type WorkflowStep } from '../../services/workflowService';

export interface WorkflowStatusDisplayProps {
  status?: WorkflowStatus;
  showSteps?: boolean;
}

export function WorkflowStatusDisplay(props: WorkflowStatusDisplayProps): React.JSX.Element {
  const { status, showSteps = false } = props;
  const steps = workflowService.getSteps();
  
  if (!status) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <p className="text-gray-400">No workflow running</p>
      </div>
    );
  }
  
  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 space-y-4">
      {/* Progress Bar */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-300">
            {status.currentStep}
          </span>
          <span className="text-sm text-gray-400">
            {status.progressPercent.toFixed(0)}%
          </span>
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full transition-all duration-300 ${
              status.hasError 
                ? 'bg-red-500'
                : status.isComplete 
                  ? 'bg-green-500'
                  : 'bg-blue-500'
            }`}
            style={{ width: `${String(status.progressPercent)}%` }}
          ></div>
        </div>
        
        <p className="text-sm text-gray-400 mt-2">
          {status.statusMessage}
        </p>
      </div>
      
      {/* Status Badge */}
      <div className="flex items-center gap-2">
        {status.isComplete && (
          <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium">
            ✅ Complete
          </span>
        )}
        {status.hasError && (
          <span className="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm font-medium">
            ❌ Error
          </span>
        )}
        {!status.isComplete && !status.hasError && (
          <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm font-medium">
            🔄 Processing
          </span>
        )}
        
        <span className="text-sm text-gray-400">
          Step {status.currentStepIndex + 1} of {status.totalSteps}
        </span>
      </div>
      
      {/* Error Message */}
      {status.hasError && status.errorMessage && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
          <p className="text-sm text-red-400">
            {status.errorMessage}
          </p>
        </div>
      )}
      
      {/* Step List */}
      {showSteps && (
        <div className="space-y-2 mt-4 pt-4 border-t border-gray-700">
          <h4 className="text-sm font-medium text-gray-300 mb-3">Workflow Steps</h4>
          {steps.map((step: WorkflowStep, index: number) => {
            const isActive = index === status.currentStepIndex;
            const isComplete = index < status.currentStepIndex;
            const emoji = isComplete 
              ? '✅' 
              : isActive 
                ? '🔄' 
                : step.isStub 
                  ? '🔶' 
                  : '⏳';
            
            return (
              <div
                key={step.name}
                className={`flex items-start gap-3 p-2 rounded ${
                  isActive ? 'bg-blue-500/10' : ''
                }`}
              >
                <span className="text-lg">{emoji}</span>
                <div className="flex-1">
                  <p className={`text-sm font-medium ${
                    isActive ? 'text-blue-400' : 
                    isComplete ? 'text-gray-400' : 
                    'text-gray-500'
                  }`}>
                    {step.name}
                    {step.isStub && (
                      <span className="ml-2 text-xs text-orange-400">(Stub)</span>
                    )}
                    {!step.isRequired && (
                      <span className="ml-2 text-xs text-gray-500">(Optional)</span>
                    )}
                  </p>
                  <p className="text-xs text-gray-600 mt-0.5">
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
