import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useDivinationStore = defineStore('divination', () => {
  // 状态
  const isConnected = ref(false)
  const currentGua = ref(null)
  const guaHistory = ref([])
  const isLoading = ref(false)
  
  // API基础配置
  const API_BASE = import.meta.env.VITE_API_BASE || '/api'
  
  // 计算属性
  const hasCurrentGua = computed(() => !!currentGua.value)
  const totalGuaCount = computed(() => guaHistory.value.length)
  
  // 检查连接状态
  const checkConnection = async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`)
      isConnected.value = response.status === 200
      return isConnected.value
    } catch (error) {
      console.error('连接检查失败:', error)
      isConnected.value = false
      return false
    }
  }
  
  // 执行起卦
  const performDivination = async (method, params = {}) => {
    isLoading.value = true
    try {
      let endpoint
      let data = params
      
      switch (method) {
        case 'manual':
          endpoint = `${API_BASE}/gua`
          break
        case 'random':
          endpoint = `${API_BASE}/random`
          break
        case 'time':
          endpoint = `${API_BASE}/time-gua`
          break
        default:
          throw new Error(`未知的起卦方法: ${method}`)
      }
      
      const response = await axios.post(endpoint, data)
      
      if (response.data.success) {
        const guaData = {
          ...response.data.data,
          rendered: response.data.rendered,
          method,
          timestamp: new Date().toISOString()
        }
        
        currentGua.value = guaData
        addToHistory(guaData)
        
        return guaData
      } else {
        throw new Error(response.data.message || '起卦失败')
      }
    } catch (error) {
      console.error('起卦失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  // 获取系统常量
  const getConstants = async () => {
    try {
      const response = await axios.get(`${API_BASE}/constants`)
      return response.data.data
    } catch (error) {
      console.error('获取常量失败:', error)
      throw error
    }
  }
  
  // 获取卦象分析
  const getGuaAnalysis = async (guaName) => {
    try {
      const response = await axios.get(`${API_BASE}/gua-analysis/${encodeURIComponent(guaName)}`)
      return response.data
    } catch (error) {
      console.error('获取卦象分析失败:', error)
      throw error
    }
  }
  
  // 添加到历史记录
  const addToHistory = (guaData) => {
    const historyItem = {
      ...guaData,
      id: Date.now(),
      timestamp: new Date().toISOString()
    }
    
    guaHistory.value.unshift(historyItem)
    
    // 限制历史记录数量
    if (guaHistory.value.length > 100) {
      guaHistory.value = guaHistory.value.slice(0, 100)
    }
    
    // 保存到本地存储
    saveHistoryToLocal()
  }
  
  // 从历史记录加载卦象
  const loadFromHistory = (historyItem) => {
    currentGua.value = historyItem
  }
  
  // 清空历史记录
  const clearHistory = () => {
    guaHistory.value = []
    localStorage.removeItem('gua_history')
  }
  
  // 导出历史记录
  const exportHistory = () => {
    const data = {
      exportTime: new Date().toISOString(),
      totalCount: guaHistory.value.length,
      history: guaHistory.value
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { 
      type: 'application/json' 
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `oriching_gua_history_${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }
  
  // 保存历史到本地存储
  const saveHistoryToLocal = () => {
    try {
      localStorage.setItem('gua_history', JSON.stringify(guaHistory.value))
    } catch (error) {
      console.error('保存历史记录失败:', error)
    }
  }
  
  // 从本地存储加载历史
  const loadHistoryFromLocal = () => {
    try {
      const saved = localStorage.getItem('gua_history')
      if (saved) {
        guaHistory.value = JSON.parse(saved)
      }
    } catch (error) {
      console.error('加载历史记录失败:', error)
    }
  }
  
  // 初始化
  const init = async () => {
    loadHistoryFromLocal()
    await checkConnection()
  }
  
  return {
    // 状态
    isConnected,
    currentGua,
    guaHistory,
    isLoading,
    
    // 计算属性
    hasCurrentGua,
    totalGuaCount,
    
    // 方法
    checkConnection,
    performDivination,
    getConstants,
    getGuaAnalysis,
    addToHistory,
    loadFromHistory,
    clearHistory,
    exportHistory,
    saveHistoryToLocal,
    loadHistoryFromLocal,
    init
  }
})
