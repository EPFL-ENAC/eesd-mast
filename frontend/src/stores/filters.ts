import { defineStore } from 'pinia';
import { Reference } from 'src/components/models';

interface State {
  selections: string[];
  storeysNb: number;
  wallLeavesNb: number;
  references: Reference[];
}

export const useFiltersStore = defineStore('filters', {
  state: (): State => ({
    selections: [],
    storeysNb: 1,
    wallLeavesNb: 1,
    references: [],
  }),
  getters: {
    dbFilters: (state) => {
      const dbFilters = {};
      state.selections.forEach((selection) => {
        const tokens = selection.split(':');
        if (tokens.length === 2) {
          const [field, value] = tokens;
          const val = [
            'storeys_nb',
            'wall_leaves_nb',
            'simultaneous_excitations_nb',
          ].includes(field)
            ? Number(value)
            : value;
          if (dbFilters[field]) {
            dbFilters[field].push(val);
          } else {
            dbFilters[field] = [val];
          }
        }
      });
      if (state.references.length > 0) {
        dbFilters['reference_id'] = state.references.map((ref) => ref.id);
      }
      return dbFilters;
    },
  },
  actions: {},
});
