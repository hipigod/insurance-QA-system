<template>
  <div class="result-container">
    <!-- 头部 -->
    <div class="result-header">
      <el-button
        circle
        @click="goBack"
      >
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>练习评分报告</h2>
      <div></div>
    </div>

    <!-- 主体内容 -->
    <el-main class="main-content" v-loading="loading">
      <!-- 总分卡片 -->
      <el-card class="score-card" shadow="hover">
        <div class="total-score">
          <div class="score-circle">
            <div class="score-number">{{ scoreResult.total_score }}</div>
            <div class="score-label">总分</div>
          </div>
          <div class="score-level" :class="getScoreLevel(scoreResult.total_score).class">
            {{ getScoreLevel(scoreResult.total_score).text }}
          </div>
        </div>
      </el-card>

      <!-- 维度评分 -->
      <el-card class="dimension-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><TrendCharts /></el-icon>
            <span>维度评分</span>
          </div>
        </template>

        <div class="dimension-list">
          <div
            v-for="(item, key) in scoreResult.dimension_scores"
            :key="key"
            class="dimension-item"
          >
            <div class="dimension-header">
              <span class="dimension-name">{{ key }}</span>
              <span class="dimension-score">{{ item.score }}分</span>
            </div>
            <el-progress
              :percentage="item.score"
              :color="getProgressColor(item.score)"
              :show-text="false"
            />
            <div class="dimension-evaluation">{{ item.evaluation }}</div>
          </div>
        </div>
      </el-card>

      <!-- 异议识别 -->
      <el-card class="objection-card" shadow="hover" v-if="scoreResult.objection_tags?.length">
        <template #header>
          <div class="card-header">
            <el-icon><PriceTag /></el-icon>
            <span>异议识别</span>
          </div>
        </template>

        <div class="objection-tags">
          <el-tag
            v-for="(tag, index) in scoreResult.objection_tags"
            :key="index"
            type="warning"
            size="large"
            class="objection-tag"
          >
            {{ tag }}
          </el-tag>
        </div>
      </el-card>

      <!-- 优秀案例对比 -->
      <el-card class="case-card" shadow="hover" v-if="scoreResult.excellent_cases?.length">
        <template #header>
          <div class="card-header">
            <el-icon><Medal /></el-icon>
            <span>优秀案例学习</span>
          </div>
        </template>

        <div class="case-list">
          <div
            v-for="(case_item, index) in scoreResult.excellent_cases"
            :key="index"
            class="case-item"
          >
            <div class="case-weakness">
              <el-tag type="danger" size="small">{{ case_item.薄弱环节 }}</el-tag>
            </div>
            <div class="case-content">{{ case_item.案例片段 }}</div>
          </div>
        </div>
      </el-card>

      <!-- 总体评价 -->
      <el-card class="evaluation-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Document /></el-icon>
            <span>总体评价</span>
          </div>
        </template>

        <div class="evaluation-content">
          {{ scoreResult.overall_evaluation }}
        </div>
      </el-card>

      <!-- 对话记录 -->
      <el-card class="dialogue-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><ChatDotRound /></el-icon>
            <span>对话记录</span>
          </div>
        </template>

        <div class="dialogue-history">
          <div
            v-for="(msg, index) in dialogueHistory"
            :key="index"
            class="history-message"
            :class="msg.role"
          >
            <div class="message-label">
              {{ msg.role === 'user' ? '销售' : '客户' }}
            </div>
            <div class="message-text">{{ msg.content }}</div>
          </div>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          @click="practiceAgain"
        >
          <el-icon><RefreshRight /></el-icon>
          再次练习
        </el-button>
        <el-button
          size="large"
          @click="viewHistory"
        >
          <el-icon><Clock /></el-icon>
          查看历史
        </el-button>
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 数据
const scoreResult = ref({})
const dialogueHistory = ref([])
const loading = ref(false)

// 方法
const getScoreLevel = (score) => {
  if (score >= 90) return { text: '优秀', class: 'excellent' }
  if (score >= 80) return { text: '良好', class: 'good' }
  if (score >= 60) return { text: '合格', class: 'pass' }
  return { text: '需改进', class: 'fail' }
}

const getProgressColor = (score) => {
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#409eff'
  if (score >= 60) return '#e6a23c'
  return '#f56c6c'
}

const goBack = () => {
  router.push('/')
}

const practiceAgain = () => {
  // 清除sessionStorage
  sessionStorage.clear()
  router.push('/')
}

const viewHistory = () => {
  router.push('/history')
}

// 生命周期
onMounted(() => {
  // 从sessionStorage获取数据
  const scoreData = sessionStorage.getItem('score_result')
  const historyData = sessionStorage.getItem('dialogue_history')

  if (!scoreData || !historyData) {
    ElMessage.error('数据丢失，请重新开始')
    router.push('/')
    return
  }

  scoreResult.value = JSON.parse(scoreData)
  dialogueHistory.value = JSON.parse(historyData)

  // 保存到LocalStorage作为历史记录
  const record = {
    id: Date.now(),
    role_name: sessionStorage.getItem('role_name'),
    product_name: sessionStorage.getItem('product_name'),
    total_score: scoreResult.value.total_score,
    dialogue_data: dialogueHistory.value,
    score_data: scoreResult.value,
    created_at: new Date().toISOString()
  }

  // 获取现有历史记录
  const history = JSON.parse(localStorage.getItem('practice_history') || '[]')
  history.unshift(record)

  // 只保留最近10条
  if (history.length > 10) {
    history.splice(10)
  }

  localStorage.setItem('practice_history', JSON.stringify(history))
})
</script>

<style scoped>
.result-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-header h2 {
  margin: 0;
  font-size: 20px;
}

.main-content {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px 40px;
}

.score-card {
  margin-bottom: 20px;
  text-align: center;
  border-radius: 12px;
}

.total-score {
  padding: 20px 0;
}

.score-circle {
  width: 150px;
  height: 150px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.score-number {
  font-size: 48px;
  font-weight: bold;
}

.score-label {
  font-size: 14px;
  opacity: 0.9;
}

.score-level {
  font-size: 24px;
  font-weight: bold;
  margin-top: 16px;
}

.score-level.excellent { color: #67c23a; }
.score-level.good { color: #409eff; }
.score-level.pass { color: #e6a23c; }
.score-level.fail { color: #f56c6c; }

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.dimension-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dimension-item {
  padding: 16px;
  background: #f9fafc;
  border-radius: 8px;
}

.dimension-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.dimension-name {
  font-weight: bold;
  font-size: 16px;
}

.dimension-score {
  color: #409eff;
  font-weight: bold;
  font-size: 18px;
}

.dimension-evaluation {
  margin-top: 12px;
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.objection-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.objection-tag {
  font-size: 14px;
}

.case-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.case-item {
  padding: 16px;
  background: #f9fafc;
  border-radius: 8px;
}

.case-weakness {
  margin-bottom: 12px;
}

.case-content {
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.evaluation-content {
  color: #606266;
  line-height: 1.8;
  font-size: 15px;
  white-space: pre-wrap;
}

.dialogue-history {
  max-height: 400px;
  overflow-y: auto;
}

.history-message {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
  background: #f9fafc;
}

.history-message.user {
  background: #eef6ff;
}

.message-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}

.message-text {
  color: #303133;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 40px;
}

.action-buttons .el-button {
  min-width: 150px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .main-content {
    padding: 0 16px 20px;
  }

  .score-circle {
    width: 120px;
    height: 120px;
  }

  .score-number {
    font-size: 36px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}
</style>
