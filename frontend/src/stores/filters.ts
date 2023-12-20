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
      state.selections
        .filter(
          (selection) =>
            selection !== 'storeys_nb' && selection !== 'wall_leaves_nb'
        )
        .forEach((selection) => {
          const tokens = selection.split(':');
          if (tokens.length === 2) {
            const [field, value] = tokens;
            if (dbFilters[field]) {
              dbFilters[field].push(value);
            } else {
              dbFilters[field] = [value];
            }
          }
        });
      if (state.selections.indexOf('storeys_nb') > -1) {
        dbFilters['storeys_nb'] = state.storeysNb;
      }
      if (state.selections.indexOf('wall_leaves_nb') > -1) {
        dbFilters['wall_leaves_nb'] = state.wallLeavesNb;
      }
      if (state.references.length > 0) {
        dbFilters['reference_id'] = state.references.map((ref) => ref.id);
      }
      return dbFilters;
    },
  },
  actions: {},
});
