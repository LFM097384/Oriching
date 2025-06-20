<template>
  <div class="ai-interpretation-panel">
    <div v-if="guaData" class="interpretation-content">
      <!-- AI分析状态 -->
      <div class="ai-status">
        <div class="status-header">
          <div class="status-icon">
            <SparklesIcon v-if="!isLoading" class="ai-icon" />
            <div v-else class="loading-spinner"></div>
          </div>
          <h4 class="status-title">AI 智能解卦</h4>
        </div>
        
        <div v-if="!interpretation && !isLoading" class="ai-prompt">
          <div class="prompt-content">
            <div class="prompt-icon">
              <SparklesIcon class="large-icon" />
            </div>
            <h4 class="prompt-title">AI 智能解卦</h4>
            <p class="prompt-text">AI解卦功能开发中，敬请期待</p>
            <button 
              class="zen-button primary large"
              @click="requestInterpretation"
            >
              <SparklesIcon class="w-5 h-5" />
              开始AI解卦
            </button>
          </div>
        </div>
        
        <div v-if="isLoading" class="loading-status">
          <div class="loading-text">正在处理...</div>
        </div>
      </div>
      
      <!-- AI解卦结果 -->
      <div v-if="interpretation" class="interpretation-result">
        <div class="result-sections">
          <div class="result-section">
            <h5 class="section-title">AI 分析结果</h5>
            <div class="section-content">
              <p class="interpretation-text">{{ interpretation.summary }}</p>
            </div>
          </div>
        </div>
      </div>
      
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <SparklesIcon class="empty-sparkles" />
      </div>
      <h3 class="empty-title">等待卦象</h3>
      <p class="empty-text">请先进行起卦</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SparklesIcon from './icons/SparklesIcon.vue'

const props = defineProps({
  guaData: { type: Object, default: null },
  isLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['request-interpretation'])

const interpretation = ref(null)

watch(() => props.isLoading, (loading) => {
  if (loading) {
    setTimeout(() => {
      interpretation.value = {
        summary: 'AI解卦功能开发中，敬请期待真实AI服务的接入',
        timestamp: new Date()
      }
    }, 2000)
  }
})

const requestInterpretation = () => {
  interpretation.value = null
  emit('request-interpretation')
}
</script>

<style scoped>
.ai-interpretation-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.interpretation-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* AI状态 */
.ai-status {
  margin-bottom: var(--space-6);
}

.status-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.status-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-icon {
  width: 24px;
  height: 24px;
  color: var(--water-blue);
}

.status-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--deep-ink);
  margin: 0;
}

.ai-prompt {
  text-align: center;
  padding: var(--space-6);
  background: var(--cloud-gray);
  border-radius: var(--radius-lg);
}

.prompt-content {
  max-width: 280px;
  margin: 0 auto;
}

.prompt-icon {
  margin-bottom: var(--space-4);
}

.large-icon {
  width: 48px;
  height: 48px;
  color: var(--water-blue);
}

.prompt-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--deep-ink);
  margin-bottom: var(--space-2);
}

.prompt-text {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  line-height: 1.5;
  margin-bottom: var(--space-4);
}

.zen-button.large {
  padding: var(--space-4) var(--space-6);
  font-size: var(--font-size-base);
}

.loading-status {
  text-align: center;
  padding: var(--space-6);
}

.loading-text {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
}

.interpretation-result {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-sections {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.result-section {
  background: var(--cloud-gray);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
}

.section-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--deep-ink);
  margin-bottom: var(--space-3);
}

.section-content {
  font-size: var(--font-size-sm);
  line-height: 1.6;
}

.interpretation-text {
  color: var(--sage-gray);
  margin: 0;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--sage-gray);
  padding: var(--space-8);
}

.empty-icon {
  margin-bottom: var(--space-4);
}

.empty-sparkles {
  width: 64px;
  height: 64px;
  color: var(--mist-gray);
}

.empty-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--sage-gray);
  margin-bottom: var(--space-2);
}

.empty-text {
  font-size: var(--font-size-sm);
  color: var(--mist-gray);
  max-width: 280px;
  line-height: 1.5;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
