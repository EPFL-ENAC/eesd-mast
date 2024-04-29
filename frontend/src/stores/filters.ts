import { defineStore } from 'pinia';
import { FieldValue, Reference } from 'src/components/models';
import { STONES, MIXED_MATERIAL } from 'src/utils/criteria';

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
          let val = [
            'storeys_nb',
            'test_scale',
            'wall_leaves_nb',
            'simultaneous_excitations_nb',
          ].includes(field)
            ? Number(value)
            : value;
          if (val === 'null') {
            val = null;
          }
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
    applySelections(filters: FieldValue[]) {
      filters.forEach((filter) => {
        if (
          filter.field === 'masonry_unit_material' &&
          filter.value === 'Stone'
        ) {
          STONES.forEach((val) =>
            this.selections.push(`${filter.field}:${val}`)
          );
        } else if (
          filter.field === 'diaphragm_material' &&
          filter.value === 'Mixed'
        ) {
          MIXED_MATERIAL.forEach((val) =>
            this.selections.push(`${filter.field}:${val}`)
          );
        } else {
          this.selections.push(`${filter.field}:${filter.value}`);
        }
      });
    },
  },
});
