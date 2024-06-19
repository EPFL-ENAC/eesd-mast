import { defineStore } from 'pinia';
import { FieldValue, Reference } from 'src/components/models';
import { STONES, MIXED_MATERIAL } from 'src/utils/criteria';

interface RefenceSelection {
  label: string;
  value: Reference;
}

interface State {
  with3dModel: boolean | null;
  selections: string[];
  referenceSelections: RefenceSelection[];
}

export const useFiltersStore = defineStore('filters', {
  state: (): State => ({
    with3dModel: null,
    selections: [],
    referenceSelections: [],
  }),
  getters: {
    dbFilters: (state) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const dbFilters: { [Key: string]: any } = {};
      state.selections.forEach((selection) => {
        const tokens = selection.split(':');
        if (tokens.length === 2) {
          const [field, value] = tokens;
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          let val: any = [
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
          if (field === 'masonry_unit_material' && value === 'Stone') {
            //val = STONES;
            if (dbFilters[field]) {
              dbFilters[field].push(...STONES);
            } else {
              dbFilters[field] = [...STONES];
            }
          } else if (dbFilters[field]) {
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
      if (state.with3dModel !== null) {
        dbFilters['model_files'] = { $exists: state.with3dModel };
      }
      return dbFilters;
    },
  },
  actions: {
    resetFilters() {
      this.selections = [];
      this.referenceSelections = [];
    },
    applySelections(filters: FieldValue[]) {
      this.with3dModel = null;
      filters.forEach((filter) => {
        if (filter.field === 'diaphragm_material' && filter.value === 'Mixed') {
          MIXED_MATERIAL.forEach((val) =>
            this.selections.push(`${filter.field}:${val}`)
          );
        } else if (
          filter.field === 'diaphragm_material' &&
          filter.value === 'None'
        ) {
          this.selections.push(`${filter.field}:null`);
        } else if (filter.field === 'model_files') {
          this.with3dModel = filter.value === 'Yes';
        } else {
          this.selections.push(`${filter.field}:${filter.value}`);
        }
      });
    },
  },
});
