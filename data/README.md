# 训练数据说明

## 📁 目录结构

```
data/
├── raw/                    # 原始数据（未经处理的图片）
│   ├── identity_card/      # 身份證图片
│   ├── utility_bill/       # 水電費單图片
│   ├── bank_statement/     # 銀行賬單图片
│   ├── address_proof/      # 地址證明图片
│   ├── lease_agreement/    # 租約图片
│   └── other/              # 其他文檔图片
├── processed/              # 处理后的数据（用于训练）
│   ├── identity_card/
│   ├── utility_bill/
│   ├── bank_statement/
│   ├── address_proof/
│   ├── lease_agreement/
│   └── other/
└── labels/                 # 标签文件（可选）
```

## 📊 数据要求

### 每个类别建议的数据量
- **最少**: 每个类别 **50张** 图片（用于快速测试）
- **推荐**: 每个类别 **100-200张** 图片（用于正式训练）
- **理想**: 每个类别 **200-500张** 图片（获得更好的准确率）

### 图片要求
- **格式**: PNG, JPG, JPEG
- **分辨率**: 至少 224x224 像素（推荐 512x512 或更高）
- **质量**: 图片清晰，文字可读
- **内容**: 完整的文档图片，不要过度裁剪

### 数据多样性
为了获得更好的模型性能，建议包含：
- ✅ 不同的光照条件（明亮、昏暗、阴影）
- ✅ 不同的角度（正面、轻微倾斜）
- ✅ 不同的背景（白色、灰色、彩色）
- ✅ 不同的文档布局和样式
- ✅ 不同字体大小和样式

## 🚀 如何准备数据

### 方法1: 手动准备（推荐用于真实数据）

1. **收集图片**
   - 使用手机或相机拍摄文档照片
   - 或从公开数据集下载
   - ⚠️ **注意隐私**: 不要使用包含真实敏感信息的图片

2. **组织图片**
   ```bash
   # 将图片放入对应的类别文件夹
   # 例如，将身份證图片放入:
   data/raw/identity_card/
   ```

3. **运行预处理**
   ```bash
   cd model_training
   python data_preprocessing.py
   ```
   这会将 `raw/` 中的数据整理到 `processed/` 目录中。

### 方法2: 使用公开数据集

可以从以下来源获取数据：
- [Kaggle Document Classification](https://www.kaggle.com/datasets?search=document)
- [GitHub 文档数据集](https://github.com/topics/document-dataset)
- [Google Dataset Search](https://datasetsearch.research.google.com/)

下载后，按照类别分类并放入对应的 `raw/` 子目录中。

### 方法3: 使用合成数据（用于快速测试）

可以使用模板生成文档图片：
- 使用设计软件（如 Figma, Canva）创建文档模板
- 使用数据增强技术生成变体
- 确保合成数据看起来真实

## 📝 文档类型说明

### 1. identity_card (身份證)
- 香港身份证
- 护照
- 其他身份证明文件

### 2. utility_bill (水電費單)
- 电费单
- 水费单
- 煤气费单
- 电话费单

### 3. bank_statement (銀行賬單)
- 银行对账单
- 账户明细
- 信用卡账单

### 4. address_proof (地址證明)
- 住址证明
- 银行地址证明
- 政府发出的地址证明

### 5. lease_agreement (租約)
- 租赁合同
- 租约协议
- 租赁证明

### 6. other (其他)
- 不属于上述类别的文档
- 可以是收据、发票、通知书等

## ✅ 数据准备检查清单

在开始训练之前，请确认：

- [ ] 每个类别至少有 50 张图片（用于测试）或 100 张图片（用于正式训练）
- [ ] 所有图片都在 `data/raw/` 对应的类别文件夹中
- [ ] 图片格式为 PNG、JPG 或 JPEG
- [ ] 图片清晰可读
- [ ] 已运行数据预处理脚本
- [ ] `data/processed/` 中有处理后的数据

## 🔧 快速开始

### 步骤1: 检查数据分布
```bash
cd model_training
python data_preprocessing.py
```
这会显示每个类别的图片数量。

### 步骤2: 预处理图片（如果需要）
在 `data_preprocessing.py` 中取消注释预处理函数：
```python
preprocessor.preprocess_images()
```

### 步骤3: 数据增强（可选，推荐）
```python
preprocessor.augment_data(augment_per_image=3)
```
这可以为每张图片生成3个增强版本。

### 步骤4: 开始训练
```bash
python train.py
```

## ⚠️ 注意事项

1. **隐私保护**: 
   - 不要使用包含真实个人信息的图片
   - 训练数据应遮蔽敏感信息（姓名、身份证号、地址等）
   - 使用合成数据或公开数据时注意数据许可

2. **数据平衡**:
   - 尽量保持各类别数据量平衡
   - 如果某个类别数据过少，考虑使用数据增强

3. **数据质量**:
   - 确保图片清晰
   - 移除损坏或无法识别的图片
   - 确保标注正确

4. **版本控制**:
   - 不要在 Git 中提交训练数据（文件太大）
   - 将 `data/` 目录添加到 `.gitignore`
   - 使用云存储或单独的数据仓库管理数据

## 📚 相关文档

- [数据收集指南](../docs/DATA_COLLECTION.md)
- [训练脚本说明](../model_training/train.py)
- [数据预处理说明](../model_training/data_preprocessing.py)

