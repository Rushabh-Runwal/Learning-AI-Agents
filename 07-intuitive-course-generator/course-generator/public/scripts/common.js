/**
 * Common JavaScript utilities for course generator games
 */

// Global game utilities
window.CourseGenerator = {
  // Toast notification system
  showToast: function (message, type = "info", duration = 3000) {
    const toast = document.createElement("div");
    toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white fade-in`;

    switch (type) {
      case "success":
        toast.className += " bg-green-500";
        break;
      case "error":
        toast.className += " bg-red-500";
        break;
      case "warning":
        toast.className += " bg-yellow-500";
        break;
      default:
        toast.className += " bg-blue-500";
    }

    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, duration);
  },

  // Score calculation utilities
  calculateScore: function (correct, total, maxScore = 10) {
    const percentage = correct / total;
    return Math.round(percentage * maxScore);
  },

  // Format score message
  getScoreMessage: function (score, maxScore) {
    const percentage = (score / maxScore) * 100;

    if (percentage >= 90)
      return { message: "Excellent work! 🎉", class: "text-green-600" };
    if (percentage >= 80)
      return { message: "Great job! 👏", class: "text-green-600" };
    if (percentage >= 70)
      return { message: "Good work! 👍", class: "text-blue-600" };
    if (percentage >= 60)
      return { message: "Nice effort! 😊", class: "text-blue-600" };
    if (percentage >= 50)
      return { message: "Keep trying! 💪", class: "text-orange-600" };
    return { message: "Practice makes perfect! 📚", class: "text-orange-600" };
  },

  // Timer utilities
  Timer: class {
    constructor(duration, onTick, onComplete) {
      this.duration = duration;
      this.timeLeft = duration;
      this.onTick = onTick;
      this.onComplete = onComplete;
      this.interval = null;
      this.isRunning = false;
    }

    start() {
      if (this.isRunning) return;

      this.isRunning = true;
      this.interval = setInterval(() => {
        this.timeLeft--;

        if (this.onTick) {
          this.onTick(this.timeLeft, this.duration);
        }

        if (this.timeLeft <= 0) {
          this.stop();
          if (this.onComplete) {
            this.onComplete();
          }
        }
      }, 1000);
    }

    stop() {
      if (this.interval) {
        clearInterval(this.interval);
        this.interval = null;
      }
      this.isRunning = false;
    }

    reset() {
      this.stop();
      this.timeLeft = this.duration;
    }

    formatTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes}:${seconds.toString().padStart(2, "0")}`;
    }
  },

  // Local storage utilities
  saveProgress: function (gameId, data) {
    try {
      const key = `course_generator_${gameId}`;
      localStorage.setItem(
        key,
        JSON.stringify({
          ...data,
          timestamp: Date.now(),
        })
      );
    } catch (error) {
      console.warn("Could not save progress:", error);
    }
  },

  loadProgress: function (gameId) {
    try {
      const key = `course_generator_${gameId}`;
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.warn("Could not load progress:", error);
      return null;
    }
  },

  // Animation utilities
  animateScore: function (element, startScore, endScore, duration = 1000) {
    const startTime = performance.now();

    function animate(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (ease-out)
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const currentScore = Math.round(
        startScore + (endScore - startScore) * easeOut
      );

      element.textContent = currentScore;

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  },

  // Shuffle array utility
  shuffle: function (array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  },

  // Debounce utility
  debounce: function (func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Accessibility utilities
  announceToScreenReader: function (message) {
    const announcement = document.createElement("div");
    announcement.setAttribute("aria-live", "polite");
    announcement.setAttribute("aria-atomic", "true");
    announcement.className = "sr-only";
    announcement.textContent = message;

    document.body.appendChild(announcement);

    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  },

  // Keyboard navigation helper
  setupKeyboardNavigation: function (elements, options = {}) {
    const { loop = true, onEnter = null, onEscape = null } = options;

    let currentIndex = 0;

    elements.forEach((element, index) => {
      element.setAttribute("tabindex", index === 0 ? "0" : "-1");

      element.addEventListener("keydown", (e) => {
        switch (e.key) {
          case "ArrowUp":
          case "ArrowLeft":
            e.preventDefault();
            currentIndex =
              currentIndex > 0
                ? currentIndex - 1
                : loop
                ? elements.length - 1
                : 0;
            updateFocus();
            break;

          case "ArrowDown":
          case "ArrowRight":
            e.preventDefault();
            currentIndex =
              currentIndex < elements.length - 1
                ? currentIndex + 1
                : loop
                ? 0
                : elements.length - 1;
            updateFocus();
            break;

          case "Enter":
          case " ":
            e.preventDefault();
            if (onEnter) onEnter(element, index);
            break;

          case "Escape":
            if (onEscape) onEscape(element, index);
            break;
        }
      });

      element.addEventListener("focus", () => {
        currentIndex = index;
        updateFocus();
      });
    });

    function updateFocus() {
      elements.forEach((el, index) => {
        el.setAttribute("tabindex", index === currentIndex ? "0" : "-1");
      });
      elements[currentIndex].focus();
    }

    return {
      focusFirst: () => {
        currentIndex = 0;
        updateFocus();
      },
      focusLast: () => {
        currentIndex = elements.length - 1;
        updateFocus();
      },
    };
  },

  // Confetti effect for celebrations
  confetti: function () {
    // Simple confetti implementation
    const colors = ["#7c3aed", "#a855f7", "#10b981", "#f59e0b", "#ef4444"];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
      setTimeout(() => {
        const confetti = document.createElement("div");
        confetti.style.cssText = `
          position: fixed;
          top: -10px;
          left: ${Math.random() * 100}%;
          width: 10px;
          height: 10px;
          background: ${colors[Math.floor(Math.random() * colors.length)]};
          z-index: 9999;
          pointer-events: none;
          animation: confetti-fall 3s linear forwards;
        `;

        document.body.appendChild(confetti);

        setTimeout(() => {
          confetti.remove();
        }, 3000);
      }, i * 50);
    }
  },
};

// Add confetti CSS animation
const style = document.createElement("style");
style.textContent = `
  @keyframes confetti-fall {
    to {
      transform: translateY(100vh) rotate(360deg);
      opacity: 0;
    }
  }
  
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
`;
document.head.appendChild(style);

// Initialize common functionality when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Add focus-visible polyfill for older browsers
  if (!CSS.supports("selector(:focus-visible)")) {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        document.body.classList.add("using-keyboard");
      }
    });

    document.addEventListener("mousedown", () => {
      document.body.classList.remove("using-keyboard");
    });
  }

  // Set up global keyboard shortcuts
  document.addEventListener("keydown", (e) => {
    // ESC to go back (if back button exists)
    if (e.key === "Escape") {
      const backButton = document.querySelector('[href="../"]');
      if (backButton) {
        backButton.click();
      }
    }
  });
});

// Export for use in modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = window.CourseGenerator;
}
