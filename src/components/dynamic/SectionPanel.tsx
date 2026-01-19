import React from 'react';

export interface SectionPanelProps {
  /**
   * The title of the section
   */
  title: string;
  
  /**
   * Optional subtitle or description
   */
  subtitle?: string;
  
  /**
   * Content to render inside the panel
   */
  children: React.ReactNode;
  
  /**
   * Whether the section is collapsible
   * @default false
   */
  collapsible?: boolean;
  
  /**
   * Initial collapsed state (only used when collapsible is true)
   * @default false
   */
  defaultCollapsed?: boolean;
}

/**
 * A glassmorphic section panel component for organizing content sections.
 * Features a modern glass effect with dark theme and metal accents.
 */
export function SectionPanel(props: SectionPanelProps): React.JSX.Element {
  const { title, subtitle, children, collapsible = false, defaultCollapsed = false } = props;
  const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed);
  
  const handleToggle = (): void => {
    if (collapsible) {
      setIsCollapsed(!isCollapsed);
    }
  };
  
  return (
    <div className="glass-panel p-6 mb-4 transition-all duration-300 hover:shadow-xl">
      <div 
        className={`flex justify-between items-center ${collapsible ? 'cursor-pointer' : ''}`}
        onClick={handleToggle}
        role={collapsible ? 'button' : undefined}
        aria-expanded={collapsible ? !isCollapsed : undefined}
        tabIndex={collapsible ? 0 : undefined}
        onKeyDown={collapsible ? (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            handleToggle();
          }
        } : undefined}
      >
        <div>
          <h2 className="text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 mb-1">
            {title}
          </h2>
          {subtitle && (
            <p className="text-sm text-gray-400">{subtitle}</p>
          )}
        </div>
        
        {collapsible && (
          <div className="text-gray-400 transition-transform duration-200" style={{ transform: isCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)' }}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        )}
      </div>
      
      {!isCollapsed && (
        <div className="mt-4">
          {children}
        </div>
      )}
    </div>
  );
}
