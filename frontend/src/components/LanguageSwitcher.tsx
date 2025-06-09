import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Globe, ChevronDown } from 'lucide-react';
import { useI18n } from '../i18n/useI18n';
import type { Language } from '../i18n/translations';
import { languages } from '../i18n/translations';

interface LanguageSwitcherProps {
  className?: string;
  variant?: 'button' | 'dropdown';
  onLanguageChange?: (language: Language) => void;
}

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ 
  className = "", 
  variant = "dropdown",
  onLanguageChange
}) => {
  const { language, setLanguage } = useI18n();
  const [isOpen, setIsOpen] = useState(false);

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (onLanguageChange) {
      onLanguageChange(newLang);
    }
  };

  const currentLang = languages[language];

  if (variant === 'button') {
    return (
      <motion.button
        className={`flex items-center gap-2 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 text-white transition-colors ${className}`}
        onClick={() => handleLanguageChange(language === 'zh' ? 'en' : 'zh')}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Globe className="w-4 h-4" />
        <span className="text-sm font-medium">{currentLang.flag} {currentLang.name}</span>
      </motion.button>
    );
  }

  return (
    <div className={`relative ${className}`}>
      <motion.button
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 text-white transition-colors w-full"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <Globe className="w-4 h-4" />
        <span className="text-sm font-medium flex-1 text-left">
          {currentLang.flag} {currentLang.name}
        </span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown className="w-4 h-4" />
        </motion.div>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            {/* 背景遮罩 */}
            <motion.div
              className="fixed inset-0 z-40"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />
            
            {/* 下拉菜单 */}
            <motion.div
              className="absolute top-full left-0 right-0 mt-2 bg-black/80 backdrop-blur-xl border border-white/20 rounded-lg shadow-xl z-50 overflow-hidden"
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.2 }}
            >
              {Object.entries(languages).map(([langCode, langConfig]) => (
                <motion.button
                  key={langCode}
                  className={`w-full px-3 py-2 text-left flex items-center gap-2 text-sm transition-colors ${
                    language === langCode
                      ? 'bg-white/20 text-white'
                      : 'text-white/70 hover:bg-white/10 hover:text-white'
                  }`}                  onClick={() => {
                    handleLanguageChange(langCode as Language);
                    setIsOpen(false);
                  }}
                  whileHover={{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }}
                >
                  <span className="text-base">{langConfig.flag}</span>
                  <span className="font-medium">{langConfig.name}</span>
                  {language === langCode && (
                    <motion.div
                      className="ml-auto w-2 h-2 bg-green-400 rounded-full"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.1 }}
                    />
                  )}
                </motion.button>
              ))}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LanguageSwitcher;
