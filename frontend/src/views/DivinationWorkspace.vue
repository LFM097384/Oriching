<template>
  <div class="divination-workspace">
    <!-- 顶部导航栏 -->
    <header class="workspace-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo">
            <TaijituIcon class="logo-icon" />
            <h1 class="app-title">Oriching</h1>
          </div>
          <span class="subtitle">占卜工作台</span>
        </div>
        
        <nav class="nav-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['nav-tab', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <component :is="tab.icon" class="tab-icon" />
            {{ tab.name }}
          </button>
        </nav>
        
        <div class="header-actions">
          <button class="zen-button" @click="toggleTheme">
            <MoonIcon v-if="isDark" class="w-4 h-4" />
            <SunIcon v-else class="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>

    <!-- 主工作区 -->
    <main class="workspace-main">
      <div class="workspace-grid">
        
        <!-- 左侧：起卦面板 -->
        <section class="left-panel zen-card">
          <div class="panel-header">
            <h2 class="panel-title">起卦设置</h2>
            <span class="panel-subtitle">选择起卦方式</span>
          </div>
          
          <div class="divination-methods">
            <div 
              v-for="method in divinationMethods" 
              :key="method.id"
              :class="['method-card', { active: selectedMethod === method.id }]"
              @click="selectedMethod = method.id"
            >
              <div class="method-icon">
                <component :is="method.icon" />
              </div>
              <div class="method-info">
                <h3 class="method-name">{{ method.name }}</h3>
                <p class="method-desc">{{ method.description }}</p>
              </div>
            </div>
          </div>
          
          <!-- 起卦参数 -->
          <div class="divination-params">
            <GuaParamsPanel 
              :method="selectedMethod"
              @update-params="handleParamsUpdate"
            />
          </div>
            <!-- 起卦按钮 -->
          <div class="action-buttons">
            <!-- 消息提示 -->
            <div v-if="errorMessage" class="message-alert error">
              <div class="alert-content">
                <span class="alert-icon">⚠️</span>
                <span class="alert-text">{{ errorMessage }}</span>
              </div>
            </div>
            
            <div v-if="successMessage" class="message-alert success">
              <div class="alert-content">
                <span class="alert-icon">✅</span>
                <span class="alert-text">{{ successMessage }}</span>
              </div>
            </div>
            
            <button 
              class="zen-button primary"
              :disabled="isLoading"
              @click="performDivination"
            >
              <div v-if="isLoading" class="loading-spinner"></div>
              <ZapIcon v-else class="w-4 h-4" />
              {{ isLoading ? '起卦中...' : '开始起卦' }}
            </button>
          </div>
        </section>

        <!-- 中央：卦象显示区 -->
        <section class="center-panel">
          <div class="gua-display-area zen-card">
            <GuaRenderer 
              v-if="currentGua"
              :gua-data="currentGua"
              :show-details="true"
            />
            <div v-else class="empty-state">
              <div class="empty-icon">
                <YinYangIcon class="floating" />
              </div>
              <h3 class="empty-title">等待起卦</h3>
              <p class="empty-text">选择起卦方式，开始您的占卜之旅</p>
            </div>
          </div>
          
          <!-- 卦象历史 -->
          <div class="gua-history zen-card" v-if="guaHistory.length > 0">
            <h3 class="history-title">最近卦象</h3>
            <div class="history-list">
              <div 
                v-for="(gua, index) in guaHistory.slice(0, 5)" 
                :key="index"
                class="history-item"
                @click="loadHistoryGua(gua)"              >
                <div class="history-mark">{{ gua.mark }}</div>
                <div class="history-info">
                  <span class="history-name">{{ gua.name }}</span>
                  <span class="history-time" v-if="gua.timestamp">{{ formatTime(gua.timestamp) }}</span>
                  <span class="history-time" v-else>时间未知</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 右侧：AI解卦区域 -->
        <section class="right-panel zen-card">
          <div class="panel-header">
            <h2 class="panel-title">AI 解卦</h2>
            <span class="panel-subtitle">智能卦象分析</span>
          </div>
          
          <AIInterpretationPanel 
            :gua-data="currentGua"
            :is-loading="aiLoading"
            @request-interpretation="handleAIInterpretation"
          />
        </section>
      </div>
    </main>

    <!-- 底部状态栏 -->
    <footer class="workspace-footer">
      <div class="footer-content">
        <div class="status-info">
          <div class="status-item">
            <span class="status-label">连接状态:</span>
            <span :class="['status-value', connectionStatus.class]">
              {{ connectionStatus.text }}
            </span>
          </div>
          <div class="status-item">
            <span class="status-label">已起卦:</span>
            <span class="status-value">{{ guaHistory.length }} 次</span>
          </div>
        </div>
        
        <div class="footer-actions">
          <button class="zen-button" @click="exportHistory">
            <DownloadIcon class="w-4 h-4" />
            导出记录
          </button>
          <button class="zen-button" @click="clearHistory">
            <TrashIcon class="w-4 h-4" />
            清空历史
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useDivinationStore } from '@/stores/divination'
import { useThemeStore } from '@/stores/theme'

// 组件导入
import GuaRenderer from '@/components/GuaRenderer.vue'
import GuaParamsPanel from '@/components/GuaParamsPanel.vue'
import AIInterpretationPanel from '@/components/AIInterpretationPanel.vue'

// 图标组件
import TaijituIcon from '@/components/icons/TaijituIcon.vue'
import YinYangIcon from '@/components/icons/YinYangIcon.vue'
import ZapIcon from '@/components/icons/ZapIcon.vue'
import MoonIcon from '@/components/icons/MoonIcon.vue'
import SunIcon from '@/components/icons/SunIcon.vue'
import DownloadIcon from '@/components/icons/DownloadIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import DiceIcon from '@/components/icons/DiceIcon.vue'
import ClockIcon from '@/components/icons/ClockIcon.vue'
import HandIcon from '@/components/icons/HandIcon.vue'

// 状态管理
const divinationStore = useDivinationStore()
const themeStore = useThemeStore()

// 响应式数据
const activeTab = ref('divination')
const selectedMethod = ref('manual')
const isLoading = ref(false)
const aiLoading = ref(false)
const currentGua = ref(null)
const guaHistory = ref([])
const guaParams = reactive({})
const errorMessage = ref('')
const successMessage = ref('')

// 计算属性
const isDark = computed(() => themeStore.isDark)
const connectionStatus = computed(() => {
  return divinationStore.isConnected 
    ? { text: '已连接', class: 'connected' }
    : { text: '未连接', class: 'disconnected' }
})

// 导航标签
const tabs = [
  { id: 'divination', name: '占卜', icon: YinYangIcon },
  { id: 'analysis', name: '分析', icon: ZapIcon },
  { id: 'history', name: '历史', icon: ClockIcon }
]

// 起卦方法
const divinationMethods = [
  {
    id: 'manual',
    name: '手动起卦',
    description: '手动输入六个数字进行起卦',
    icon: HandIcon
  },
  {
    id: 'random',
    name: '随机起卦',
    description: '系统随机生成卦象',
    icon: DiceIcon
  },
  {
    id: 'time',
    name: '时间起卦',
    description: '根据当前时间自动起卦',
    icon: ClockIcon
  }
]

// 方法定义
const toggleTheme = () => {
  themeStore.toggleTheme()
}

const handleParamsUpdate = (params) => {
  Object.assign(guaParams, params)
}

const performDivination = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {    const result = await divinationStore.performDivination(selectedMethod.value, guaParams)
    currentGua.value = result
    guaHistory.value.unshift({
      ...result,
      timestamp: new Date(),
      method: selectedMethod.value
    })
    
    // 保存到本地存储，确保时间戳格式正确
    const historyToSave = guaHistory.value.slice(0, 50).map(gua => ({
      ...gua,
      timestamp: gua.timestamp instanceof Date ? gua.timestamp.toISOString() : gua.timestamp
    }))
    localStorage.setItem('guaHistory', JSON.stringify(historyToSave))
    
    // 自动请求AI解释
    if (currentGua.value) {
      setTimeout(() => handleAIInterpretation(), 500)
    }
    
    successMessage.value = '起卦成功！'
    setTimeout(() => successMessage.value = '', 3000)
  } catch (error) {
    console.error('起卦失败:', error)
    errorMessage.value = error.message || '起卦失败，请检查网络连接或稍后重试'
    setTimeout(() => errorMessage.value = '', 5000)
  } finally {
    isLoading.value = false
  }
}

const handleAIInterpretation = async () => {
  if (!currentGua.value) return
  
  aiLoading.value = true
  try {
    // 这里可以接入AI解卦API
    await new Promise(resolve => setTimeout(resolve, 2000)) // 模拟AI请求
  } catch (error) {
    console.error('AI解卦失败:', error)
  } finally {
    aiLoading.value = false
  }
}

const loadHistoryGua = (gua) => {
  currentGua.value = gua
}

const formatTime = (date) => {
  try {
    // 确保输入是有效的日期
    const validDate = date instanceof Date ? date : new Date(date)
    
    // 检查日期是否有效
    if (isNaN(validDate.getTime())) {
      return '时间无效'
    }
    
    return new Intl.DateTimeFormat('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(validDate)
  } catch (error) {
    console.error('格式化时间失败:', error)
    return '时间无效'
  }
}

const exportHistory = () => {
  const data = JSON.stringify(guaHistory.value, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `占卜记录_${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const clearHistory = () => {
  if (confirm('确定要清空所有历史记录吗？')) {
    guaHistory.value = []
    localStorage.removeItem('guaHistory')
  }
}

// 生命周期
onMounted(() => {
  divinationStore.checkConnection()
  
  // 加载历史记录
  const savedHistory = localStorage.getItem('guaHistory')
  if (savedHistory) {
    try {
      const parsedHistory = JSON.parse(savedHistory)
      // 确保 timestamp 是 Date 对象
      guaHistory.value = parsedHistory.map(gua => ({
        ...gua,
        timestamp: gua.timestamp ? new Date(gua.timestamp) : new Date()
      }))
    } catch (error) {
      console.error('加载历史记录失败:', error)
      guaHistory.value = []
    }
  }
})
</script>

<style scoped>
.divination-workspace {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 顶部导航栏 */
.workspace-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: var(--border-light);
  padding: var(--space-4) 0;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: var(--water-blue);
}

.app-title {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--deep-ink);
  margin: 0;
}

.subtitle {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  font-weight: 400;
}

.nav-tabs {
  display: flex;
  gap: var(--space-2);
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border: none;
  background: transparent;
  border-radius: var(--radius-lg);
  color: var(--sage-gray);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-tab:hover,
.nav-tab.active {
  background: var(--primary-white);
  color: var(--water-blue);
  box-shadow: var(--shadow-soft);
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.header-actions {
  display: flex;
  gap: var(--space-2);
}

/* 主工作区 */
.workspace-main {
  flex: 1;
  padding: var(--space-6);
  overflow: hidden;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 350px 1fr 350px;
  gap: var(--space-6);
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* 面板样式 */
.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  padding: var(--space-6);
  overflow-y: auto;
}

.center-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.panel-header {
  margin-bottom: var(--space-6);
}

.panel-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--deep-ink);
  margin-bottom: var(--space-1);
}

.panel-subtitle {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
}

/* 起卦方法选择 */
.divination-methods {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.method-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border: var(--border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--primary-white);
}

.method-card:hover {
  border-color: var(--water-blue);
  box-shadow: var(--shadow-soft);
}

.method-card.active {
  border-color: var(--water-blue);
  background: rgba(74, 144, 226, 0.05);
}

.method-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  background: var(--cloud-gray);
  color: var(--water-blue);
}

.method-card.active .method-icon {
  background: var(--water-blue);
  color: white;
}

.method-info {
  flex: 1;
}

.method-name {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--deep-ink);
  margin-bottom: var(--space-1);
}

.method-desc {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  line-height: 1.4;
}

/* 卦象显示区 */
.gua-display-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  min-height: 400px;
}

.empty-state {
  text-align: center;
  color: var(--sage-gray);
}

.empty-icon {
  margin-bottom: var(--space-4);
}

.empty-icon svg {
  width: 80px;
  height: 80px;
  color: var(--mist-gray);
}

.empty-title {
  font-size: var(--font-size-xl);
  font-weight: 500;
  color: var(--ink-dark);
  margin-bottom: var(--space-2);
}

.empty-text {
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

/* 历史记录 */
.gua-history {
  padding: var(--space-4);
}

.history-title {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--deep-ink);
  margin-bottom: var(--space-3);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.history-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background: var(--cloud-gray);
}

.history-mark {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
  font-size: var(--font-size-xs);
  color: var(--water-blue);
  background: rgba(74, 144, 226, 0.1);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

.history-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.history-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--deep-ink);
}

.history-time {
  font-size: var(--font-size-xs);
  color: var(--sage-gray);
}

/* 动作按钮 */
.action-buttons {
  margin-top: auto;
  padding-top: var(--space-6);
}

.action-buttons .zen-button {
  width: 100%;
  justify-content: center;
  padding: var(--space-4);
  font-weight: 500;
}

/* 底部状态栏 */
.workspace-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-top: var(--border-light);
  padding: var(--space-3) 0;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-info {
  display: flex;
  gap: var(--space-6);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
}

.status-label {
  color: var(--sage-gray);
}

.status-value {
  font-weight: 500;
}

.status-value.connected {
  color: var(--mountain-green);
}

.status-value.disconnected {
  color: var(--fire-red);
}

.footer-actions {
  display: flex;
  gap: var(--space-2);
}

/* 加载动画 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 消息提示样式 */
.message-alert {
  margin-bottom: var(--space-4);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  animation: slideIn 0.3s ease-out;
}

.message-alert.error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #dc2626;
}

.message-alert.success {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.2);
  color: #16a34a;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.alert-icon {
  font-size: var(--font-size-sm);
}

.alert-text {
  font-size: var(--font-size-sm);
  font-weight: 500;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .workspace-grid {
    grid-template-columns: 300px 1fr 300px;
  }
}

@media (max-width: 768px) {
  .workspace-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  
  .header-content {
    padding: 0 var(--space-4);
  }
  
  .workspace-main {
    padding: var(--space-4);
  }
  
  .nav-tabs {
    order: 3;
    margin-top: var(--space-2);
  }
  
  .header-content {
    flex-wrap: wrap;
  }
}
</style>
