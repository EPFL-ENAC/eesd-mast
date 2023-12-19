import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';

interface State {
  references: any;
}

export const useReferencesStore = defineStore('references', {
  state: (): State => ({
    references: {},
  }),
  getters: {
    fetchReference: (state) => {
      return async (id: string) => {
        if (!state.references[id]) {
          const resp = await api.get(`/references/${id}`);
          state.references[id] = resp.data;
        }
        return state.references[id];
      };
    },
  },
  actions: {},
});
