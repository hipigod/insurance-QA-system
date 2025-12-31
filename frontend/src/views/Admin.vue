<template>
  <div class="admin-container">
    <!-- 头部 -->
    <div class="admin-header">
      <el-button circle @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>管理后台</h2>
      <div></div>
    </div>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 角色管理 - 使用组件 -->
        <el-tab-pane label="客户角色管理" name="roles">
          <RoleManagement ref="roleManagementRef" />
        </el-tab-pane>

        <!-- 产品管理 - 使用组件 -->
        <el-tab-pane label="保险产品管理" name="products">
          <ProductManagement ref="productManagementRef" />
        </el-tab-pane>

        <!-- 评分维度管理 - 保留原代码 -->
        <el-tab-pane label="评分维度管理" name="dimensions">
          <div class="tab-header">
            <el-alert
              title="提示:各维度权重之和必须等于100%"
              type="info"
              :closable="false"
              style="margin-bottom: 16px"
            />
            <el-button type="primary" @click="showDimensionDialog()">
              <el-icon><Plus /></el-icon>
              新增维度
            </el-button>
          </div>

          <el-table :data="dimensions" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="维度名称" width="150" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="weight" label="权重(%)" width="100">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.weight"
                  :min="0"
                  :max="100"
                  size="small"
                  @change="updateDimensionWeight(row)"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showDimensionDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteDimension(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="weight-summary">
            <el-tag :type="totalWeight === 100 ? 'success' : 'danger'">
              当前总权重: {{ totalWeight }}%
            </el-tag>
          </div>
        </el-tab-pane>

        <!-- 优秀案例库 - 保留原代码 -->
        <el-tab-pane label="优秀案例库" name="cases">
          <div class="tab-header">
            <el-button type="primary" @click="showCaseDialog()">
              <el-icon><Plus /></el-icon>
              新增案例
            </el-button>
          </div>

          <el-table :data="cases" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="weakness_type" label="弱项类型" width="150" />
            <el-table-column prop="case_content" label="案例内容" show-overflow-tooltip />
            <el-table-column prop="dialogue_node" label="对话节点" width="150" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showCaseDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteCase(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 模型配置管理 - 使用组件 -->
        <el-tab-pane label="模型配置管理" name="models">
          <ModelManagement ref="modelManagementRef" />
        </el-tab-pane>

        <!-- 数据导出 - 使用组件 -->
        <el-tab-pane label="数据导出" name="export">
          <DataExport />
        </el-tab-pane>
      </el-tabs>
    </el-main>

    <!-- 评分维度编辑对话框 -->
    <el-dialog
      v-model="dimensionDialogVisible"
      :title="dimensionForm.id ? '编辑维度' : '新增维度'"
      width="600px"
    >
      <el-form :model="dimensionForm" label-width="100px">
        <el-form-item label="维度名称">
          <el-input v-model="dimensionForm.name" placeholder="例如: 需求挖掘" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="dimensionForm.description" type="textarea" :rows="3" placeholder="请输入维度描述" />
        </el-form-item>
        <el-form-item label="权重(%)">
          <el-input-number v-model="dimensionForm.weight" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="评价提示词">
          <el-input v-model="dimensionForm.evaluation_prompt" type="textarea" :rows="6" placeholder="请输入评价提示词" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dimensionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDimension" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 案例编辑对话框 -->
    <el-dialog
      v-model="caseDialogVisible"
      :title="caseForm.id ? '编辑案例' : '新增案例'"
      width="600px"
    >
      <el-form :model="caseForm" label-width="100px">
        <el-form-item label="弱项类型">
          <el-input v-model="caseForm.weakness_type" placeholder="例如: 需求挖掘" />
        </el-form-item>
        <el-form-item label="对话节点">
          <el-select v-model="caseForm.dialogue_node" placeholder="请选择对话节点">
            <el-option label="开场" value="开场" />
            <el-option label="需求挖掘" value="需求挖掘" />
            <el-option label="产品说明" value="产品说明" />
            <el-option label="异议处理" value="异议处理" />
            <el-option label="促成" value="促成" />
          </el-select>
        </el-form-item>
        <el-form-item label="案例内容">
          <el-input v-model="caseForm.case_content" type="textarea" :rows="8" placeholder="请输入案例内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="caseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCase" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, ArrowLeft } from '@element-plus/icons-vue'
import * as api from '@/api/modules'
import RoleManagement from '@/components/admin/RoleManagement.vue'
import ProductManagement from '@/components/admin/ProductManagement.vue'
import ModelManagement from '@/components/admin/ModelManagement.vue'
import DataExport from '@/components/admin/DataExport.vue'

const router = useRouter()

// 引用组件
const roleManagementRef = ref(null)
const productManagementRef = ref(null)
const modelManagementRef = ref(null)

// 数据
const activeTab = ref('roles')
const loading = ref(false)
const saving = ref(false)
const dimensions = ref([])
const cases = ref([])

// 对话框状态
const dimensionDialogVisible = ref(false)
const caseDialogVisible = ref(false)

// 表单数据
const dimensionForm = ref({})
const caseForm = ref({})

// 计算总权重
const totalWeight = computed(() => {
  return dimensions.value.reduce((sum, d) => sum + (d.weight || 0), 0)
})

// 方法
const goBack = () => {
  router.push('/')
}

// ========== 评分维度管理 ==========
const loadDimensions = async () => {
  try {
    loading.value = true
    const response = await api.getDimensions()
    dimensions.value = response || []
  } catch (error) {
    console.error('加载维度失败:', error)
    ElMessage.error('加载维度失败')
  } finally {
    loading.value = false
  }
}

const showDimensionDialog = (dimension = null) => {
  if (dimension) {
    dimensionForm.value = { ...dimension }
  } else {
    dimensionForm.value = {
      name: '',
      description: '',
      weight: 25,
      evaluation_prompt: ''
    }
  }
  dimensionDialogVisible.value = true
}

const saveDimension = async () => {
  try {
    saving.value = true

    if (dimensionForm.value.id) {
      await api.updateDimension(dimensionForm.value.id, dimensionForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createDimension(dimensionForm.value)
      ElMessage.success('创建成功')
    }

    dimensionDialogVisible.value = false
    await loadDimensions()
  } catch (error) {
    console.error('保存维度失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const updateDimensionWeight = async (dimension) => {
  try {
    await api.updateDimension(dimension.id, { weight: dimension.weight })
    ElMessage.success('权重更新成功')
  } catch (error) {
    console.error('更新权重失败:', error)
    ElMessage.error('更新权重失败')
  }
}

const deleteDimension = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个维度吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteDimension(id)
    ElMessage.success('删除成功')
    await loadDimensions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除维度失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// ========== 案例管理 ==========
const loadCases = async () => {
  try {
    loading.value = true
    const response = await api.getCases()
    cases.value = response || []
  } catch (error) {
    console.error('加载案例失败:', error)
    ElMessage.error('加载案例失败')
  } finally {
    loading.value = false
  }
}

const showCaseDialog = (case_item = null) => {
  if (case_item) {
    caseForm.value = { ...case_item }
  } else {
    caseForm.value = {
      weakness_type: '',
      case_content: '',
      dialogue_node: '开场'
    }
  }
  caseDialogVisible.value = true
}

const saveCase = async () => {
  try {
    saving.value = true

    if (caseForm.value.id) {
      await api.updateCase(caseForm.value.id, caseForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createCase(caseForm.value)
      ElMessage.success('创建成功')
    }

    caseDialogVisible.value = false
    await loadCases()
  } catch (error) {
    console.error('保存案例失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const deleteCase = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个案例吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteCase(id)
    ElMessage.success('删除成功')
    await loadCases()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除案例失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 生命周期 - 初始化数据
import { onMounted } from 'vue'
onMounted(() => {
  loadDimensions()
  loadCases()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.main-content {
  padding: 20px;
}

.tab-header {
  margin-bottom: 16px;
}

.weight-summary {
  margin-top: 16px;
  text-align: right;
}
</style>
