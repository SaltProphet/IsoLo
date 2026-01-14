import React from 'react';

/**
 * Props for the Card component
 */
export interface CardProps {
  /**
   * The title displayed at the top of the card
   */
  title: string;
  
  /**
   * Optional description text
   */
  description?: string;
  
  /**
   * Child elements to render inside the card
   */
  children?: React.ReactNode;
  
  /**
   * Optional click handler for the entire card
   */
  onClick?: () => void;
  
  /**
   * Visual variant of the card
   * @default 'default'
   */
  variant?: 'default' | 'outlined' | 'elevated';
}

/**
 * A modular, reusable card component for displaying content in a contained format.
 * 
 * This component demonstrates the AI-Aware structure principles:
 * - Explicit TypeScript interfaces with no 'any' types
 * - Tailwind CSS for all styling
 * - Self-contained and composable
 * - Clear props documentation
 * 
 * @example
 * ```tsx
 * <Card title="Welcome" description="Get started with FileUploads">
 *   <button>Click me</button>
 * </Card>
 * ```
 */
export function Card(props: CardProps): React.JSX.Element {
  const { title, description, children, onClick, variant = 'default' } = props;
  
  // Determine styling based on variant
  const variantClasses = {
    default: 'bg-white border border-gray-200',
    outlined: 'bg-transparent border-2 border-gray-300',
    elevated: 'bg-white shadow-lg',
  };
  
  const baseClasses = 'rounded-lg p-6 transition-all duration-200';
  const interactiveClasses = onClick 
    ? 'cursor-pointer hover:shadow-md' 
    : '';
  
  const cardClasses = `${baseClasses} ${variantClasses[variant]} ${interactiveClasses}`;
  
  return (
    <div 
      className={cardClasses}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      } : undefined}
    >
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        {title}
      </h3>
      
      {description && (
        <p className="text-gray-600 text-sm mb-4">
          {description}
        </p>
      )}
      
      {children && (
        <div className="mt-4">
          {children}
        </div>
      )}
    </div>
  );
}
