<template>
  <div class="data-export">
    <el-card shadow="never">
      <h3>导出练习记录</h3>
      <p class="tip">将LocalStorage中的练习记录导出为文件</p>

      <el-space direction="vertical" style="width: 100%">
        <el-button type="primary" @click="exportData('json')" :icon="Download">
          导出为JSON
        </el-button>
        <el-button type="success" @click="exportData('excel')" :icon="Download">
          导出为Excel(CSV)
        </el-button>
      </el-space>

      <el-divider />

      <h3>导入练习记录</h3>
      <p class="tip">从之前导出的JSON文件恢复数据</p>

      <el-upload
        :auto-upload="false"
        :on-change="importData"
        :show-file-list="false"
        accept=".json"
      >
        <el-button type="warning" :icon="Upload">
          选择JSON文件导入
        </el-button>
      </el-upload>
    </el-card>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { Download, Upload } from '@element-plus/icons-vue'

const exportData = (format) => {
  try {
    const history = JSON.parse(localStorage.getItem('practice_history') || '[]')

    if (history.length === 0) {
      ElMessage.warning('暂无练习记录')
      return
    }

    let content, filename, type

    if (format === 'json') {
      content = JSON.stringify(history, null, 2)
      filename = `practice_history_${new Date().toISOString().slice(0, 10)}.json`
      type = 'application/json'
    } else if (format === 'excel') {
      // 简单CSV导出
      const headers = ['时间', '角色', '产品', '总分', '对话轮数']
      const rows = history.map(record => [
        record.created_at,
        record.role_name,
        record.product_name,
        record.total_score,
        record.dialogue_rounds || 0
      ])
      content = [headers, ...rows].map(row => row.join(',')).join('\n')
      filename = `practice_history_${new Date().toISOString().slice(0, 10)}.csv`
      type = 'text/csv'
    }

    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)

    ElMessage.success(`成功导出${history.length}条记录`)
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const importData = (file) => {
  const reader = new FileReader()

  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result)

      if (!Array.isArray(data)) {
        throw new Error('格式错误')
      }

      localStorage.setItem('practice_history', JSON.stringify(data))
      ElMessage.success(`成功导入${data.length}条记录`)
    } catch (error) {
      ElMessage.error('文件格式错误,请选择正确的JSON文件')
    }
  }

  reader.readAsText(file.raw)
}
</script>

<style scoped>
.tip {
  color: #909399;
  margin-bottom: 16px;
}

h3 {
  margin-bottom: 8px;
}
</style>
