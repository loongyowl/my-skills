# 互动元素实现模式

本文档提供用于心灵成长课程的互动教学元素的实现模式。

## 目录

1. [概念 ↔ 生活场景映射](#1-概念--生活场景映射)
2. [情境选择测验](#2-情境选择测验)
3. [内心对话动画](#3-内心对话动画)
4. [情绪转变过程动画](#4-情绪转变过程动画)
5. [认知偏差识别挑战](#5-认知偏差识别挑战)
6. [情绪-反应配对](#6-情绪-反应配对)
7. [Aha! 提示框](#7-aha-提示框)
8. [实践练习卡片](#8-实践练习卡片)
9. [呼吸动画引导](#9-呼吸动画引导)
10. [进度追踪器](#10-进度追踪器)

---

## 1. 概念 ↔ 生活场景映射

展示抽象概念与日常生活的对应关系，帮助学习者将理论与经验连接。

### HTML 结构

```html
<div class="concept-scenario-block">
  <div class="concept-side">
    <div class="side-header">
      <span class="side-icon">📚</span>
      <h4>概念</h4>
    </div>
    <div class="concept-content">
      <p class="concept-term"><span class="glossary-term" data-term="cognitive-bias">认知偏差</span>：读心术</p>
      <p class="concept-definition">假设知道别人的想法和动机，而没有实际证据。</p>
    </div>
  </div>

  <div class="scenario-side">
    <div class="side-header">
      <span class="side-icon">🌟</span>
      <h4>生活场景</h4>
    </div>
    <div class="scenario-content">
      <blockquote class="scenario-quote">"他没有回复我的消息，一定是对我生气了。"</blockquote>
      <div class="scenario-insight"
        <p><strong>实际上可能有100个原因：</strong></p>
        <ul>
          <li>手机没电了</li>
          <li>正在开会</li>
          <li>单纯忘记了</li>
          <li>需要时间思考回复</li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

### CSS 类说明

- `.concept-scenario-block` —— 容器，使用grid布局
- `.concept-side` —— 左侧概念区域
- `.scenario-side` —— 右侧场景区域
- `.side-header` —— 区域标题，带图标
- `.concept-term` —— 概念名称
- `.scenario-quote` —— 生活场景引用
- `.scenario-insight` —— 洞察/替代视角

---

## 2. 情境选择测验

给出生活情境，让学习者选择回应方式，了解自己的反应模式。

### HTML 结构

```html
<div class="scenario-quiz" data-quiz-id="conflict-response">
  <div class="scenario-header">
    <span class="scenario-badge">情境 1</span>
    <h4>冲突时刻</h4>
  </div>

  <div class="scenario-narrative">
    <p>你和伴侣因为家务分工问题产生分歧。你感到胸口发紧，声音开始变大。对方说："你总是这样，从不听我说话。"</p>
    <p class="scenario-question">此刻，你的第一反应是...</p>
  </div>

  <div class="scenario-options">
    <button class="scenario-option" data-pattern="fight" data-value="1">
      <span class="option-icon">⚔️</span>
      <span class="option-text">立即反驳："我才不是！你才是那个从不..."</span>
    </button>

    <button class="scenario-option" data-pattern="freeze" data-value="2">
      <span class="option-icon">🧊</span>
      <span class="option-text">愣住，感到被攻击，说不出话来</span>
    </button>

    <button class="scenario-option" data-pattern="flee" data-value="3">
      <span class="option-icon">🏃</span>
      <span class="option-text">转身离开房间，避免继续争吵</span>
    </button>

    <button class="scenario-option" data-pattern="awareness" data-value="4">
      <span class="option-icon">🧘</span>
      <span class="option-text">深呼吸，注意到自己的愤怒，暂停一下</span>
    </button>
  </div>

  <div class="scenario-feedback-container">
    <div class="feedback" data-for="fight">
      <div class="feedback-header">
        <span class="feedback-pattern">战斗反应</span>
      </div>
      <p>这是<span class="glossary-term" data-term="fight-response">战斗反应</span>——当感到威胁时的攻击性回应。虽然表达很重要，但在情绪高涨时容易说出伤人的话，让冲突升级。</p>
      <div class="feedback-insight">
        <p><strong>觉察点：</strong>你的身体在试图保护你，但方式可能适得其反。</p>
      </div>
    </div>

    <div class="feedback" data-for="freeze">
      <div class="feedback-header">
        <span class="feedback-pattern">冻结反应</span>
      </div>
      <p>这是<span class="glossary-term" data-term="freeze-response">冻结反应</span>——神经系统过载时的"宕机"状态。你可能感到麻木、无法思考或行动。</p>
      <div class="feedback-insight">
        <p><strong>觉察点：</strong>这是身体在说"太多了"。给自己时间和空间很重要。</p>
      </div>
    </div>

    <div class="feedback" data-for="flee">
      <div class="feedback-header">
        <span class="feedback-pattern">逃跑反应</span>
      </div>
      <p>这是<span class="glossary-term" data-term="flee-response">逃跑反应</span>——通过离开来避免痛苦。虽然暂时缓解，但问题通常会在之后以更强烈的方式回来。</p>
      <div class="feedback-insight">
        <p><strong>觉察点：</strong>离开可以是一个健康的选择，但觉察动机很重要——是冷静还是逃避？</p>
      </div>
    </div>

    <div class="feedback" data-for="awareness">
      <div class="feedback-header">
        <span class="feedback-pattern">觉察回应</span>
      </div>
      <p>这是<span class="glossary-term" data-term="conscious-response">觉察回应</span>——在反应和回应之间创造空间。你注意到了身体信号，给自己时间选择。</p>
      <div class="feedback-insight"
        <p><strong>觉察点：</strong>这是可以培养的能力！暂停是改变反应模式的第一步。</p>
      </div>
    </div>
  </div>
</div>
```

### 数据属性

- `data-quiz-id` —— 测验唯一标识
- `data-pattern` —— 反应模式类型（fight/freeze/flee/awareness）
- `data-value` —— 选项值
- `data-for` —— 对应哪个选项的反馈

---

## 3. 内心对话动画

展示内心不同"声音"的对话，帮助学习者理解内在冲突。

### HTML 结构

```html
<div class="inner-dialogue" id="dialogue-critic">
  <div class="dialogue-header">
    <h4><span class="dialogue-icon">💭</span> 内心的对话</h4>
    <p class="dialogue-context">当你犯了一个错误时，内心发生了什么？</p>
  </div>

  <div class="dialogue-messages">
    <div class="message message-critic" data-delay="0" data-actor="critic">
      <div class="message-avatar">😤</div>
      <div class="message-content">
        <span class="message-sender">内在批评者</span>
        <p>你怎么又搞砸了？这么简单的事情都做不好！</p>
      </div>
    </div>

    <div class="message message-protector" data-delay="2000" data-actor="protector">
      <div class="message-avatar">🛡️</div>
      <div class="message-content">
        <span class="message-sender">保护者</span>
        <p>等等，别这么苛刻。犯错是正常的，没必要这么攻击自己。</p>
      </div>
    </div>

    <div class="message message-critic" data-delay="4000" data-actor="critic">
      <div class="message-avatar">😤</div>
      <div class="message-content">
        <span class="message-sender">内在批评者</span>
        <p>但如果是别人犯了这种错，我会觉得他们很无能...</p>
      </div>
    </div>

    <div class="message message-wise" data-delay="6000" data-actor="wise">
      <div class="message-avatar">🦉</div>
      <div class="message-content">
        <span class="message-sender">智慧的声音</span>
        <p>让我们深呼吸。错误发生了，我们能从中学到什么？对自己温柔一点...</p>
      </div>
    </div>
  </div>

  <div class="dialogue-controls">
    <button class="dialogue-play">▶️ 播放对话</button>
    <button class="dialogue-reset">🔄 重新开始</button>
  </div>

  <div class="dialogue-legend">
    <div class="legend-item">
      <span class="legend-color critic"></span>
      <span>内在批评者 —— 追求完美，害怕失败</span>
    </div>
    <div class="legend-item">
      <span class="legend-color protector"></span>
      <span>保护者 —— 试图保护你不受伤害</span>
    </div>
    <div class="legend-item">
      <span class="legend-color wise"></span>
      <span>智慧的声音 —— 平衡、慈悲、洞察</span>
    </div>
  </div>
</div>
```

### 数据属性

- `data-delay` —— 消息出现的延迟（毫秒）
- `data-actor` —— 说话者角色（critic/protector/wise/child等）
- `id` —— 对话容器唯一标识

### 角色类型

- `.message-critic` —— 内在批评者（红色调）
- `.message-protector` —— 保护者（蓝色调）
- `.message-wise` —— 智慧的声音（绿色调）
- `.message-child` —— 内在小孩（黄色调）

---

## 4. 情绪转变过程动画

展示从触发事件到反应/回应的完整链条。

### HTML 结构

```html
<div class="emotion-flow"
     id="flow-anger"
     data-steps='[
       {"actor": "trigger", "label": "触发事件", "description": "收到一封批评邮件", "icon": "📧"},
       {"actor": "body", "label": "身体感受", "description": "胸口发紧、心跳加速、脸发热", "icon": "💓"},
       {"actor": "emotion", "label": "情绪", "description": "愤怒、羞耻、防御", "icon": "😠"},
       {"actor": "thought", "label": "思维", "description": "\"他总是针对我\"、\"这不公平\"", "icon": "💭"},
       {"actor": "urge", "label": "冲动", "description": "想要立即写反驳邮件", "icon": "⚡"},
       {"actor": "response", "label": "反应", "description": "愤怒地回复（可能导致后悔）", "icon": "📤"}
     ]'>

  <div class="flow-header">
    <h4><span class="flow-icon">🌊</span> 情绪的波浪</h4>
    <p>观察情绪如何从触发到反应的完整过程</p>
  </div>

  <div class="flow-visualization">
    <div class="flow-track"></div>
    <div class="flow-nodes"></div>
    <div class="flow-particle"></div>
  </div>

  <div class="flow-explanation">
    <div class="explanation-step" data-step="0">
      <h5>触发事件</h5>
      <p>外部或内部事件启动了整个链条。</p>
    </div>
    <div class="explanation-step" data-step="1">
      <h5>身体感受</h5>
      <p>身体是最先反应的。觉察这些信号是打断自动化反应的关键。</p>
    </div>
    <div class="explanation-step" data-step="2">
      <h5>情绪</h5>
      <p>情绪是身体感受的标签。命名情绪可以降低它的强度。</p>
    </div>
    <div class="explanation-step" data-step="3">
      <h5>思维</h5>
      <p>大脑开始编织故事。注意：这些想法不一定是事实！</p>
    </div>
    <div class="explanation-step" data-step="4">
      <h5>冲动</h5>
      <p>强烈的行动倾向。这是<strong>反应</strong>和<strong>回应</strong>之间的临界点。</p>
    </div>
    <div class="explanation-step" data-step="5">
      <h5>反应</h5>
      <p>自动化的行为。如果我们能在冲动阶段暂停，就能选择更智慧的回应。</p>
    </div>
  </div>

  <div class="flow-controls">
    <button class="flow-play">▶️ 播放过程</button>
    <div class="flow-progress">
      <div class="progress-bar"></div>
    </div>
  </div>

  <div class="flow-pause-points">
    <h5>🛑 干预点</h5>
    <p>在哪些点你可以介入，改变结果？</p>
    <ul>
      <li><strong>觉察身体感受</strong> —— 最早的信号</li>
      <li><strong>命名情绪</strong> —— "我感到愤怒"</li>
      <li><strong>质疑思维</strong> —— "这是事实还是想法？"</li>
      <li><strong>暂停冲动</strong> —— 深呼吸，数到10</li>
    </ul>
  </div>
</div>
```

### JSON 数据结构

```json
{
  "steps": [
    {
      "actor": "触发器类型",
      "label": "显示标签",
      "description": "具体描述",
      "icon": "emoji图标"
    }
  ]
}
```

---

## 5. 认知偏差识别挑战

帮助学习者识别思维中的认知偏差。

### HTML 结构

```html
<div class="bias-spotting" data-bias-id="mind-reading-1">
  <div class="challenge-header">
    <span class="challenge-badge">🔍 挑战 1</span>
    <h4>找出认知偏差</h4>
  </div>

  <div class="thought-bubble">
    <div class="bubble-icon">💭</div>
    <blockquote class="thought-text">
      "同事没有邀请我参加午餐，他们一定是不喜欢我，在故意排挤我。"
    </blockquote>
  </div>

  <div class="bias-question">
    <p>这个想法中包含了什么<span class="glossary-term" data-term="cognitive-bias">认知偏差</span>？</p>
  </div>

  <div class="bias-options">
    <button class="bias-option" data-bias="catastrophizing">
      <span class="option-name">灾难化思维</span>
      <span class="option-desc">想象最坏的情况</span>
    </button>

    <button class="bias-option" data-bias="mind-reading">
      <span class="option-name">读心术</span>
      <span class="option-desc">假设知道别人的想法</span>
    </button>

    <button class="bias-option" data-bias="all-or-nothing">
      <span class="option-name">全或无思维</span>
      <span class="option-desc">非黑即白的极端思维</span>
    </button>

    <button class="bias-option" data-bias="personalization">
      <span class="option-name">个人化</span>
      <span class="option-desc">认为事情是针对自己的</span>
    </button>
  </div>

  <div class="bias-result" data-result="correct">
    <div class="result-header">
      <span class="result-icon">✅</span>
      <h5>正确！</h5>
    </div>

    <div class="bias-explanation">
      <h6>读心术 + 个人化</h6>
      <p>这个想法假设知道同事的想法（读心术），并认为他们的行为是针对自己的（个人化）。</p>
    </div>

    <div class="alternative-thought">
      <h6>🔄 替代思维</h6>
      <blockquote>"我不知道他们为什么没有邀请我。可能有各种原因——也许只是临时决定，或者他们以为我有其他安排。我可以选择直接询问，而不是假设最坏的情况。"</blockquote>
    </div>

    <div class="reflection-prompt">
      <h6>🤔 反思</h6>
      <p>你最近有过类似的想法吗？当时的情境是什么？</p>
    </div>
  </div>

  <div class="bias-result" data-result="incorrect">
    <div class="result-header">
      <span class="result-icon">💡</span>
      <h5>接近，但再看看...</h5>
    </div>
    <p>这个想法确实包含了一些偏差，但最主要的两个是<strong>读心术</strong>（假设知道同事的想法）和<strong>个人化</strong>（认为事情是针对自己的）。</p>
  </div>
</div>
```

### 偏差类型

- `mind-reading` —— 读心术
- `catastrophizing` —— 灾难化思维
- `all-or-nothing` —— 全或无思维
- `personalization` —— 个人化
- `overgeneralization` —— 过度概括
- `filtering` —— 心理过滤
- `should-statements` —— 应该陈述

---

## 6. 情绪-反应配对

拖拽配对游戏，连接情绪与对应的身体感受或思维模式。

### HTML 结构

```html
<div class="emotion-matching" data-game-id="emotion-body">
  <div class="matching-header">
    <h4>🎯 情绪与身体信号</h4>
    <p>将情绪与对应的身体感受配对</p>
  </div>

  <div class="matching-container">
    <div class="emotion-column">
      <h5>情绪</h5>

      <div class="emotion-item" data-emotion="anger" draggable="true">
        <span class="emotion-icon">😠</span>
        <span class="emotion-name">愤怒</span>
      </div>

      <div class="emotion-item" data-emotion="anxiety" draggable="true">
        <span class="emotion-icon">😰</span>
        <span class="emotion-name">焦虑</span>
      </div>

      <div class="emotion-item" data-emotion="sadness" draggable="true">
        <span class="emotion-icon">😢</span>
        <span class="emotion-name">悲伤</span>
      </div>

      <div class="emotion-item" data-emotion="joy" draggable="true">
        <span class="emotion-icon">😊</span>
        <span class="emotion-name">喜悦</span>
      </div>
    </div>

    <div class="reaction-column">
      <h5>身体信号</h5>

      <div class="reaction-slot" data-match="anxiety">
        <span class="slot-placeholder">胸口发紧、呼吸急促</span>
      </div>

      <div class="reaction-slot" data-match="joy">
        <span class="slot-placeholder">胸口开阔、轻松</span>
      </div>

      <div class="reaction-slot" data-match="anger">
        <span class="slot-placeholder">脸部发热、肌肉紧绷</span>
      </div>

      <div class="reaction-slot" data-match="sadness">
        <span class="slot-placeholder">沉重、能量低落</span>
      </div>
    </div>
  </div>

  <div class="matching-feedback">
    <div class="feedback-success">
      <span class="feedback-icon">🎉</span>
      <p>很好！觉察身体信号是情绪管理的第一步。</p>
    </div>
  </div>

  <div class="matching-insight">
    <h5>💡 洞察</h5>
    <p>身体往往比思维更早感知情绪。学会"倾听"身体，你就能在情绪升级前及时觉察。</p>
  </div>
</div>
```

---

## 7. Aha! 提示框

突出重要的洞察时刻。

### HTML 结构

```html
<div class="callout callout-aha">
  <div class="callout-icon">💡</div>
  <div class="callout-content">
    <h4>Aha! 时刻</h4>
    <p>你不是你的情绪。你是那个能够<strong>观察</strong>情绪的人。</p>
    <p class="callout-subtext">情绪会来也会走，但那个觉察的"你"始终在那里。</p>
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-icon">⚠️</div>
  <div class="callout-content">
    <h4>常见误区</h4>
    <p>觉察情绪不等于压抑情绪。压抑是"我不应该感到愤怒"，觉察是"我注意到我感到愤怒"。</p>
  </div>
</div>

<div class="callout callout-tip">
  <div class="callout-icon">✨</div>
  <div class="callout-content">
    <h4>实践小贴士</h4>
    <p>下次情绪升起时，试着问自己："此刻我的身体哪里感到紧绷？"</p>
  </div>
</div>
```

---

## 8. 实践练习卡片

具体的日常练习方法。

### HTML 结构

```html
<div class="practice-card">
  <div class="practice-header">
    <span class="practice-icon">🧘</span>
    <h4>今日练习：STOP技巧</h4>
    <span class="practice-duration">⏱️ 30秒</span>
  </div>

  <div class="practice-description">
    <p>当情绪强烈时，使用这个简单的技巧创造暂停空间。</p>
  </div>

  <div class="practice-steps"
    <div class="practice-step">
      <div class="step-marker"><span class="step-letter">S</span></div>
      <div class="step-content">
        <strong>Stop</strong> —— 暂停
        <p>停下你正在做的事情。如果可能，闭上眼睛或转移视线。</p>
      </div>
    </div>

    <div class="practice-step">
      <div class="step-marker"><span class="step-letter">T</span></div>
      <div class="step-content">
        <strong>Take a breath</strong> —— 深呼吸
        <p>做三次深呼吸。感受空气进入和离开你的身体。</p>
      </div>
    </div>

    <div class="practice-step">
      <div class="step-marker"><span class="step-letter">O</span></div>
      <div class="step-content">
        <strong>Observe</strong> —— 观察
        <p>注意：你的身体感受、情绪、思维。只是观察，不评判。</p>
      </div>
    </div>

    <div class="practice-step">
      <div class="step-marker"><span class="step-letter">P</span></div>
      <div class="step-content">
        <strong>Proceed</strong> —— 继续
        <p>带着这份觉察，选择如何回应。你可以问："什么是最有智慧的做法？"</p>
      </div>
    </div>
  </div>

  <div class="practice-reminder">
    <p>📌 <strong>提醒：</strong> 把"STOP"设为手机壁纸，或写在便利贴上贴在显眼处。</p>
  </div>
</div>
```

---

## 9. 呼吸动画引导

引导式呼吸练习。

### HTML 结构

```html
<div class="breathing-guide" id="breathing-1">
  <div class="breathing-header">
    <h4>🌬️ 呼吸练习</h4>
    <p>跟随动画，让呼吸慢下来</p>
  </div>

  <div class="breathing-visual">
    <div class="breath-circle">
      <span class="breath-text">吸气</span>
    </div>
    <div class="breath-timer">4秒</div>
  </div>

  <div class="breathing-controls"
    <button class="breathing-start">▶️ 开始练习</button>
    <button class="breathing-stop" style="display:none;">⏹️ 停止</button>
  </div>

  <div class="breathing-instructions">
    <div class="instruction" data-phase="inhale">
      <span class="phase-name">吸气</span>
      <span class="phase-duration">4秒</span>
    </div>
    <div class="instruction" data-phase="hold">
      <span class="phase-name">屏息</span>
      <span class="phase-duration">4秒</span>
    </div>
    <div class="instruction" data-phase="exhale">
      <span class="phase-name">呼气</span>
      <span class="phase-duration">6秒</span>
    </div>
  </div>
</div>
```

---

## 10. 进度追踪器

显示学习进度和成就。

### HTML 结构

```html
<div class="progress-tracker">
  <div class="tracker-header"
003e
    <h4>📊 你的学习旅程</h4>
  </div>

  <div class="tracker-modules">
    <div class="tracker-module completed">
      <span class="module-status">✅</span>
      <span class="module-name">当情绪来袭</span>
    </div>

    <div class="tracker-module completed">
      <span class="module-status">✅</span>
      <span class="module-name">认识自动化反应</span>
    </div>

    <div class="tracker-module current">
      <span class="module-status">📍</span>
      <span class="module-name">情绪背后的信息</span>
    </div>

    <div class="tracker-module">
      <span class="module-status">⭕</span>
      <span class="module-name">按下暂停键</span>
    </div>
  </div>

  <div class="tracker-insights">
    <h5>🎯 关键洞察</h5>
    <ul>
      <li>你不是你的情绪</li>
      <li>身体比思维更早感知情绪</li>
      <li>暂停是改变反应模式的关键</li>
    </ul>
  </div>
</div>
```

---

## CSS 类命名规范

所有互动元素使用以下命名约定：

- **容器**：`-container`, `-wrapper`, `-block`
- **状态**：`.active`, `.completed`, `.correct`, `.incorrect`, `.visible`
- **交互**：`.draggable`, `.droppable`, `.clickable`, `.selectable`
- **动画**：`.animate-in`, `.animate-out`, `.pulse`, `.fade`

## JavaScript 初始化

所有互动元素通过 `data-*` 属性和CSS类自动初始化。`main.js` 会：

1. 扫描页面中的互动元素
2. 根据 `data-*` 属性绑定事件处理器
3. 管理动画时序和状态
4. 处理用户交互反馈

不需要内联 `<script>` 标签。
