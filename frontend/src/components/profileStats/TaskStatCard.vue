<template>
    <div class="task-card" :style="cardStyle">
      <div class="card-content">
        <div class="header">
          <span class="task-number">Задание #{{ taskNumber }}</span>
        </div>

        <div class="progress-container">
          <div class="progress-background"></div>
          <div
            class="progress-fill"
            :style="progressStyle"
            :class="progressClass"
          ></div>
        </div>

        <div class="percentage">{{ taskCompletion }}%</div>
      </div>
    </div>
  </template>

  <script>
  export default {
    props: {
      taskNumber: {
        type: Number,
        required: true,
        validator: value => value >= 1 && value <= 27
      },
      taskCompletion: {
        type: Number,
        required: true,
        validator: value => value >= 0 && value <= 100
      }
    },
    computed: {
      progressStyle() {
        return { width: `${this.taskCompletion}%` };
      },
      progressClass() {
        return {
          'low': this.taskCompletion < 30,
          'medium': this.taskCompletion >= 30 && this.taskCompletion < 70,
          'high': this.taskCompletion >= 70
        };
      },
      cardStyle() {
        return {
          background: `linear-gradient(135deg,
            rgba(245, 247, 250, 0.9) 0%,
            rgba(240, 242, 245, 0.9) 100%)`
        };
      }
    }
  };
  </script>

  <style scoped>
  .task-card {
    width: 200px;
    padding: 1.5rem;
    border-radius: 16px;
    backdrop-filter: blur(4px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin: 0 12px;
  }

  .task-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  }

  .header {
    margin-bottom: 1.2rem;
  }

  .task-number {
    font-size: 1.1rem;
    color: #4a5568;
    font-weight: 500;
    letter-spacing: -0.02em;
  }

  .progress-container {
    position: relative;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    background: rgba(237, 242, 247, 0.6);
  }

  .progress-fill {
    position: absolute;
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .low { background: #F6AD55; }
  .medium { background: #63B3ED; }
  .high { background: #68D391; }

  .percentage {
    text-align: right;
    margin-top: 0.8rem;
    font-size: 1.4rem;
    font-weight: 600;
    color: #2d3748;
    letter-spacing: -0.03em;
  }
  </style>
