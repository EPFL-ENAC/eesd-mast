import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import { Metrics } from 'src/components/models';

interface State {
  metrics: Metrics;
}

export const useAnalysisStore = defineStore('analysis', {
  state: (): State => ({
    metrics: {
      experiments_count: 0,
      references_count: 0,
      run_results_count: 0,
    },
  }),
  getters: {
    loadMetrics: (state) => {
      return async () => {
        const resp = await api.get<Metrics>('/analysis/metrics');
        state.metrics = resp.data;
        return state.metrics;
      };
    },
  },
  actions: {},
});
