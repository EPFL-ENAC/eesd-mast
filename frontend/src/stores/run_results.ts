import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import { RunResult } from 'src/components/models';

interface State {
  run_results: { [Key: number]: RunResult[] };
}

export const useRunResultsStore = defineStore('run_results', {
  state: (): State => ({
    run_results: {},
  }),
  getters: {
    fetchRunResults: (state) => {
      return async (id: number): Promise<RunResult[]> => {
        if (!state.run_results[id]) {
          const query = {
            experiment_id: id,
          };
          const resp = await api({
            method: 'get',
            url: '/run_results',
            params: {
              filter: JSON.stringify(query),
            },
          });
          state.run_results[id] = resp.data;
        }
        return state.run_results[id];
      };
    },
  },
  actions: {},
});
