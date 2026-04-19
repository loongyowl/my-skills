// Wisdom Course - Interactive Elements
// Handles all interactive components for mindfulness/psychology courses

document.addEventListener('DOMContentLoaded', function() {
  initProgressBar();
  initNavigationDots();
  initScrollAnimations();
  initScenarioQuizzes();
  initInnerDialogues();
  initEmotionFlows();
  initBiasSpotting();
  initGlossaryTooltips();
  initBreathingGuides();
});

// Progress Bar
function initProgressBar() {
  const progressBar = document.createElement('div');
  progressBar.className = 'progress-bar';
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', function() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    progressBar.style.width = progress + '%';
  });
}

// Navigation Dots
function initNavigationDots() {
  const modules = document.querySelectorAll('.module');
  if (modules.length === 0) return;

  const navContainer = document.createElement('div');
  navContainer.className = 'nav-dots';

  modules.forEach((module, index) => {
    const dot = document.createElement('button');
    dot.className = 'nav-dot';
    dot.setAttribute('aria-label', `Go to module ${index + 1}`);
    dot.addEventListener('click', () => {
      module.scrollIntoView({ behavior: 'smooth' });
    });
    navContainer.appendChild(dot);
  });

  document.body.appendChild(navContainer);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const index = Array.from(modules).indexOf(entry.target);
        const dots = navContainer.querySelectorAll('.nav-dot');
        dots.forEach((dot, i) => {
          dot.classList.remove('active', 'visited');
          if (i === index) dot.classList.add('active');
          else if (i < index) dot.classList.add('visited');
        });
      }
    });
  }, { threshold: 0.5 });

  modules.forEach(module => observer.observe(module));
}

// Scroll Animations
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  animatedElements.forEach(el => observer.observe(el));
}

// Scenario Quizzes
function initScenarioQuizzes() {
  const quizzes = document.querySelectorAll('.scenario-quiz');

  quizzes.forEach(quiz => {
    const options = quiz.querySelectorAll('.scenario-option');
    const feedbackContainer = quiz.querySelector('.scenario-feedback-container');

    options.forEach(option => {
      option.addEventListener('click', function() {
        options.forEach(opt => opt.classList.remove('selected'));
        this.classList.add('selected');

        const pattern = this.dataset.pattern;
        if (feedbackContainer) {
          feedbackContainer.classList.add('visible');
          const allFeedback = feedbackContainer.querySelectorAll('.feedback');
          allFeedback.forEach(fb => fb.style.display = 'none');

          const relevantFeedback = feedbackContainer.querySelector(`.feedback[data-for="${pattern}"]`);
          if (relevantFeedback) {
            relevantFeedback.style.display = 'block';
          }
        }
      });
    });
  });
}

// Inner Dialogue Animations
function initInnerDialogues() {
  const dialogues = document.querySelectorAll('.inner-dialogue');

  dialogues.forEach(dialogue => {
    const messages = dialogue.querySelectorAll('.message');
    const playBtn = dialogue.querySelector('.dialogue-play');
    const resetBtn = dialogue.querySelector('.dialogue-reset');

    let currentIndex = 0;
    let isPlaying = false;

    function reset() {
      messages.forEach(msg => msg.classList.remove('visible'));
      currentIndex = 0;
      isPlaying = false;
      if (playBtn) playBtn.textContent = '▶️ Play';
    }

    function playNext() {
      if (currentIndex < messages.length) {
        const msg = messages[currentIndex];
        const delay = parseInt(msg.dataset.delay) || 1500;

        setTimeout(() => {
          msg.classList.add('visible');
          currentIndex++;
          if (currentIndex < messages.length) {
            playNext();
          } else {
            isPlaying = false;
            if (playBtn) playBtn.textContent = '▶️ Replay';
          }
        }, delay);
      }
    }

    function start() {
      if (isPlaying) return;
      isPlaying = true;
      if (playBtn) playBtn.textContent = '⏸️ Playing...';
      if (currentIndex >= messages.length) reset();
      playNext();
    }

    if (playBtn) playBtn.addEventListener('click', start);
    if (resetBtn) resetBtn.addEventListener('click', reset);
  });
}

// Emotion Flow Animations
function initEmotionFlows() {
  const flows = document.querySelectorAll('.emotion-flow');

  flows.forEach(flow => {
    const stepsData = flow.dataset.steps;
    if (!stepsData) return;

    const steps = JSON.parse(stepsData);
    const nodesContainer = flow.querySelector('.flow-nodes');
    const explanationContainer = flow.querySelector('.flow-explanation');
    const playBtn = flow.querySelector('.flow-play');
    const progressBar = flow.querySelector('.progress-bar');

    if (nodesContainer) {
      nodesContainer.innerHTML = '';
      steps.forEach((step, index) => {
        const node = document.createElement('div');
        node.className = 'flow-node';
        node.dataset.step = index;
        node.innerHTML = `
          <div class="flow-node-icon">${step.icon}</div>
          <div class="flow-node-label">${step.label}</div>
        `;
        nodesContainer.appendChild(node);
      });
    }

    if (explanationContainer) {
      explanationContainer.innerHTML = '';
      steps.forEach((step, index) => {
        const exp = document.createElement('div');
        exp.className = 'explanation-step';
        exp.dataset.step = index;
        exp.innerHTML = `<h5>${step.label}</h5><p>${step.description}</p>`;
        explanationContainer.appendChild(exp);
      });
    }

    let currentStep = 0;
    let isPlaying = false;

    function showStep(index) {
      const nodes = flow.querySelectorAll('.flow-node');
      nodes.forEach((node, i) => node.classList.toggle('active', i === index));

      const explanations = flow.querySelectorAll('.explanation-step');
      explanations.forEach((exp, i) => exp.classList.toggle('active', i === index));

      if (progressBar) {
        progressBar.style.width = ((index + 1) / steps.length * 100) + '%';
      }
    }

    function play() {
      if (isPlaying) return;
      isPlaying = true;
      currentStep = 0;

      function next() {
        if (currentStep < steps.length) {
          showStep(currentStep);
          currentStep++;
          setTimeout(next, 2000);
        } else {
          isPlaying = false;
          if (playBtn) playBtn.textContent = '▶️ Replay';
        }
      }

      next();
    }

    if (playBtn) playBtn.addEventListener('click', play);
    showStep(0);
  });
}

// Bias Spotting Challenges
function initBiasSpotting() {
  const challenges = document.querySelectorAll('.bias-spotting');

  challenges.forEach(challenge => {
    const options = challenge.querySelectorAll('.bias-option');
    const correctResults = challenge.querySelectorAll('.bias-result[data-result="correct"]');
    const incorrectResults = challenge.querySelectorAll('.bias-result[data-result="incorrect"]');

    options.forEach(option => {
      option.addEventListener('click', function() {
        const selectedBias = this.dataset.bias;
        const correctBias = challenge.dataset.bias || challenge.dataset.biasId;

        options.forEach(opt => {
          opt.classList.remove('correct', 'incorrect');
          opt.disabled = true;
        });

        const isCorrect = selectedBias === correctBias;
        this.classList.add(isCorrect ? 'correct' : 'incorrect');

        correctResults.forEach(r => r.classList.remove('visible'));
        incorrectResults.forEach(r => r.classList.remove('visible'));

        if (isCorrect) {
          correctResults.forEach(r => r.classList.add('visible'));
        } else {
          incorrectResults.forEach(r => r.classList.add('visible'));
        }
      });
    });
  });
}

// Glossary Tooltips
function initGlossaryTooltips() {
  const terms = document.querySelectorAll('.glossary-term');
  const tooltip = document.createElement('div');
  tooltip.className = 'glossary-tooltip';
  document.body.appendChild(tooltip);

  const glossary = {
    'mindfulness': { title: '正念', definition: '有意识地、不评判地觉察当下。' },
    'cognitive-bias': { title: '认知偏差', definition: '思维中的系统性错误，让我们偏离理性的判断。' },
    'mind-reading': { title: '读心术', definition: '假设知道别人的想法，而没有实际证据。' },
    'emotional-awareness': { title: '情绪觉察', definition: '识别和命名自己情绪状态的能力。' }
  };

  terms.forEach(term => {
    term.addEventListener('mouseenter', function(e) {
      const def = glossary[this.dataset.term];
      if (def) {
        tooltip.innerHTML = `<h6>${def.title}</h6><p>${def.definition}</p>`;
        tooltip.classList.add('visible');
        positionTooltip(e, tooltip);
      }
    });

    term.addEventListener('mouseleave', () => tooltip.classList.remove('visible'));
    term.addEventListener('mousemove', (e) => positionTooltip(e, tooltip));
  });

  function positionTooltip(e, tooltip) {
    const rect = tooltip.getBoundingClientRect();
    let left = e.clientX + 10;
    let top = e.clientY + 10;

    if (left + rect.width > window.innerWidth) left = e.clientX - rect.width - 10;
    if (top + rect.height > window.innerHeight) top = e.clientY - rect.height - 10;

    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
  }
}

// Breathing Guides
function initBreathingGuides() {
  const guides = document.querySelectorAll('.breathing-guide');

  guides.forEach(guide => {
    const circle = guide.querySelector('.breath-circle');
    const text = guide.querySelector('.breath-text');
    const startBtn = guide.querySelector('.breathing-start');
    const stopBtn = guide.querySelector('.breathing-stop');

    let isRunning = false;
    const phases = [
      { name: '吸气', duration: 4000, scale: 1.5 },
      { name: '屏息', duration: 4000, scale: 1.5 },
      { name: '呼气', duration: 6000, scale: 1 }
    ];

    let currentPhase = 0;
    let timeoutId = null;

    function runPhase() {
      if (!isRunning) return;

      const phase = phases[currentPhase];
      if (text) text.textContent = phase.name;
      if (circle) {
        circle.style.transform = `scale(${phase.scale})`;
        circle.style.transition = `transform ${phase.duration}ms ease-in-out`;
      }

      currentPhase = (currentPhase + 1) % phases.length;
      timeoutId = setTimeout(runPhase, phase.duration);
    }

    function start() {
      if (isRunning) return;
      isRunning = true;
      currentPhase = 0;
      if (startBtn) startBtn.style.display = 'none';
      if (stopBtn) stopBtn.style.display = 'inline-flex';
      runPhase();
    }

    function stop() {
      isRunning = false;
      if (timeoutId) clearTimeout(timeoutId);
      if (startBtn) startBtn.style.display = 'inline-flex';
      if (stopBtn) stopBtn.style.display = 'none';
      if (circle) {
        circle.style.transform = 'scale(1)';
        circle.style.transition = 'transform 0.5s ease-out';
      }
      if (text) text.textContent = '准备';
    }

    if (startBtn) startBtn.addEventListener('click', start);
    if (stopBtn) stopBtn.addEventListener('click', stop);
  });
}

// Keyboard Navigation
document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
    e.preventDefault();
    navigateModule(1);
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
    e.preventDefault();
    navigateModule(-1);
  }
});

function navigateModule(direction) {
  const modules = document.querySelectorAll('.module');
  const scrollPos = window.scrollY + window.innerHeight / 2;

  for (let i = 0; i < modules.length; i++) {
    const rect = modules[i].getBoundingClientRect();
    const moduleCenter = rect.top + rect.height / 2 + window.scrollY;

    if (direction > 0 && moduleCenter > scrollPos) {
      modules[i].scrollIntoView({ behavior: 'smooth' });
      break;
    } else if (direction < 0 && moduleCenter < scrollPos - 10) {
      modules[i].scrollIntoView({ behavior: 'smooth' });
      break;
    }
  }
}