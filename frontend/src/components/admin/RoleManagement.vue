<template>
  <div class="role-management">
    <div class="tab-header">
      <el-button type="primary" @click="showDialog()">
        <el-icon><Plus /></el-icon>
        新增角色
      </el-button>
    </div>

    <el-table :data="roles" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="角色名称" width="150" />
      <el-table-column prop="description" label="简介" />
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-tag :type="getDifficultyType(row.difficulty)">
            {{ row.difficulty }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 角色编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑角色' : '新增角色'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="角色名称">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入角色简介" />
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.difficulty" placeholder="请选择难度">
            <el-option label="简单" value="简单" />
            <el-option label="普通" value="普通" />
            <el-option label="困难" value="困难" />
            <el-option label="专家" value="专家" />
          </el-select>
        </el-form-item>
        <el-form-item label="系统提示词">
          <el-input v-model="form.system_prompt" type="textarea" :rows="8" placeholder="请输入系统提示词" />
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
const roles = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const form = ref({})

// 加载角色列表
const loadData = async () => {
  try {
    loading.value = true
    const response = await api.getRoles()
    roles.value = response.data || []
  } catch (error) {
    console.error('加载角色失败:', error)
    ElMessage.error('加载角色失败')
  } finally {
    loading.value = false
  }
}

// 显示对话框
const showDialog = (role = null) => {
  if (role) {
    form.value = { ...role }
  } else {
    form.value = {
      name: '',
      description: '',
      difficulty: '普通',
      system_prompt: ''
    }
  }
  dialogVisible.value = true
}

// 保存角色
const handleSave = async () => {
  try {
    saving.value = true

    if (form.value.id) {
      await api.updateRole(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await api.createRole(form.value)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    await loadData()
  } catch (error) {
    console.error('保存角色失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

// 删除角色
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个角色吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteRole(id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除角色失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 获取难度标签类型
const getDifficultyType = (difficulty) => {
  const map = {
    '简单': 'success',
    '普通': 'info',
    '困难': 'danger',
    '专家': 'warning'
  }
  return map[difficulty] || 'info'
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
}

.weight-summary {
  margin-top: 16px;
  text-align: right;
}
</style>
