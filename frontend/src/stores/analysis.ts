import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import {
  ExperimentFrequencies,
  Metrics,
  FieldValue,
} from 'src/components/models';
import { QueryParams } from 'src/utils/pagination';

interface State {
  metrics: Metrics;
  frequencies: ExperimentFrequencies | null;
  filters: FieldValue[];
}

export const useAnalysisStore = defineStore('analysis', {
  state: (): State => ({
    metrics: {
      experiments_count: 0,
      references_count: 0,
      run_results_count: 0,
    },
    frequencies: null,
    filters: [],
  }),
  getters: {},
  actions: {
    loadMetrics() {
      api.get<Metrics>('/analysis/metrics').then((resp) => {
        this.metrics = resp.data;
      });
    },
    loadFrequencies() {
      const dbFilters: { [Key: string]: (string | number | null)[] } = {};
      this.filters.forEach((filter) => {
        const val = ['storeys_nb'].includes(filter.field)
          ? Number(filter.value)
          : filter.value;
        if (dbFilters[filter.field]) {
          dbFilters[filter.field].push(val);
        } else {
          dbFilters[filter.field] = [val];
        }
      });
      const query: QueryParams = {
        filter: JSON.stringify(dbFilters),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/frequencies',
        params: query,
      }).then((resp) => {
        this.frequencies = resp.data;
      });
    },
    updateFilters(criteria: FieldValue | undefined) {
      if (!criteria) {
        this.resetFilters();
      } else {
        const index = this.filters.findIndex((f) => f.field === criteria.field);
        if (index >= 0) {
          if (this.filters[index].value === criteria.value) {
            // reapply the same filter means remove it
            this.filters.splice(index, 1);
          } else {
            this.filters[index] = criteria;
          }
        } else {
          this.filters.push(criteria);
        }
        this.loadFrequencies();
      }
    },
    resetFilters() {
      this.filters = [];
      this.loadFrequencies();
    },
  },
});
