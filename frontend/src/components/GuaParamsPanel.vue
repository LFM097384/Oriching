<template>
  <div class="gua-params-panel">
    <div v-if="method === 'manual'" class="manual-params">
      <h4 class="params-title">手动输入参数</h4>
      <p class="params-desc">请输入6个数字（1-4），代表六爻的初始状态</p>
      
      <div class="params-grid">
        <div 
          v-for="(param, index) in manualParams" 
          :key="index"
          class="param-input-group"
        >
          <label class="param-label">{{ getYaoName(index) }}</label>
          <input 
            v-model.number="manualParams[index]"
            type="number"
            min="1"
            max="4"
            class="zen-input param-input"
            :placeholder="getParamHint(index)"
            @input="updateParams"
          />
          <div class="param-hint">
            {{ getParamDescription(manualParams[index]) }}
          </div>
        </div>
      </div>
      
      <div class="additional-options">
        <div class="option-group">
          <label class="option-label">性别</label>
          <select v-model="gender" class="zen-input" @change="updateParams">
            <option value="">不限</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        
        <div class="option-group">
          <label class="option-label">起卦标题</label>
          <input 
            v-model="title"
            type="text"
            class="zen-input"
            placeholder="输入要占卜的事项"
            @input="updateParams"
          />
        </div>
        
        <div class="option-group">
          <label class="option-label">指定时间</label>
          <input 
            v-model="customDate"
            type="datetime-local"
            class="zen-input"
            @change="updateParams"
          />
        </div>
      </div>
    </div>
    
    <div v-else-if="method === 'random'" class="random-params">
      <h4 class="params-title">随机起卦设置</h4>
      <p class="params-desc">系统将随机生成6个数字进行起卦</p>
      
      <div class="random-options">
        <div class="option-group">
          <label class="option-label">性别</label>
          <select v-model="gender" class="zen-input" @change="updateParams">
            <option value="">不限</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        
        <div class="option-group">
          <label class="option-label">起卦标题</label>
          <input 
            v-model="title"
            type="text"
            class="zen-input"
            placeholder="输入要占卜的事项"
            @input="updateParams"
          />
        </div>
      </div>
      
      <div class="random-preview">
        <div class="preview-card">
          <DiceIcon class="preview-icon" />
          <span class="preview-text">点击"开始起卦"生成随机卦象</span>
        </div>
      </div>
    </div>
    
    <div v-else-if="method === 'time'" class="time-params">
      <h4 class="params-title">时间起卦设置</h4>
      <p class="params-desc">根据当前时间的干支信息进行起卦</p>
      
      <div class="time-display">
        <div class="current-time">
          <ClockIcon class="time-icon" />
          <div class="time-info">
            <div class="time-value">{{ currentTime }}</div>
            <div class="time-label">当前时间</div>
          </div>
        </div>
      </div>
      
      <div class="time-options">
        <div class="option-group">
          <label class="option-label">性别</label>
          <select v-model="gender" class="zen-input" @change="updateParams">
            <option value="">不限</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        
        <div class="option-group">
          <label class="option-label">起卦标题</label>
          <input 
            v-model="title"
            type="text"
            class="zen-input"
            placeholder="输入要占卜的事项"
            @input="updateParams"
          />
        </div>
      </div>
    </div>
    
    <!-- 参数验证提示 -->
    <div v-if="validationMessage" class="validation-message">
      <AlertIcon class="validation-icon" />
      <span>{{ validationMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import DiceIcon from './icons/DiceIcon.vue'
import ClockIcon from './icons/ClockIcon.vue'
import AlertIcon from './icons/AlertIcon.vue'

const props = defineProps({
  method: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update-params'])

// 响应式数据
const manualParams = ref([1, 1, 1, 1, 1, 1])
const gender = ref('')
const title = ref('')
const customDate = ref('')
const currentTime = ref('')
const validationMessage = ref('')

let timeInterval = null

// 计算属性
const isValidManualParams = computed(() => {
  return manualParams.value.every(param => 
    Number.isInteger(param) && param >= 1 && param <= 4
  )
})

// 方法定义 - 必须在 watch 之前定义
const getYaoName = (index) => {
  const names = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻']
  return names[index]
}

const getParamHint = (index) => {
  return `第${index + 1}爻`
}

const getParamDescription = (value) => {
  const descriptions = {
    1: '少阳',
    2: '少阴', 
    3: '老阴(动)',
    4: '老阳(动)'
  }
  return descriptions[value] || '请输入1-4'
}

const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const validateParams = () => {
  if (props.method === 'manual') {
    if (!isValidManualParams.value) {
      validationMessage.value = '请输入6个有效的数字（1-4）'
      return false
    }
  }
  validationMessage.value = ''
  return true
}

const updateParams = () => {
  if (!validateParams()) return
  
  const params = {}
  
  switch (props.method) {
    case 'manual':
      params.params = [...manualParams.value]
      if (gender.value) params.gender = gender.value
      if (title.value) params.title = title.value
      if (customDate.value) params.date = customDate.value
      break
      
    case 'random':
      if (gender.value) params.gender = gender.value
      if (title.value) params.title = title.value
      break
      
    case 'time':
      if (gender.value) params.gender = gender.value
      if (title.value) params.title = title.value
      break
  }
  
  emit('update-params', params)
}

// 监听方法变化 - 现在 updateParams 已经定义了
watch(() => props.method, () => {
  updateParams()
}, { immediate: true })

// 监听手动参数变化
watch(manualParams, () => {
  validateParams()
}, { deep: true })

// 生命周期
onMounted(() => {
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
  updateParams()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.gua-params-panel {
  width: 100%;
}

.params-title {
  font-size: var(--font-size-lg);
  font-weight: 500;
  color: var(--deep-ink);
  margin-bottom: var(--space-2);
}

.params-desc {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  line-height: 1.5;
  margin-bottom: var(--space-6);
}

/* 手动参数 */
.params-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.param-input-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.param-label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--ink-dark);
}

.param-input {
  text-align: center;
  font-weight: 500;
  font-size: var(--font-size-base);
}

.param-hint {
  font-size: var(--font-size-xs);
  color: var(--sage-gray);
  text-align: center;
  min-height: 16px;
}

/* 附加选项 */
.additional-options,
.random-options,
.time-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.option-label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--ink-dark);
}

/* 随机起卦预览 */
.random-preview {
  margin-top: var(--space-4);
}

.preview-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-6);
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1), rgba(72, 187, 120, 0.1));
  border: 2px dashed var(--water-blue);
  border-radius: var(--radius-lg);
  color: var(--water-blue);
}

.preview-icon {
  width: 24px;
  height: 24px;
}

.preview-text {
  font-size: var(--font-size-sm);
  font-weight: 500;
}

/* 时间显示 */
.time-display {
  margin-bottom: var(--space-6);
}

.current-time {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--soft-white);
  border-radius: var(--radius-lg);
  border: var(--border-light);
}

.time-icon {
  width: 32px;
  height: 32px;
  color: var(--water-blue);
}

.time-info {
  flex: 1;
}

.time-value {
  font-size: var(--font-size-lg);
  font-weight: 500;
  color: var(--deep-ink);
  font-family: 'SF Mono', 'Monaco', monospace;
}

.time-label {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
}

/* 验证消息 */
.validation-message {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3);
  background: rgba(229, 62, 62, 0.1);
  border: 1px solid rgba(229, 62, 62, 0.3);
  border-radius: var(--radius-md);
  color: var(--fire-red);
  font-size: var(--font-size-sm);
  margin-top: var(--space-4);
}

.validation-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .params-grid {
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }
  
  .additional-options,
  .random-options,
  .time-options {
    gap: var(--space-3);
  }
}
</style>
