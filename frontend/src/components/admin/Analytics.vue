<template>
  <div class="analytics">
    <h2>Аналитика выполнения заданий</h2>

    <div v-if="loading" class="loading">Загрузка данных...</div>
    <div v-else-if="error" class="error">Ошибка загрузки данных</div>

    <div v-else class="analytics-grid">
      <div
        v-for="task in statsData"
        :key="task.task_type"
        class="analytics-card"
        :style="cardStyle"
      >
        <div class="card-header">
          <span class="task-type">Тип задания {{ task.task_type }}</span>
        </div>

        <div class="progress-container">
          <div class="progress-background"></div>
          <div
            class="progress-fill"
            :style="{ width: `${task.completed_percent}%` }"
            :class="getProgressClass(task.completed_percent)"
          ></div>
        </div>

        <div class="percentage">{{ task.completed_percent.toFixed(1) }}%</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      error: false,
      statsData: []
    };
  },
  computed: {
    cardStyle() {
      return {
        background: `linear-gradient(135deg,
          rgba(245, 247, 250, 0.9) 0%,
          rgba(240, 242, 245, 0.9) 100%)`
      };
    }
  },
  methods: {
    getProgressClass(percent) {
      return {
        'low': percent < 30,
        'medium': percent >= 30 && percent < 70,
        'high': percent >= 70
      };
    },
    async fetchStats() {
      try {
        const response = await fetch('https://127.0.0.1/api/v1/stats/admin/');
        if (!response.ok) throw new Error('Ошибка сервера');
        this.statsData = await response.json();
        this.loading = false;
      } catch (error) {
        console.error('Ошибка:', error);
        this.error = true;
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchStats();
  }
};
</script>

<style scoped>
.analytics {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  color: #2d3748;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  text-align: center;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.analytics-card {
  padding: 1.5rem;
  border-radius: 16px;
  backdrop-filter: blur(4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.analytics-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
}

.card-header {
  margin-bottom: 1.2rem;
}

.task-type {
  font-size: 1.1rem;
  color: #4a5568;
  font-weight: 500;
  display: block;
  margin-bottom: 0.5rem;
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
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #718096;
}

.error {
  color: #e53e3e;
}
</style>
