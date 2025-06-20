# 🔮 Oriching - 纳甲六爻排盘系统

> 基于传统易学智慧与现代技术的六爻占卜工作台

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.0+-brightgreen.svg)

## ⚖️ 许可证声明

**这是专有软件，受版权保护。**

- 本软件仅供个人学习和研究使用
- 未经明确授权，禁止商业使用、复制或分发
- 使用前请仔细阅读 [LICENSE](./LICENSE) 文件
- 如需商业授权，请联系作者

## ✨ 项目特色

### 🎨 道家留白美学
- 简约优雅的界面设计
- 传统配色与现代布局完美融合
- 响应式设计，支持多端使用

### 🔮 专业六爻功能
- **多种起卦方式**: 手动、随机、时间起卦
- **完整卦象渲染**: 阴阳爻、动爻、世应标识
- **传统纳甲体系**: 六亲、六神、干支配置
- **变卦分析**: 动爻变化及卦象演变

### 🤖 AI智能解卦
- 预留AI解卦接口
- 支持传统卦辞与现代解释
- 个性化建议生成

### 📱 现代化体验
- Vue3 + Vite 高性能前端
- FastAPI 高效后端服务
- 本地历史记录管理
- Electron 桌面应用支持

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **npm** 或 **yarn**

### 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd Oriching
```

#### 2. 启动后端服务
```bash
cd najia
pip install -r requirements.txt
python start_server.py
```

后端服务将在 `http://localhost:8000` 启动

#### 3. 启动前端服务
```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

#### 4. 访问应用
打开浏览器访问 `http://localhost:5173` 即可使用占卜工作台

## 📖 API 文档

后端提供完整的RESTful API，支持：

### 主要端点
- `GET /api/health` - 健康检查
- `POST /api/gua` - 手动起卦
- `POST /api/random` - 随机起卦
- `POST /api/time-gua` - 时间起卦
- `GET /api/constants` - 获取系统常量
- `GET /api/gua-analysis/{gua_name}` - 卦象分析

### API 文档地址
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ 项目结构

```
Oriching/
├── najia/                    # 后端六爻排盘服务
│   ├── najia/               # 核心算法模块
│   ├── app.py               # FastAPI 主应用
│   ├── start_server.py      # 服务启动脚本
│   ├── requirements.txt     # Python 依赖
│   └── API_Documentation.md # API 文档
├── frontend/                # 前端占卜工作台
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   ├── stores/         # 状态管理
│   │   └── style.css       # 全局样式
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite 配置
└── README.md               # 项目说明
```

## 🎯 使用指南

### 起卦流程

1. **选择起卦方式**
   - 手动起卦：输入6个数字(1-4)
   - 随机起卦：系统自动生成
   - 时间起卦：基于当前时间

2. **填写起卦信息**
   - 性别（可选）
   - 起卦标题（占卜事项）

3. **查看卦象结果**
   - 主卦信息：卦名、爻位、六亲六神
   - 变卦信息：动爻变化
   - 时间信息：公历、干支

4. **AI智能解卦**
   - 点击AI解卦按钮
   - 获取智能分析结果
   - 导出解卦记录

### 界面操作

- **导航切换**: 占卜、分析、历史三个标签
- **主题切换**: 明暗模式切换
- **历史管理**: 查看、导出、清空历史记录
- **卦象交互**: 点击爻位查看详细信息

## 🛠️ 开发指南

### 技术栈

#### 后端
- **框架**: FastAPI
- **算法**: 纳甲六爻传统算法
- **文档**: 自动生成的 OpenAPI 文档

#### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **样式**: 原生 CSS + CSS Variables

### 开发环境

```bash
# 后端开发
cd najia
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 前端开发
cd frontend
npm run dev

# 同时启动前后端
# 使用两个终端分别运行上述命令
```

### 构建部署

```bash
# 前端构建
cd frontend
npm run build

# Docker 部署（后端）
cd najia
docker build -t oriching-api .
docker run -p 8000:8000 oriching-api
```

## 🎨 设计理念

### 道家留白美学
项目采用道家"留白"的设计理念，追求简约而不简单的视觉效果：

- **配色**: 以白、灰、蓝为主色调，营造宁静致远的氛围
- **布局**: 大量留白空间，突出核心内容
- **交互**: 简洁直观，符合用户直觉
- **动画**: 轻柔自然，不喧宾夺主

### 易学传统
严格遵循传统六爻纳甲体系：
- **起卦方法**: 支持传统的手动起卦和现代的随机起卦
- **卦象表示**: 准确的阴阳爻、动爻、世应标识
- **六亲六神**: 完整的纳甲配置体系
- **变卦推演**: 基于动爻的卦象变化

## 🔮 功能特性

### 已实现功能
- ✅ 完整的六爻排盘算法
- ✅ 多种起卦方式支持
- ✅ 卦象可视化渲染
- ✅ 历史记录管理
- ✅ 响应式设计
- ✅ API 接口完善
- ✅ 前后端联调

### 规划功能
- 🔄 AI 智能解卦（接口已预留）
- 🔄 用户账户系统
- 🔄 社区分享功能
- 🔄 移动端 App
- 🔄 更多占卜方法
- 🔄 数据统计分析

## 📱 兼容性

- **浏览器**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **移动端**: iOS 12+, Android 8+
- **桌面端**: Windows 10+, macOS 10.15+, Linux

## 🤝 贡献指南

欢迎参与项目贡献！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
## ⚖️ 法律声明与使用条款

### 软件许可
- **本软件为专有软件**，受版权法保护
- 仅授权个人学习、研究和非商业使用
- 商业使用需要获得明确的书面授权
- 详细条款请参阅 [LICENSE](./LICENSE) 文件

### 第三方组件归属
- 本软件使用了多个开源组件，详见 [NOTICE](./NOTICE) 文件
- 所有第三方组件均按其原始许可证条款使用
- 特别感谢 najia 库的原作者提供的核心算法支持

### 免责声明
- 本软件仅供娱乐和学习参考
- 占卜结果不应作为重大决策的唯一依据
- 使用者应理性对待传统文化内容
- 作者不承担因使用本软件产生的任何后果

### 知识产权保护
- 严禁未经授权的复制、修改、分发
- 严禁逆向工程或提取核心算法
- 发现侵权行为将依法追究责任

## 📧 联系方式

**商业授权咨询**: [Your Email]  
**技术支持**: 请通过 Issues 提交  
**法律事务**: [Legal Email]

## 🙏 致谢

- [najia](https://github.com/bopo/najia) - 六爻排盘核心算法（按其原始许可证使用）
- [Vue.js](https://vuejs.org/) - 前端框架（MIT License）
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架（MIT License）
- [Vite](https://vitejs.dev/) - 构建工具（MIT License）

---

*愿此工具能为您的人生抉择提供一份参考，但请记住：易学是智慧的结晶，而非命运的枷锁。🌟*

**使用本软件即表示您同意遵守上述条款和许可证协议。**
