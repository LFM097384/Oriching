import React, { createContext, useContext, useState, ReactNode } from 'react';
import { cn } from "@/lib/utils";
import { X } from 'lucide-react';

interface Toast {
  id: string;
  title?: string;
  description?: string;
  variant?: 'default' | 'destructive' | 'success';
  duration?: number;
}

interface ToastContextType {
  toasts: Toast[];
  toast: (toast: Omit<Toast, 'id'>) => void;
  dismiss: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const toast = (newToast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const toastWithId = { ...newToast, id };
    
    setToasts(prev => [...prev, toastWithId]);
    
    // Auto dismiss after duration
    const duration = newToast.duration || 5000;
    setTimeout(() => {
      dismiss(id);
    }, duration);
  };

  const dismiss = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ toasts, toast, dismiss }}>
      {children}
      <ToastContainer />
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  
  // 添加便利函数
  const showSuccess = (title: string, description?: string) => {
    context.toast({
      title,
      description,
      variant: 'success'
    });
  };

  const showError = (title: string, description?: string) => {
    context.toast({
      title,
      description,
      variant: 'destructive'
    });
  };

  const showInfo = (title: string, description?: string) => {
    context.toast({
      title,
      description,
      variant: 'default'
    });
  };

  return {
    ...context,
    showSuccess,
    showError,
    showInfo
  };
};

export const ToastContainer: React.FC = () => {
  const { toasts, dismiss } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            "min-w-[300px] rounded-lg border p-4 shadow-lg transition-all",
            "bg-background border-border",
            toast.variant === 'destructive' && "border-red-500 bg-red-50 text-red-900",
            toast.variant === 'success' && "border-green-500 bg-green-50 text-green-900"
          )}
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              {toast.title && (
                <div className="font-semibold">{toast.title}</div>
              )}
              {toast.description && (
                <div className="text-sm opacity-90">{toast.description}</div>
              )}
            </div>
            <button
              onClick={() => dismiss(toast.id)}
              className="opacity-70 hover:opacity-100 transition-opacity"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};