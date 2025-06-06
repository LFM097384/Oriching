import React from 'react';
import { cn } from '@/lib/utils';

interface EnhancedLoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'pulse' | 'dots';
  className?: string;
  text?: string;
}

export const EnhancedLoadingSpinner: React.FC<EnhancedLoadingSpinnerProps> = ({
  size = 'md',
  variant = 'default',
  className,
  text
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  if (variant === 'pulse') {
    return (
      <div className={cn("flex flex-col items-center gap-2", className)}>
        <div className={cn(
          "rounded-full bg-blue-500 animate-pulse",
          sizeClasses[size]
        )} />
        {text && <span className="text-sm text-gray-400">{text}</span>}
      </div>
    );
  }

  if (variant === 'dots') {
    return (
      <div className={cn("flex flex-col items-center gap-2", className)}>
        <div className="flex gap-1">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className={cn(
                "rounded-full bg-blue-500 animate-bounce",
                size === 'sm' ? 'h-2 w-2' : size === 'md' ? 'h-3 w-3' : 'h-4 w-4'
              )}
              style={{
                animationDelay: `${i * 0.1}s`
              }}
            />
          ))}
        </div>
        {text && <span className="text-sm text-gray-400">{text}</span>}
      </div>
    );
  }

  return (
    <div className={cn("flex flex-col items-center gap-2", className)}>
      <div className={cn(
        "animate-spin rounded-full border-2 border-gray-300 border-t-blue-500",
        sizeClasses[size]
      )} />
      {text && <span className="text-sm text-gray-400">{text}</span>}
    </div>
  );
};