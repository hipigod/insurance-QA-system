<template>
  <div class="model-management">
    <div class="tab-header">
      <el-button type="primary" @click="showDialog()">
        <el-icon><Plus /></el-icon>
        新增模型
      </el-button>
      <span class="header-tip">配置保存到服务器 data/model_config.json，练习开始时可选</span>
    </div>

    <el-table :data="models" style="width: 100%" v-loading="loading">
      <el-table-column prop="model_name" label="模型名称" min-width="160" />
      <el-table-column prop="provider" label="提供商" width="140" />
      <el-table-column prop="api_base" label="API地址" show-overflow-tooltip />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button
            size="small"
            :type="row.is_active ? 'warning' : 'success'"
            @click="toggleActive(row)"
          >
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
          <el-button size="small" type="primary" plain :loading="testingId === row.id" @click="handleTest(row)">
            测试
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 模型配置对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑模型' : '新增模型'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="模型名称" required>
          <el-input v-model="form.model_name" placeholder="模型ID，例如: qwen-plus / deepseek-chat" />
        </el-form-item>
        <el-form-item label="提供商">
          <el-input v-model="form.provider" placeholder="例如: 阿里云 / DeepSeek" />
        </el-form-item>
        <el-form-item label="API Key" required>
          <el-input v-model="form.api_key" type="password" placeholder="请输入API Key" show-password />
        </el-form-item>
        <el-form-item label="API地址">
          <el-input v-model="form.api_base" placeholder="例如: https://dashscope.aliyuncs.com/compatible-mode/v1" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import * as api from '@/api/modules'

// 数据
const models = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const form = ref({})
const testingId = ref(null)

// 加载模型列表
const loadData = async () => {
  try {
    loading.value = true
    const response = await api.getModels()
    models.value = response || []
  } catch (error) {
    console.error('加载模型失败:', error)
    ElMessage.error('加载模型失败')
  } finally {
    loading.value = false
  }
}

// 显示对话框
const showDialog = (model = null) => {
  if (model) {
    // 编辑：回填除api_key外的字段（后端不回传密钥）
    form.value = {
      id: model.id,
      model_name: model.model_name,
      provider: model.provider || '',
      api_key: '',
      api_base: model.api_base || '',
      is_active: model.is_active
    }
  } else {
    form.value = {
      model_name: '',
      provider: '',
      api_key: '',
      api_base: '',
      is_active: true
    }
  }
  dialogVisible.value = true
}

// 保存模型
const handleSave = async () => {
  if (!form.value.model_name || !form.value.model_name.trim()) {
    ElMessage.warning('请填写模型名称')
    return
  }

  const payload = { ...form.value }
  delete payload.id

  try {
    saving.value = true

    if (form.value.id) {
      // 编辑时api_key留空表示不修改
      if (!payload.api_key) delete payload.api_key
      await api.updateModel(form.value.id, payload)
      ElMessage.success('更新成功')
    } else {
      if (!payload.api_key) {
        ElMessage.warning('请填写API Key')
        return
      }
      await api.createModel(payload)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    await loadData()
  } catch (error) {
    console.error('保存模型失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

// 删除模型
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个模型配置吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteModel(id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除模型失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 切换启用状态
const toggleActive = async (model) => {
  try {
    const nextActive = !model.is_active
    await api.updateModel(model.id, { is_active: nextActive })
    ElMessage.success(nextActive ? '已启用' : '已禁用')
    await loadData()
  } catch (error) {
    console.error('切换状态失败:', error)
    ElMessage.error('操作失败')
  }
}

// 测试连通性
const handleTest = async (model) => {
  try {
    testingId.value = model.id
    const res = await api.testModel(model.id)
    if (res && res.success) {
      ElMessage.success(`${model.model_name} 连接成功`)
    } else {
      ElMessage.error(`${model.model_name} 连接失败，请检查配置`)
    }
  } catch (error) {
    console.error('测试失败:', error)
    ElMessage.error('测试请求失败')
  } finally {
    testingId.value = null
  }
}

// 生命周期
onMounted(() => {
  loadData()
})

// 暴露方法给父组件
defineExpose({
  loadData
})
</script>

<style scoped>
.tab-header {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-tip {
  font-size: 12px;
  color: #909399;
}
</style>
