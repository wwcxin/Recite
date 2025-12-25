# 大开门识单词 (Recite)

一个基于 React 的英语单词学习应用，支持四级和六级核心词汇学习。

## ✨ 功能特点

- 📚 **多题库支持**：支持四级（CET4）和六级（CET6）核心词汇
- 🎯 **互动答题**：选择题形式，随机出题，帮助记忆单词
- 🔊 **语音播放**：支持美式发音，点击即可播放单词音频
- 📊 **实时计分**：答对加分，答错扣分，实时显示学习进度
- 🎨 **精美界面**：现代化 UI 设计，流畅的动画效果
- 📱 **响应式设计**：完美适配手机和电脑端
- 🎉 **反馈机制**：答对时显示"蒸蚌+1"提示，增强学习趣味性

## 🛠️ 技术栈

- **React 18** - 前端框架
- **React Router** - 路由管理
- **Vite** - 构建工具
- **CSS3** - 样式和动画

## 📦 安装和运行

### 环境要求

- Node.js >= 16.0.0
- npm >= 7.0.0

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

启动后访问 `http://localhost:5173`

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist/` 目录

### 预览生产版本

```bash
npm run preview
```

## 📁 项目结构

```
Recite/
├── src/                 # 源代码目录
│   ├── App.jsx          # 主应用组件（路由配置）
│   ├── App.css          # 主页样式
│   ├── main.jsx         # 应用入口
│   ├── index.css        # 全局样式
│   ├── pages/
│   │   └── Start.jsx    # 答题页面组件
│   └── styles/
│       └── Start.css    # 答题页面样式
├── public/              # 静态资源目录
│   ├── favicon.png      # 网站图标
│   ├── image/           # 图片资源
│   │   ├── center.png   # 中间选项图片
│   │   ├── Cover.png    # 封面图片
│   │   ├── great.png    # 计分图标
│   │   ├── left.png     # 左侧选项图片
│   │   ├── right.png    # 右侧选项图片
│   │   └── wait.png     # 等待状态图片
│   ├── json/            # JSON题库文件
│   │   ├── CET4luan_1.json
│   │   └── CET6luan_1.json
│   └── voice/           # 音频资源
│       ├── great.mp3    # 非一次答对音效
│       └── great2.mp3   # 一次答对音效
├── index.html           # HTML模板
├── vite.config.js       # Vite配置
├── package.json         # 项目配置
└── README.md            # 项目说明
```

## 🎮 使用说明

### 主页

1. 打开应用后，会看到"大开门识单词"主页
2. 点击"四级核心词"或"六级核心词"开始学习
3. 右上角有"项目地址"和"联系"按钮

### 答题页面

1. **查看单词**：页面中央显示当前单词（带 GB 标签表示英式英语）
2. **播放音频**：点击单词旁的 🔊 按钮播放美式发音
3. **选择答案**：从三个选项中选择正确的中文释义
4. **查看反馈**：
   - 答对：显示"蒸蚌+1"提示，播放成功音效，分数+1
   - 答错：播放单词音频，分数-1，2秒后可重新选择
5. **返回主页**：点击左上角"← 返回"按钮

### 计分规则

- ✅ **一次答对**：播放 `great2.mp3`，分数 +1
- ✅ **非一次答对**：播放 `great.mp3`，分数 +1
- ❌ **答错**：播放单词音频，分数 -1（最低为 0）

## 🔧 开发说明

### 添加新题库

1. 将 JSON 文件放入 `public/json/` 目录
2. JSON 格式示例：
```json
[
  {
    "wordRank": 1,
    "headWord": "access",
    "usspeech": "access&type=2",
    "tranCn": "获取；接近，入口"
  }
]
```

3. 在 `src/App.jsx` 中添加新的选项按钮

### 自定义样式

- 主页样式：`src/App.css`
- 答题页样式：`src/styles/Start.css`
- 全局样式：`src/index.css`

## 📝 注意事项

- 所有静态资源（图片、音频、JSON文件）都放在 `public/` 目录下
- Vite 会自动提供 public 目录下的静态资源，可通过 `/image/xxx.png` 访问
- 项目结构符合标准 React + Vite 项目规范
- 音频资源使用有道词典的 API：`https://dict.youdao.com/dictvoice?audio={usspeech}`

## 📄 许可证

本项目采用 Apache v2 许可证。

## 👤 作者

- GitHub: [wwcxin](https://github.com/wwcxin)
- 联系邮箱: hi@b23.run

## 🙏 致谢
[词典](https://github.com/kajweb/dict)

---

**大开门识单词** - 让单词学习更有趣！ 🎓
