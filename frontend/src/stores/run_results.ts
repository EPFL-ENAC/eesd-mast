import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import { RunResult } from 'src/components/models';

export const useRunResultsStore = defineStore('run_results', () => {
  const run_results = ref([] as RunResult[]);

  const run_results_digest = computed(() => {
    return run_results.value
      .filter((run) => !['Initial', 'Final'].includes(run.run_id))
      .sort((a, b) => (a.id < b.id ? -1 : 1)); // sort by (unique) id in the db
  });

  async function initRunResults(id: number) {
    const query = {
      experiment_id: id,
    };
    return api({
      method: 'get',
      url: '/run_results',
      params: {
        filter: JSON.stringify(query),
      },
    }).then((resp) => (run_results.value = resp.data));
  }

  return {
    run_results,
    run_results_digest,
    initRunResults,
  };
});
