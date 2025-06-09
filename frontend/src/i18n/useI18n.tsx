import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { Language, Translations } from './translations';
import { languages, defaultLanguage } from './translations';

interface I18nContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
  availableLanguages: typeof languages;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

interface I18nProviderProps {
  children: ReactNode;
}

export const I18nProvider: React.FC<I18nProviderProps> = ({ children }) => {  const [language, setLanguage] = useState<Language>(() => {
    // 从 localStorage 读取保存的语言设置
    const savedLanguage = localStorage.getItem('language') as Language;
    return savedLanguage && languages[savedLanguage] ? savedLanguage : defaultLanguage;
  });

  useEffect(() => {
    // 保存语言设置到 localStorage
    localStorage.setItem('language', language);
  }, [language]);
  
  const value: I18nContextType = {
    language,
    setLanguage,
    t: languages[language].translations,
    availableLanguages: languages,
  };

  return (
    <I18nContext.Provider value={value}>
      {children}
    </I18nContext.Provider>
  );
};

export const useI18n = () => {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
};

// 导出类型
export type { Language, Translations };