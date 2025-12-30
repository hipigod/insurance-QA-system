<template>
  <div class="history-container">
    <!-- 头部 -->
    <div class="history-header">
      <el-button
        circle
        @click="goBack"
      >
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>练习历史</h2>
      <el-button
        type="danger"
        size="small"
        @click="clearHistory"
      >
        清空历史
      </el-button>
    </div>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <div v-if="historyList.length === 0" class="empty-state">
        <el-empty description="暂无练习记录">
          <el-button type="primary" @click="startPractice">开始练习</el-button>
        </el-empty>
      </div>

      <div v-else class="history-list">
        <el-card
          v-for="record in historyList"
          :key="record.id"
          class="history-card"
          shadow="hover"
          @click="viewDetail(record)"
        >
          <div class="card-header">
            <div class="record-info">
              <div class="record-title">{{ record.role_name }} - {{ record.product_name }}</div>
              <div class="record-time">{{ formatTime(record.created_at) }}</div>
            </div>
            <div class="record-score">
              <div class="score-number" :class="getScoreClass(record.total_score)">
                {{ record.total_score }}
              </div>
              <div class="score-label">分</div>
            </div>
          </div>
        </el-card>
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 数据
const historyList = ref([])

// 方法
const goBack = () => {
  router.push('/')
}

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')

  return `${date.getFullYear()}-${month}-${day} ${hours}:${minutes}`
}

const getScoreClass = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 60) return 'pass'
  return 'fail'
}

const viewDetail = (record) => {
  // 将记录保存到sessionStorage并跳转到结果页面
  sessionStorage.setItem('score_result', JSON.stringify(record.score_data))
  sessionStorage.setItem('dialogue_history', JSON.stringify(record.dialogue_data))
  sessionStorage.setItem('role_name', record.role_name)
  sessionStorage.setItem('product_name', record.product_name)
  sessionStorage.setItem('from_history', 'true')

  router.push('/result')
}

const startPractice = () => {
  router.push('/')
}

const clearHistory = () => {
  ElMessageBox.confirm(
    '确定要清空所有练习记录吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    localStorage.removeItem('practice_history')
    historyList.value = []
    ElMessage.success('已清空历史记录')
  }).catch(() => {})
}

// 生命周期
onMounted(() => {
  const history = localStorage.getItem('practice_history')

  if (history) {
    try {
      historyList.value = JSON.parse(history)
    } catch (e) {
      console.error('解析历史记录失败:', e)
    }
  }
})
</script>

<style scoped>
.history-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.history-header h2 {
  margin: 0;
  font-size: 20px;
}

.main-content {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px 40px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.history-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-info {
  flex: 1;
}

.record-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.record-time {
  font-size: 14px;
  color: #909399;
}

.record-score {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.score-number {
  font-size: 36px;
  font-weight: bold;
}

.score-number.excellent { color: #67c23a; }
.score-number.good { color: #409eff; }
.score-number.pass { color: #e6a23c; }
.score-number.fail { color: #f56c6c; }

.score-label {
  font-size: 14px;
  color: #606266;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .main-content {
    padding: 0 16px 20px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .record-score {
    align-self: flex-end;
  }
}
</style>
