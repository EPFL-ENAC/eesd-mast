import { api } from 'src/boot/axios';
import { defineStore } from 'pinia';
import { FieldValue, Reference } from 'src/components/models';
import { STONES, MIXED_MATERIAL } from 'src/utils/criteria';
import { RunResultFragility } from 'src/components/models';
import { QueryParams } from 'src/utils/pagination';

interface RefenceSelection {
  label: string;
  value: Reference;
}

export const useFiltersStore = defineStore('filters', () => {
  const with3dModel = ref(false);
  const selections = ref<string[]>([]);
  const referenceSelections = ref<RefenceSelection[]>([]);
  const runResultsFragilities = ref<RunResultFragility[]>([]);

  const dbFilters = computed(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const filters: { [Key: string]: any } = {};
    selections.value.forEach((selection) => {
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
          if (filters[field]) {
            filters[field].push(...STONES);
          } else {
            filters[field] = [...STONES];
          }
        } else if (filters[field]) {
          filters[field].push(val);
        } else {
          filters[field] = [val];
        }
      }
    });
    if (referenceSelections.value && referenceSelections.value.length > 0) {
      filters['reference_id'] = referenceSelections.value.map(
        (ref) => ref.value.id
      );
    }
    if (with3dModel.value) {
      filters['model_files'] = { $exists: true };
    }
    return filters;
  });

  function resetFilters() {
    selections.value = [];
    referenceSelections.value = [];
  }

  function applySelections(filters: FieldValue[]) {
    filters.forEach((filter) => {
      if (filter.field === 'diaphragm_material' && filter.value === 'Mixed') {
        MIXED_MATERIAL.forEach((val) =>
          selections.value.push(`${filter.field}:${val}`)
        );
      } else if (
        filter.field === 'diaphragm_material' &&
        filter.value === 'None'
      ) {
        selections.value.push(`${filter.field}:null`);
      } else {
        selections.value.push(`${filter.field}:${filter.value}`);
      }
    });
  }

  async function loadRunResultsFragilities() {
    const query: QueryParams = {
      filter: JSON.stringify(dbFilters.value),
      sort: undefined,
      range: undefined,
    };
    api({
      method: 'get',
      url: '/analysis/run_results/fragilities',
      params: query,
    }).then((resp) => {
      runResultsFragilities.value = resp.data;
    });
  }

  return {
    with3dModel,
    selections,
    referenceSelections,
    dbFilters,
    runResultsFragilities,
    applySelections,
    resetFilters,
    loadRunResultsFragilities,
  };
});
