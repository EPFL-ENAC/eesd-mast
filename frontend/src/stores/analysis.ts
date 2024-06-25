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

export const useAnalysisStore = defineStore('analysis', () => {
  const counts = ref<Counts>({
    experiments_count: 0,
    models_count: 0,
    references_count: 0,
    run_results_count: 0,
  });

  const frequencies = ref<ExperimentFrequencies | null>(null);
  const experimentsParallelCounts = ref<ExperimentParallelCount[]>([]);
  const runResultsVulnerabilities = ref<RunResultVulnerability[]>([]);
  const runResultsFragilities = ref<RunResultFragility[]>([]);
  const filters = ref<FieldValue[]>([]);

  const buildings_counts = computed(() => {
    if (frequencies.value === null) return 0;
    const model_freqs = frequencies.value.model_files;
    return (
      (model_freqs['0'] ? model_freqs['0'] : 0) +
      (model_freqs['1'] ? model_freqs['1'] : 0)
    );
  });

  const models_counts = computed(() => {
    if (frequencies.value === null) return 0;
    const model_freqs = frequencies.value.model_files;
    return model_freqs['1'] ? model_freqs['1'] : 0;
  });

  async function loadCounts() {
    api.get<Counts>('/analysis/counts').then((resp) => {
      counts.value = resp.data;
    });
  }

  async function loadExperimentsFrequencies() {
    const query: QueryParams = {
      filter: JSON.stringify(makeDbFilters(true)),
      sort: undefined,
      range: undefined,
    };
    api({
      method: 'get',
      url: '/analysis/experiments/frequencies',
      params: query,
    }).then((resp) => {
      frequencies.value = resp.data;
    });
  }

  async function loadExperimentsParallelCounts() {
    const query: QueryParams = {
      filter: JSON.stringify(makeDbFilters(true)),
      sort: undefined,
      range: undefined,
    };
    api({
      method: 'get',
      url: '/analysis/experiments/parallel-counts',
      params: query,
    }).then((resp) => {
      experimentsParallelCounts.value = resp.data;
    });
  }

  async function loadRunResultsVulnerabilities() {
    const query: QueryParams = {
      filter: JSON.stringify(makeDbFilters(false)),
      sort: undefined,
      range: undefined,
    };
    api({
      method: 'get',
      url: '/analysis/run_results/vulnerabilities',
      params: query,
    }).then((resp) => {
      runResultsVulnerabilities.value = resp.data;
    });
  }

  async function loadRunResultsFragilities() {
    const query: QueryParams = {
      filter: JSON.stringify(makeDbFilters(false)),
      sort: undefined,
      range: undefined,
    };
    api({
      method: 'get',
      url: '/analysis/run_results/fragilities',
      params: query,
    }).then((resp) => {
      runResultsFragilities.value = resp.data;
    });
  }

  async function loadExperimentsAnalysis() {
    loadExperimentsFrequencies();
    loadExperimentsParallelCounts();
    loadRunResultsVulnerabilities();
    loadRunResultsFragilities();
  }

  function makeDbFilters(with3dModel: boolean) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const dbFilters: { [Key: string]: any } = {};
    filters.value
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
        if (filter.field === 'diaphragm_material' && filter.value === 'Mixed') {
          val = [...MIXED_MATERIAL];
        }
        if (filter.field === 'diaphragm_material' && filter.value === 'None') {
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
  }

  async function updateFilters(criteria: FieldValue | undefined) {
    if (!criteria) {
      resetFilters();
    } else {
      const index = filters.value.findIndex((f) => f.field === criteria.field);
      if (index >= 0) {
        if (filters.value[index].value === criteria.value) {
          // reapply the same filter means remove it
          filters.value.splice(index, 1);
        } else {
          filters.value[index] = criteria;
        }
      } else {
        filters.value.push(criteria);
      }
      loadExperimentsAnalysis();
    }
  }

  async function resetFilters() {
    filters.value = [];
    loadExperimentsAnalysis();
  }

  return {
    counts,
    frequencies,
    experimentsParallelCounts,
    runResultsFragilities,
    runResultsVulnerabilities,
    filters,
    buildings_counts,
    models_counts,
    resetFilters,
    updateFilters,
    loadCounts,
    loadExperimentsAnalysis,
  };
});
