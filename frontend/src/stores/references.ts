import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';

interface State {
  references: any;
  reference_experiments: any;
}

export const useReferencesStore = defineStore('references', {
  state: (): State => ({
    references: {},
    reference_experiments: {},
  }),
  getters: {
    fetchReference: (state) => {
      return async (id: number) => {
        if (!state.references[id]) {
          const resp = await api.get(`/references/${id}`);
          state.references[id] = resp.data;
        }
        return state.references[id];
      };
    },
    fetchExperiments: (state) => {
      return async (id: number) => {
        if (!state.references[id]) {
          const query = {
            reference_id: id,
          };
          const resp = await api({
            method: 'get',
            url: '/experiments',
            params: {
              filter: JSON.stringify(query),
            },
          });
          state.reference_experiments[id] = resp.data;
        }
        return state.reference_experiments[id];
      };
    },
  },
  actions: {},
});
