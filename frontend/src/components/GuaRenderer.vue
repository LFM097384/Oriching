<template>
  <div class="gua-renderer">
    <div v-if="guaData" class="gua-container">
      <!-- 卦象标题 -->
      <div class="gua-header">
        <h2 class="gua-name">{{ guaData.name }}</h2>
        <div class="gua-meta">
          <span class="gua-palace">{{ guaData.gong }}宫</span>
          <span class="gua-mark">{{ guaData.mark }}</span>
        </div>
      </div>
        <!-- 主卦象 -->
      <div class="gua-diagram">
        <div class="main-gua">
          <h3 class="gua-section-title">主卦 <span class="gua-bagua">{{ getMainBagua() }}</span></h3>
          <div class="gua-lines">
            <div 
              v-for="(line, index) in renderMainGua" 
              :key="index"
              :class="['gua-line', { 
                'yang': line.value === '1', 
                'yin': line.value === '0',
                'dong': isDongYao(5 - index),
                'shi': isShiYao(5 - index),
                'ying': isYingYao(5 - index)
              }]"
              @click="showLineDetails(5 - index)"
            >
              <div class="line-number">{{ 6 - index }}</div>
              <div class="line-symbol">
                <div class="line-visual">
                  <div v-if="line.value === '1'" class="yang-line">
                    <div class="line-inner"></div>
                  </div>
                  <div v-else class="yin-line">
                    <div class="yin-left"></div>
                    <div class="yin-gap"></div>
                    <div class="yin-right"></div>
                  </div>
                </div>
                <div v-if="isDongYao(5 - index)" class="dong-marker">
                  {{ getDongSymbol(5 - index) }}
                </div>
              </div>
              <div class="line-info">
                <span class="line-qin">{{ getQin(5 - index) }}</span>
                <span class="line-gan-zhi">{{ getGanZhi(5 - index) }}</span>
                <div class="line-markers">
                  <span v-if="isShiYao(5 - index)" class="shi-marker">世</span>
                  <span v-if="isYingYao(5 - index)" class="ying-marker">应</span>
                </div>
              </div>
              <div class="line-god">
                <span class="god-name">{{ getGod(5 - index) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 变卦 -->
        <div v-if="guaData.bian && hasDongYao" class="bian-gua">
          <h3 class="gua-section-title">变卦</h3>
          <div class="gua-lines">
            <div 
              v-for="(line, index) in renderBianGua" 
              :key="index"
              :class="['gua-line', { 
                'yang': line.value === '1', 
                'yin': line.value === '0'
              }]"
            >
              <div class="line-number">{{ 6 - index }}</div>
              <div class="line-symbol">
                <div class="line-visual">
                  <div v-if="line.value === '1'" class="yang-line"></div>
                  <div v-else class="yin-line">
                    <span class="yin-gap"></span>
                  </div>
                </div>
              </div>
              <div class="line-info">
                <span class="line-qin">{{ getBianQin(5 - index) }}</span>
                <span class="line-gan-zhi">{{ getBianGanZhi(5 - index) }}</span>
              </div>
            </div>
          </div>
          <div class="bian-meta">
            <span class="bian-name">{{ guaData.bian.name }}</span>
            <span class="bian-type">{{ guaData.bian.type }}</span>
          </div>
        </div>
      </div>
      
      <!-- 时间信息 -->
      <div v-if="showDetails" class="gua-timing">
        <div class="timing-info">
          <h4>时间信息</h4>
          <div class="timing-details">
            <div class="solar-time">
              公历：{{ formatSolarTime(guaData.solar) }}
            </div>
            <div v-if="guaData.lunar" class="lunar-info">
              干支：{{ formatLunarInfo(guaData.lunar) }}
              <span class="xun-kong">（旬空：{{ guaData.lunar.xkong }}）</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 详细信息 -->
      <div v-if="showDetails" class="gua-details">
        <div class="detail-section">
          <h4>起卦参数</h4>
          <div class="params-display">
            {{ guaData.params ? guaData.params.join(', ') : '无' }}
          </div>
        </div>
        
        <div v-if="guaData.dong && guaData.dong.length" class="detail-section">
          <h4>动爻</h4>
          <div class="dong-yao-list">
            <span 
              v-for="dong in guaData.dong" 
              :key="dong"
              class="dong-yao-item"
            >
              {{ dong + 1 }}爻
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-gua">
      <div class="empty-content">
        <YinYangIcon class="empty-icon floating" />
        <p class="empty-text">暂无卦象数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import YinYangIcon from './icons/YinYangIcon.vue'

const props = defineProps({
  guaData: {
    type: Object,
    default: null
  },
  showDetails: {
    type: Boolean,
    default: true
  }
})

// 计算属性
const renderMainGua = computed(() => {
  if (!props.guaData?.mark) return []
  return props.guaData.mark.split('').map(bit => ({ value: bit }))
})

const renderBianGua = computed(() => {
  if (!props.guaData?.bian?.mark) return []
  if (typeof props.guaData.bian.mark === 'string') {
    return props.guaData.bian.mark.split('').map(bit => ({ value: bit }))
  }
  // 如果mark是数组（包含符号），提取01值
  return props.guaData.bian.mark.map(line => {
    if (line.includes('▅▅▅▅▅▅')) return { value: '1' }
    if (line.includes('▅▅  ▅▅')) return { value: '0' }
    return { value: '0' }
  })
})

const hasDongYao = computed(() => {
  return props.guaData?.dong && props.guaData.dong.length > 0
})

// 工具方法
const isDongYao = (index) => {
  return props.guaData?.dong?.includes(index) || false
}

const isShiYao = (index) => {
  return props.guaData?.shiy?.[index]?.includes('世') || false
}

const isYingYao = (index) => {
  return props.guaData?.shiy?.[index]?.includes('应') || false
}

const getDongSymbol = (index) => {
  if (!props.guaData?.params) return ''
  const param = props.guaData.params[index]
  if (param === 3) return '○→'
  if (param === 4) return '×→'
  return ''
}

const getMainBagua = () => {
  if (!props.guaData?.bagua) return ''
  const [shang, xia] = props.guaData.bagua
  return `${shang}${xia}`
}

const showLineDetails = (index) => {
  // 这里可以添加显示爻的详细信息的逻辑
  const lineInfo = {
    position: index + 1,
    type: props.guaData.mark[5 - index] === '1' ? '阳爻' : '阴爻',
    qin: getQin(index),
    ganZhi: getGanZhi(index),
    god: getGod(index),
    isDong: isDongYao(index),
    isShi: isShiYao(index),
    isYing: isYingYao(index)
  }
  
  console.log('爻位信息:', lineInfo)
  // 后续可以添加弹窗或者侧边栏显示详细信息
}

const getQin = (index) => {
  return props.guaData?.qin6?.[index] || ''
}

const getGanZhi = (index) => {
  return props.guaData?.qinx?.[index] || ''
}

const getGod = (index) => {
  return props.guaData?.god6?.[index] || ''
}

const getBianQin = (index) => {
  return props.guaData?.bian?.qin6?.[index] || ''
}

const getBianGanZhi = (index) => {
  return props.guaData?.bian?.qinx?.[index] || ''
}

const formatSolarTime = (solar) => {
  if (!solar) return ''
  const date = new Date(solar)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatLunarInfo = (lunar) => {
  if (!lunar?.gz) return ''
  const { year, month, day, hour } = lunar.gz
  return `${year}年 ${month}月 ${day}日 ${hour}时`
}
</script>

<style scoped>
.gua-renderer {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.gua-container {
  background: var(--primary-white);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  box-shadow: var(--shadow-medium);
}

/* 卦象标题 */
.gua-header {
  text-align: center;
  margin-bottom: var(--space-6);
  border-bottom: var(--border-light);
  padding-bottom: var(--space-4);
}

.gua-name {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--deep-ink);
  margin-bottom: var(--space-2);
}

.gua-meta {
  display: flex;
  justify-content: center;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
}

.gua-palace {
  background: var(--cloud-gray);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
}

.gua-mark {
  font-family: 'SF Mono', 'Monaco', monospace;
  background: rgba(74, 144, 226, 0.1);
  color: var(--water-blue);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
}

/* 卦象图 */
.gua-diagram {
  display: flex;
  gap: var(--space-8);
  justify-content: center;
  margin-bottom: var(--space-6);
}

.main-gua,
.bian-gua {
  flex: 1;
  max-width: 280px;
}

.gua-section-title {
  text-align: center;
  font-size: var(--font-size-lg);
  font-weight: 500;
  color: var(--ink-dark);
  margin-bottom: var(--space-4);
}

.gua-lines {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.gua-line {
  display: grid;
  grid-template-columns: 24px 1fr 120px 60px;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.gua-line:hover {
  background: var(--cloud-gray);
}

.gua-line.dong {
  background: rgba(237, 137, 54, 0.1);
  border: 1px solid rgba(237, 137, 54, 0.3);
}

.line-number {
  font-size: var(--font-size-xs);
  color: var(--sage-gray);
  text-align: center;
  font-weight: 500;
}

.line-symbol {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.line-visual {
  width: 80px;
  height: 8px;
  position: relative;
}

.yang-line {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: var(--radius-sm);
  background: linear-gradient(90deg, var(--water-blue), var(--deep-ink));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.line-inner {
  width: 100%;
  height: 100%;
  background: inherit;
  border-radius: inherit;
}

.yin-line {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
}

.yin-left,
.yin-right {
  flex: 1;
  height: 100%;
  background: linear-gradient(90deg, var(--water-blue), var(--deep-ink));
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.yin-gap {
  width: 16px;
  height: 100%;
}

.dong-marker {
  position: absolute;
  right: -30px;
  font-size: var(--font-size-sm);
  color: var(--earth-yellow);
  font-weight: bold;
}

.line-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
}

.line-qin {
  color: var(--water-blue);
  font-weight: 500;
}

.line-gan-zhi {
  color: var(--sage-gray);
  font-family: 'SF Mono', 'Monaco', monospace;
}

.shi-marker,
.ying-marker {
  background: var(--mountain-green);
  color: white;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-size: 10px;
  font-weight: bold;
}

.ying-marker {
  background: var(--fire-red);
}

.line-god {
  text-align: center;
}

.god-name {
  font-size: var(--font-size-xs);
  color: var(--sage-gray);
  writing-mode: vertical-rl;
  text-orientation: upright;
}

/* 变卦信息 */
.bian-meta {
  text-align: center;
  margin-top: var(--space-4);
  padding-top: var(--space-3);
  border-top: var(--border-light);
}

.bian-name {
  font-weight: 500;
  color: var(--ink-dark);
  margin-right: var(--space-2);
}

.bian-type {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  background: var(--cloud-gray);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

/* 时间信息 */
.gua-timing {
  background: var(--soft-white);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  margin-bottom: var(--space-4);
}

.timing-info h4 {
  font-size: var(--font-size-base);
  color: var(--ink-dark);
  margin-bottom: var(--space-2);
}

.timing-details {
  font-size: var(--font-size-sm);
  color: var(--sage-gray);
  line-height: 1.6;
}

.solar-time {
  margin-bottom: var(--space-1);
}

.xun-kong {
  margin-left: var(--space-2);
  color: var(--earth-yellow);
}

/* 详细信息 */
.gua-details {
  display: flex;
  gap: var(--space-6);
}

.detail-section {
  flex: 1;
}

.detail-section h4 {
  font-size: var(--font-size-sm);
  color: var(--ink-dark);
  margin-bottom: var(--space-2);
}

.params-display {
  font-family: 'SF Mono', 'Monaco', monospace;
  background: var(--cloud-gray);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

.dong-yao-list {
  display: flex;
  gap: var(--space-2);
}

.dong-yao-item {
  background: var(--earth-yellow);
  color: white;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

/* 空状态 */
.empty-gua {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: var(--soft-white);
  border-radius: var(--radius-xl);
  border: 2px dashed var(--mist-gray);
}

.empty-content {
  text-align: center;
  color: var(--sage-gray);
}

.empty-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto var(--space-3) auto;
}

.empty-text {
  font-size: var(--font-size-base);
}

/* 响应式 */
@media (max-width: 768px) {
  .gua-diagram {
    flex-direction: column;
    gap: var(--space-4);
  }
  
  .gua-line {
    grid-template-columns: 20px 1fr 100px 50px;
    gap: var(--space-2);
  }
  
  .line-visual {
    width: 60px;
  }
  
  .gua-details {
    flex-direction: column;
    gap: var(--space-3);
  }
}
</style>
