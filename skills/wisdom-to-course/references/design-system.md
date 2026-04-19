# 设计系统

本文档提供用于心灵成长课程的CSS令牌和模式。

## 核心设计令牌

### 调色板

**背景色**：
- `--color-bg: #FAF7F2` —— 温暖的米白色（偶数模块）
- `--color-bg-warm: #F5EDE3` —— 更温暖的米色（奇数模块）
- `--color-bg-alt: #F0E6D8` —— 强调背景

**强调色**：
- `--color-accent: #8B4513` —— 深棕色（主强调）
- `--color-accent-light: #A0522D` —— 赭色
- `--color-accent-dark: #654321` —— 深褐色
- `--color-accent-soft: rgba(139, 69, 19, 0.1)` —— 柔和强调背景

**情绪颜色**（用于内心对话等）：
- `--color-critic: #C75B39` —— 批评者（暖红）
- `--color-protector: #4A7C59` —— 保护者（森林绿）
- `--color-wise: #5B8BA0` —— 智慧（青蓝）
- `--color-child: #D4A574` —— 小孩（暖黄）

**文本颜色**：
- `--color-text: #2C2416` —— 主文本（深棕）
- `--color-text-secondary: #5C4D3C` —— 次要文本
- `--color-text-muted: #8B7355` —— 柔和文本

**UI颜色**：
- `--color-border: #E0D5C7` —— 边框
- `--color-shadow: rgba(44, 36, 22, 0.08)` —— 阴影
- `--color-card: #FFFFFF` —— 卡片背景

### 字体

**字体家族**：
- `--font-display: "Bricolage Grotesque", sans-serif` —— 标题
- `--font-body: "DM Sans", sans-serif` —— 正文
- `--font-mono: "JetBrains Mono", monospace` —— 术语/代码

**字体比例**（1.25比例）：
- `--text-xs: 0.75rem` —— 12px
- `--text-sm: 0.875rem` —— 14px
- `--text-base: 1rem` —— 16px
- `--text-lg: 1.125rem` —— 18px
- `--text-xl: 1.25rem` —— 20px
- `--text-2xl: 1.5rem` —— 24px
- `--text-3xl: 1.875rem` —— 30px
- `--text-4xl: 2.25rem` —— 36px
- `--text-5xl: 3rem` —— 48px

### 间距系统

**基础单位**：4px

- `--space-1: 0.25rem` —— 4px
- `--space-2: 0.5rem` —— 8px
- `--space-3: 0.75rem` —— 12px
- `--space-4: 1rem` —— 16px
- `--space-5: 1.25rem` —— 20px
- `--space-6: 1.5rem` —— 24px
- `--space-8: 2rem` —— 32px
- `--space-10: 2.5rem` —— 40px
- `--space-12: 3rem` —— 48px
- `--space-16: 4rem` —— 64px
- `--space-20: 5rem` —— 80px
- `--space-24: 6rem` —— 96px

### 布局

**内容宽度**：
- `--content-max: 800px` —— 标准内容
- `--content-wide: 1000px` —— 宽布局

**模块**：
- 全视口高度：`min-height: 100dvh`（回退 `100vh`）
- 滚动吸附：`scroll-snap-align: start`
- 偶数/奇数模块交替背景

### 阴影

- `--shadow-sm: 0 1px 2px var(--color-shadow)`
- `--shadow-md: 0 4px 6px var(--color-shadow)`
- `--shadow-lg: 0 10px 15px var(--color-shadow)`
- `--shadow-card: 0 2px 8px var(--color-shadow), 0 0 1px var(--color-border)`

### 圆角

- `--radius-sm: 4px`
- `--radius-md: 8px`
- `--radius-lg: 12px`
- `--radius-xl: 16px`
- `--radius-full: 9999px`

## 动画系统

### 缓动函数

- `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)` —— 主要缓动
- `--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)` —— 对称
- `--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)` —— 弹性

### 持续时间

- `--duration-fast: 150ms`
- `--duration-base: 300ms`
- `--duration-slow: 500ms`
- `--duration-slower: 800ms`

### 滚动触发动画

使用 Intersection Observer 触发动画：

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity var(--duration-slow) var(--ease-out),
              transform var(--duration-slow) var(--ease-out);
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### 交错动画

```css
.stagger-1 { transition-delay: 100ms; }
.stagger-2 { transition-delay: 200ms; }
.stagger-3 { transition-delay: 300ms; }
.stagger-4 { transition-delay: 400ms; }
.stagger-5 { transition-delay: 500ms; }
```

## 组件模式

### 模块容器

```css
.module {
  min-height: 100vh;
  min-height: 100dvh;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--space-8) var(--space-6);
}

.module:nth-child(even) {
  background-color: var(--color-bg);
}

.module:nth-child(odd) {
  background-color: var(--color-bg-warm);
}
```

### 内容容器

```css
.module-content {
  max-width: var(--content-max);
  margin: 0 auto;
  width: 100%;
}
```

### 卡片

```css
.card {
  background: var(--color-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: var(--space-6);
}
```

### 按钮

**主要按钮**：
```css
.btn-primary {
  background: var(--color-accent);
  color: white;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-primary:hover {
  background: var(--color-accent-dark);
  transform: translateY(-1px);
}
```

**次要按钮**：
```css
.btn-secondary {
  background: transparent;
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
}
```

### 提示框

```css
.callout {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  background: var(--color-accent-soft);
  border-left: 4px solid var(--color-accent);
}

.callout-aha {
  background: rgba(212, 165, 116, 0.2);
  border-left-color: #D4A574;
}

.callout-warning {
  background: rgba(199, 91, 57, 0.1);
  border-left-color: var(--color-critic);
}

.callout-tip {
  background: rgba(74, 124, 89, 0.1);
  border-left-color: var(--color-protector);
}
```

## 导航

### 进度条

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
  z-index: 100;
  transition: width 0.1s linear;
}
```

### 导航点

```css
.nav-dots {
  position: fixed;
  right: var(--space-6);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  z-index: 100;
}

.nav-dot {
  width: 10px;
  height: 10px;
  border-radius: var(--radius-full);
  background: var(--color-border);
  transition: all var(--duration-base) var(--ease-out);
}

.nav-dot.active {
  background: var(--color-accent);
  transform: scale(1.3);
}

.nav-dot.visited {
  background: var(--color-accent-light);
}
```

## 滚动条样式

```css
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-muted);
}
```

## 响应式断点

```css
/* 移动端优先 */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

## 无障碍

### 焦点样式

```css
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

### 减少动画

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 对比度

- 所有文本满足WCAG AA标准（4.5:1）
- 大文本满足WCAG AAA标准（7:1）
