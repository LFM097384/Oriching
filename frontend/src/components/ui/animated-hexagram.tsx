import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface AnimatedHexagramProps {
  lines?: number[]; // 6个数字，表示每一爻的值
  size?: 'sm' | 'md' | 'lg';
  animated?: boolean;
  className?: string;
}

export const AnimatedHexagram: React.FC<AnimatedHexagramProps> = ({
  lines = [6, 7, 8, 9, 6, 7], // 默认卦象
  size = 'md',
  animated = true,
  className
}) => {
  const [visibleLines, setVisibleLines] = useState<number[]>([]);

  useEffect(() => {
    if (animated) {
      setVisibleLines([]);
      lines.forEach((_, index) => {
        setTimeout(() => {
          setVisibleLines(prev => [...prev, index]);
        }, index * 300);
      });
    } else {
      setVisibleLines(lines.map((_, i) => i));
    }
  }, [lines, animated]);

  const sizeClasses = {
    sm: { line: 'h-1', gap: 'gap-1', width: 'w-16' },
    md: { line: 'h-2', gap: 'gap-2', width: 'w-24' },
    lg: { line: 'h-3', gap: 'gap-3', width: 'w-32' }
  };

  const renderLine = (value: number, index: number, isVisible: boolean) => {
    const isChanging = value === 6 || value === 9; // 变爻
    const isBroken = value === 8 || value === 6; // 阴爻
    
    return (
      <div
        key={index}
        className={cn(
          "flex justify-center transition-all duration-300",
          sizeClasses[size].width,
          isVisible ? "opacity-100 scale-100" : "opacity-0 scale-95"
        )}
      >
        <div className={cn(
          "relative transition-all duration-500",
          sizeClasses[size].line,
          sizeClasses[size].width
        )}>
          {isBroken ? (
            // 阴爻 (断开的线)
            <div className="flex justify-between items-center h-full">
              <div className={cn(
                "bg-current rounded-sm transition-all duration-300",
                sizeClasses[size].line,
                "w-2/5",
                isChanging && "animate-pulse"
              )} />
              <div className={cn(
                "bg-current rounded-sm transition-all duration-300", 
                sizeClasses[size].line,
                "w-2/5",
                isChanging && "animate-pulse"
              )} />
            </div>
          ) : (
            // 阳爻 (连续的线)
            <div className={cn(
              "bg-current rounded-sm w-full h-full transition-all duration-300",
              isChanging && "animate-pulse"
            )} />
          )}
          
          {/* 变爻标记 */}
          {isChanging && (
            <div className="absolute -right-2 top-1/2 transform -translate-y-1/2">
              <div className="w-1 h-1 bg-red-400 rounded-full animate-ping" />
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className={cn(
      "flex flex-col text-blue-400",
      sizeClasses[size].gap,
      className
    )}>
      {/* 从下往上渲染（第六爻到第一爻） */}
      {lines.slice().reverse().map((line, index) => {
        const originalIndex = lines.length - 1 - index;
        return renderLine(line, originalIndex, visibleLines.includes(originalIndex));
      })}
    </div>
  );
};