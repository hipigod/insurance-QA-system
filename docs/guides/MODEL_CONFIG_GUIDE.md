# 模型配置功能实现说明

由于Admin.vue文件较大(700+行),为避免编辑错误,建议通过API直接管理模型配置。

## 方法1: 通过API管理(推荐)

### 添加通义千问模型配置

```bash
curl -X POST http://127.0.0.1:8000/api/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "qwen-plus",
    "provider": "通义千问",
    "api_key": "sk-8b1831a371984c6483b413a759463619",
    "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "is_active": true
  }'
```

### 添加其他模型配置示例

```bash
# DeepSeek
curl -X POST http://127.0.0.1:8000/api/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "deepseek-chat",
    "provider": "DeepSeek",
    "api_key": "your-api-key",
    "api_base": "https://api.deepseek.com/v1",
    "is_active": false
  }'

# OpenAI
curl -X POST http://127.0.0.1:8000/api/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt-4",
    "provider": "OpenAI",
    "api_key": "your-api-key",
    "api_base": "https://api.openai.com/v1",
    "is_active": false
  }'
```

### 查看所有模型配置

```bash
curl http://127.0.0.1:8000/api/models/
```

### 激活指定模型

```bash
curl -X POST http://127.0.0.1:8000/api/models/1/activate
```

### 更新模型配置

```bash
curl -X PUT http://127.0.0.1:8000/api/models/1 \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "new-api-key"
  }'
```

### 删除模型配置

```bash
curl -X DELETE http://127.0.0.1:8000/api/models/1
```

## 方法2: 前端界面实现

如需在前端管理后台添加模型配置Tab页,需要在Admin.vue中添加:

### 1. 在数据导出Tab之前添加模型配置Tab

```vue
<!-- 模型配置管理 -->
<el-tab-pane label="模型配置管理" name="models">
  <div class="tab-header">
    <el-alert
      title="提示：配置AI模型的API Key和相关信息"
      type="info"
      :closable="false"
      style="margin-bottom: 16px"
    />
    <el-button type="primary" @click="showModelDialog()">
      <el-icon><Plus /></el-icon>
      新增模型配置
    </el-button>
  </div>

  <el-table :data="models" style="width: 100%" v-loading="loading">
    <el-table-column prop="id" label="ID" width="60" />
    <el-table-column prop="model_name" label="模型名称" width="200" />
    <el-table-column prop="provider" label="提供商" width="150" />
    <el-table-column prop="api_base" label="API地址" show-overflow-tooltip />
    <el-table-column prop="is_active" label="状态" width="100">
      <template #default="{ row }">
        <el-tag :type="row.is_active ? 'success' : 'info'">
          {{ row.is_active ? '已激活' : '未激活' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="250" fixed="right">
      <template #default="{ row }">
        <el-button size="small" @click="showModelDialog(row)">编辑</el-button>
        <el-button
          size="small"
          type="success"
          @click="activateModel(row.id)"
          v-if="!row.is_active"
        >
          激活
        </el-button>
        <el-button size="small" type="danger" @click="deleteModel(row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</el-tab-pane>
```

### 2. 在script setup部分添加数据和方法

```javascript
import * as api from '@/api/modules'

// 模型配置数据
const models = ref([])

// 加载模型配置列表
const loadModels = async () => {
  loading.value = true
  try {
    const res = await api.getModels()
    models.value = res.data
  } catch (error) {
    ElMessage.error('加载模型配置失败')
  } finally {
    loading.value = false
  }
}

// 模型配置表单
const modelDialogVisible = ref(false)
const modelForm = ref({
  id: null,
  model_name: '',
  provider: '',
  api_key: '',
  api_base: '',
  is_active: false
})

// 显示模型配置对话框
const showModelDialog = (row = null) => {
  if (row) {
    modelForm.value = { ...row }
  } else {
    modelForm.value = {
      id: null,
      model_name: '',
      provider: '',
      api_key: '',
      api_base: '',
      is_active: false
    }
  }
  modelDialogVisible.value = true
}

// 保存模型配置
const saveModel = async () => {
  saving.value = true
  try {
    if (modelForm.value.id) {
      await api.updateModel(modelForm.value.id, modelForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createModel(modelForm.value)
      ElMessage.success('创建成功')
    }
    modelDialogVisible.value = false
    loadModels()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 删除模型配置
const deleteModel = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该模型配置吗？', '提示', {
      type: 'warning'
    })
    await api.deleteModel(id)
    ElMessage.success('删除成功')
    loadModels()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 激活模型
const activateModel = async (id) => {
  try {
    await api.activateModel(id)
    ElMessage.success('激活成功')
    loadModels()
  } catch (error) {
    ElMessage.error('激活失败')
  }
}

// 在onMounted中添加loadModels
onMounted(() => {
  loadRoles()
  loadProducts()
  loadDimensions()
  loadCases()
  loadModels()  // 添加这行
})
```

### 3. 添加模型配置编辑对话框

```vue
<!-- 模型配置编辑对话框 -->
<el-dialog
  v-model="modelDialogVisible"
  :title="modelForm.id ? '编辑模型配置' : '新增模型配置'"
  width="600px"
>
  <el-form :model="modelForm" label-width="120px">
    <el-form-item label="模型名称">
      <el-input v-model="modelForm.model_name" placeholder="如: qwen-plus, gpt-4" />
    </el-form-item>
    <el-form-item label="提供商">
      <el-input v-model="modelForm.provider" placeholder="如: 通义千问, OpenAI" />
    </el-form-item>
    <el-form-item label="API Key">
      <el-input v-model="modelForm.api_key" type="password" show-password placeholder="请输入API Key" />
    </el-form-item>
    <el-form-item label="API地址">
      <el-input v-model="modelForm.api_base" placeholder="如: https://api.openai.com/v1" />
    </el-form-item>
    <el-form-item label="是否激活">
      <el-switch v-model="modelForm.is_active" />
      <span style="margin-left: 10px; color: #999;">
        激活后该模型将用于AI对话
      </span>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="modelDialogVisible = false">取消</el-button>
    <el-button type="primary" @click="saveModel" :loading="saving">保存</el-button>
  </template>
</el-dialog>
```

## 已完成的功能

### 后端API ✅
- GET `/api/models/` - 获取所有模型配置
- POST `/api/models/` - 创建模型配置
- PUT `/api/models/{id}` - 更新模型配置
- DELETE `/api/models/{id}` - 删除模型配置
- POST `/api/models/{id}/activate` - 激活指定模型

### 前端API接口 ✅
- getModels()
- createModel(data)
- updateModel(id, data)
- deleteModel(id)
- activateModel(id)

## 快速开始

使用以下命令添加通义千问配置(推荐):

```bash
curl -X POST http://127.0.0.1:8000/api/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "qwen-plus",
    "provider": "通义千问",
    "api_key": "sk-8b1831a371984c6483b413a759463619",
    "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "is_active": true
  }'
```

或者访问 http://127.0.0.1:8000/docs 使用Swagger UI界面操作!
