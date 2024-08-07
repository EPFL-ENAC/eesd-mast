const colorPalettes: { [Key: string]: { [Key: string]: string } } = {
  masonry_unit_material: {
    Clay: '#d62728',
    Stone: '#1f77b4',
    Limestone: '#1f77b4',
    'Calcareous sandstone': '#9467bd',
    Concrete: '#7f7f7f',
    'Calcium silicate': '#2ca02c',
    Granite: '#8c564b',
    Adobe: '#ff7f0e',
    'Neopolitan tuff stone': '#e377c2',
    'Tuff stone': '#bcbd22',
    'Calcareous tuff stone': '#17becf',
  },
  diaphragm_material: {
    Timber: '#8c564b',
    RC: '#7f7f7f',
    Mixed: '#ffd92f',
    'Hollow tile slab': '#8da0cb',
    'Steel & bricks': '#e78ac3',
    'RC & Timber': '#a6d854',
    'N/A': '#9467bd',
    None: '#9467bd',
  },
  storeys_nb: {
    '1': '#a8ddb5',
    '2': '#7bccc4',
    '3': '#4eb3d3',
    '4': '#2b8cbe',
    '5': '#08589e',
  },
  test_scale: {
    '1': '#7a0177',
    '2/3': '#c51b8a',
    '1/2': '#f768a1',
    '1/3': '#fbb4b9',
    '1/4': '#feebe2',
  },
  model_files: {
    No: '#AD9DD1',
    Yes: '#F7B7E7',
  },
};

export function getFieldValueColor(
  field: string,
  value: string | null
): string {
  if (value === null) {
    return '#000000';
  }
  return colorPalettes[field][value] || '#000000';
}

const dgColors: { [Key: string]: string } = {
  '1': 'blue',
  '2': 'green',
  '3': 'yellow',
  '4': 'orange',
  '5': 'red',
};

export function getDgColor(dg: string): string {
  return dgColors[dg] || '#000000';
}
