import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import { NumericalModel } from 'src/components/models';

interface State {
  numerical_model: NumericalModel;
}

export const useNumericalModelsStore = defineStore('numerical_models', {
  state: (): State => ({
    numerical_model: {} as NumericalModel,
  }),
  getters: {
    fetchNumericalModel: (state) => {
      return async (id: number): Promise<NumericalModel> => {
        if (state.numerical_model.experiment_id !== id) {
          state.numerical_model = {} as NumericalModel;
          const resp = await api({
            method: 'get',
            url: `/experiments/${id}/numerical_model`,
          });
          console.log(resp);
          if (resp.status === 200) {
            state.numerical_model = resp.data;
          }
        }
        return state.numerical_model;
      };
    },
  },
  actions: {},
});
