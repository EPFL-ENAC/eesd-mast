import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import {
  ExperimentFrequencies,
  ExperimentParallelCount,
  RunResultVulnerability,
  RunResultFragility,
  Counts,
  FieldValue,
} from 'src/components/models';
import { QueryParams } from 'src/utils/pagination';
import { STONES, MIXED_MATERIAL } from 'src/utils/criteria';

interface State {
  counts: Counts;
  frequencies: ExperimentFrequencies | null;
  experimentsParallelCounts: ExperimentParallelCount[] | [];
  runResultsVulnerabilities: RunResultVulnerability[] | [];
  runResultsFragilities: RunResultFragility[] | [];
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
    experimentsParallelCounts: [],
    runResultsVulnerabilities: [],
    runResultsFragilities: [],
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
        filter: JSON.stringify(this.makeDbFilters(true)),
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
        filter: JSON.stringify(this.makeDbFilters(true)),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/experiments/parallel-counts',
        params: query,
      }).then((resp) => {
        this.experimentsParallelCounts = resp.data;
      });
    },
    loadRunResultsVulnerabilities() {
      const query: QueryParams = {
        filter: JSON.stringify(this.makeDbFilters(false)),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/run_results/vulnerabilities',
        params: query,
      }).then((resp) => {
        this.runResultsVulnerabilities = resp.data;
      });
    },
    loadRunResultsFragilities() {
      const query: QueryParams = {
        filter: JSON.stringify(this.makeDbFilters(false)),
        sort: undefined,
        range: undefined,
      };
      api({
        method: 'get',
        url: '/analysis/run_results/fragilities',
        params: query,
      }).then((resp) => {
        this.runResultsFragilities = resp.data;
      });
    },
    loadExperimentsAnalysis() {
      this.loadExperimentsFrequencies();
      this.loadExperimentsParallelCounts();
      this.loadRunResultsVulnerabilities();
      this.loadRunResultsFragilities();
    },
    makeDbFilters(with3dModel: boolean) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const dbFilters: { [Key: string]: any } = {};
      this.filters
        .filter((filter) => with3dModel || filter.field !== 'model_files')
        .forEach((filter) => {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          let val: any = ['storeys_nb'].includes(filter.field)
            ? Number(filter.value)
            : filter.value;
          if (
            filter.field === 'masonry_unit_material' &&
            filter.value === 'Stone'
          ) {
            val = [...STONES];
          }
          if (
            filter.field === 'diaphragm_material' &&
            filter.value === 'Mixed'
          ) {
            val = [...MIXED_MATERIAL];
          }
          if (
            filter.field === 'diaphragm_material' &&
            filter.value === 'None'
          ) {
            val = null;
          }
          if (filter.field === 'model_files') {
            val = { $exists: filter.value === 'Yes' };
          }
          if (Array.isArray(val)) {
            if (dbFilters[filter.field]) {
              dbFilters[filter.field].push(...val);
            } else {
              dbFilters[filter.field] = val;
            }
          } else if (dbFilters[filter.field]) {
            dbFilters[filter.field].push(val);
          } else if (typeof val === 'object') {
            dbFilters[filter.field] = val;
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
        this.loadExperimentsAnalysis();
      }
    },
    resetFilters() {
      this.filters = [];
      this.loadExperimentsAnalysis();
    },
  },
});
