<template>
  <div class="product-management">
    <div class="tab-header">
      <el-button type="primary" @click="showDialog()">
        <el-icon><Plus /></el-icon>
        新增产品
      </el-button>
    </div>

    <el-table :data="products" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="产品名称" width="180" />
      <el-table-column prop="product_type" label="类型" width="120" />
      <el-table-column prop="description" label="简介" />
      <el-table-column prop="premium_range" label="保费范围" width="120" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 产品编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑产品' : '新增产品'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品名称">
          <el-input v-model="form.name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-select v-model="form.product_type" placeholder="请选择产品类型">
            <el-option label="人寿保险" value="人寿保险" />
            <el-option label="健康保险" value="健康保险" />
            <el-option label="意外保险" value="意外保险" />
            <el-option label="财产保险" value="财产保险" />
          </el-select>
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入产品简介" />
        </el-form-item>
        <el-form-item label="保障范围">
          <el-input v-model="form.coverage" type="textarea" :rows="3" placeholder="请输入保障范围" />
        </el-form-item>
        <el-form-item label="保费范围">
          <el-input v-model="form.premium_range" placeholder="例如: 1000-10000元/年" />
        </el-form-item>
        <el-form-item label="目标人群">
          <el-input v-model="form.target_audience" placeholder="例如: 25-45岁中年人" />
        </el-form-item>
        <el-form-item label="详细信息">
          <el-input v-model="form.detailed_info" type="textarea" :rows="6" placeholder="请输入详细信息" />
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

const products = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const form = ref({})

const loadData = async () => {
  try {
    loading.value = true
    const response = await api.getProducts()
    products.value = response || []
  } catch (error) {
    console.error('加载产品失败:', error)
    ElMessage.error('加载产品失败')
  } finally {
    loading.value = false
  }
}

const showDialog = (product = null) => {
  if (product) {
    form.value = { ...product }
  } else {
    form.value = {
      name: '',
      product_type: '人寿保险',
      description: '',
      coverage: '',
      premium_range: '',
      target_audience: '',
      detailed_info: ''
    }
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  try {
    saving.value = true
    if (form.value.id) {
      await api.updateProduct(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await api.createProduct(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadData()
  } catch (error) {
    console.error('保存产品失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个产品吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await api.deleteProduct(id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除产品失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadData()
})

defineExpose({
  loadData
})
</script>

<style scoped>
.tab-header {
  margin-bottom: 16px;
}
</style>
