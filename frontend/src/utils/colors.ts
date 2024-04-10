const colorPalettes: { [Key: string]: { [Key: string]: string } } = {
  masonry_unit_material: {
    Clay: '#d62728',
    Stone: '#1f77b4',
    Limestone: '#1f77b4',
    'Calcareous sandstone': '#2ca02c',
    Concrete: '#7f7f7f',
    'Calcium silicate': '#9467bd',
    Granite: '#8c564b',
    Adobe: '#e377c2',
    'Neopolitan tuff stone': '#ff7f0e',
    'Tuff stone': '#bcbd22',
    'Calcareous tuff stone': '#17becf',
  },
  diaphragm_material: {
    Timber: '#fc8d62',
    RC: '#66c2a5',
    'Hollow tile slab': '#8da0cb',
    'Steel & bricks': '#e78ac3',
    'RC & Timber': '#a6d854',
    'N/A': '#ffd92f',
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
};

export function getFieldValueColor(field: string, value: string): string {
  return colorPalettes[field][value] || '#000000';
}
