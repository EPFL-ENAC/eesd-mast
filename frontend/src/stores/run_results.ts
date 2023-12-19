import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';

interface State {
  run_results: any;
}

export const useRunResultsStore = defineStore('run_results', {
  state: (): State => ({
    run_results: {},
  }),
  getters: {
    fetchRunResults: (state) => {
      return async (id: number) => {
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
