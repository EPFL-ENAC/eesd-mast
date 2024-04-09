import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import {
  ExperimentFrequencies,
  ExperimentParallelCount,
  Counts,
  FieldValue,
} from 'src/components/models';
import { QueryParams } from 'src/utils/pagination';

interface State {
  counts: Counts;
  frequencies: ExperimentFrequencies | null;
  parallelCounts: ExperimentParallelCount[] | [];
  filters: FieldValue[];
}

export const useAnalysisStore = defineStore('analysis', {
  state: (): State => ({
    counts: {
      experiments_count: 0,
      references_count: 0,
      run_results_count: 0,
    },
    frequencies: null,
    parallelCounts: [],
    filters: [],
  }),
  getters: {},
  actions: {
    loadCounts() {
      api.get<Counts>('/analysis/counts').then((resp) => {
        this.counts = resp.data;
      });
    },
    loadExperimentsFrequencies() {
      const query: QueryParams = {
        filter: JSON.stringify(this.makeDbFilters()),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/experiments/frequencies',
        params: query,
      }).then((resp) => {
        this.frequencies = resp.data;
      });
    },
    loadExperimentsParallelCounts() {
      const query: QueryParams = {
        filter: JSON.stringify(this.makeDbFilters()),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/experiments/parallel-counts',
        params: query,
      }).then((resp) => {
        this.parallelCounts = resp.data;
      });
    },
    loadExperimentsAnalysis() {
      this.loadExperimentsFrequencies();
      this.loadExperimentsParallelCounts();
    },
    makeDbFilters() {
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
      return dbFilters;
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
        this.loadExperimentsFrequencies();
        this.loadExperimentsParallelCounts();
      }
    },
    resetFilters() {
      this.filters = [];
      this.loadExperimentsAnalysis();
    },
  },
});
