import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const isDark = ref(false)
  const currentTheme = ref('light')
  
  // 主题配置
  const themes = {
    light: {
      name: '明亮模式',
      colors: {
        primary: '#4a90e2',
        background: '#fefefe',
        surface: '#f8f9fc',
        text: '#2d3748'
      }
    },
    dark: {
      name: '暗黑模式', 
      colors: {
        primary: '#64b5f6',
        background: '#1a202c',
        surface: '#2d3748',
        text: '#e2e8f0'
      }
    },
    zen: {
      name: '禅意模式',
      colors: {
        primary: '#48bb78',
        background: '#f7fafc',
        surface: '#ffffff',
        text: '#2d3748'
      }
    }
  }
  
  // 计算属性
  const currentThemeConfig = computed(() => themes[currentTheme.value])
  
  // 切换主题
  const toggleTheme = () => {
    isDark.value = !isDark.value
    currentTheme.value = isDark.value ? 'dark' : 'light'
    applyTheme()
    saveThemeToLocal()
  }
  
  // 设置特定主题
  const setTheme = (themeName) => {
    if (themes[themeName]) {
      currentTheme.value = themeName
      isDark.value = themeName === 'dark'
      applyTheme()
      saveThemeToLocal()
    }
  }
  
  // 应用主题到DOM
  const applyTheme = () => {
    const root = document.documentElement
    const theme = themes[currentTheme.value]
    
    // 应用CSS变量
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--theme-${key}`, value)
    })
    
    // 添加暗色模式类
    if (isDark.value) {
      document.body.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
    }
  }
  
  // 保存主题到本地存储
  const saveThemeToLocal = () => {
    try {
      localStorage.setItem('oriching_theme', JSON.stringify({
        isDark: isDark.value,
        currentTheme: currentTheme.value
      }))
    } catch (error) {
      console.error('保存主题设置失败:', error)
    }
  }
  
  // 从本地存储加载主题
  const loadThemeFromLocal = () => {
    try {
      const saved = localStorage.getItem('oriching_theme')
      if (saved) {
        const theme = JSON.parse(saved)
        isDark.value = theme.isDark
        currentTheme.value = theme.currentTheme
        applyTheme()
      }
    } catch (error) {
      console.error('加载主题设置失败:', error)
    }
  }
  
  // 自动检测系统主题
  const detectSystemTheme = () => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark')
    } else {
      setTheme('light')
    }
  }
  
  // 监听系统主题变化
  const watchSystemTheme = () => {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      mediaQuery.addEventListener('change', (e) => {
        if (e.matches) {
          setTheme('dark')
        } else {
          setTheme('light')
        }
      })
    }
  }
  
  // 初始化
  const init = () => {
    loadThemeFromLocal()
    if (!localStorage.getItem('oriching_theme')) {
      detectSystemTheme()
    }
    watchSystemTheme()
  }
  
  return {
    // 状态
    isDark,
    currentTheme,
    themes,
    
    // 计算属性
    currentThemeConfig,
    
    // 方法
    toggleTheme,
    setTheme,
    applyTheme,
    saveThemeToLocal,
    loadThemeFromLocal,
    detectSystemTheme,
    watchSystemTheme,
    init
  }
})
