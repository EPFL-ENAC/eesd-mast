import { defineStore } from 'pinia';
import { Reference } from 'src/components/models';

interface RefenceSelection {
  label: string;
  value: Reference;
}

interface State {
  selections: string[];
  references: Reference[];
  referenceSelections: RefenceSelection[];
}

export const useFiltersStore = defineStore('filters', {
  state: (): State => ({
    selections: [],
    references: [],
    referenceSelections: [],
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
      if (state.referenceSelections && state.referenceSelections.length > 0) {
        dbFilters['reference_id'] = state.referenceSelections.map(
          (ref) => ref.value.id
        );
      }
      if (state.references && state.references.length > 0) {
        const ids = state.references.map((ref) => ref.id);
        if (dbFilters['reference_id']) {
          dbFilters['reference_id'].push(...ids);
        } else {
          dbFilters['reference_id'] = ids;
        }
      }
      return dbFilters;
    },
  },
  actions: {
    resetFilters() {
      this.selections = [];
      this.references = [];
      this.referenceSelections = [];
    },
  },
});
