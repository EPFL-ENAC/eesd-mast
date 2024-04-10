export const STONES: string[] = [
  'Limestone',
  'Calcareous sandstone',
  'Neopolitan tuff stone',
  'Tuff stone',
  'Calcareous tuff stone',
  'Granite',
];

export const MASONRY_UNIT_MATERIAL: string[] = [
  'Clay',
  'Calcareous sandstone',
  'Calcium silicate',
  'Granite',
  'Limestone',
  'Tuff stone',
  'Concrete',
  'Adobe',
  'Calcareous tuff stone',
  'Neopolitan tuff stone',
];

export const MASONRY_UNIT_TYPE: string[] = [
  'Hollow brick',
  'Solid brick',
  'Dressed stone',
  'Undressed stone',
];

export const STOREYS_NB: string[] = ['1', '2', '3', '4', '5'];

export const WALL_LEAVES_NB: string[] = ['1', '2', '3'];

export const TEST_SCALE: string[] = [
  '1',
  '0.667',
  '0.5',
  '0.333',
  '0.25',
  '0.1',
];

export const MIXED_MATERIAL: string[] = [
  'RC & Timber',
  'Steel & bricks',
  'Hollow tile slab',
];

export const DIAPHRAGM_MATERIAL: string[] = [
  'RC',
  'Timber',
  'RC & Timber',
  'Steel & bricks',
  'Hollow tile slab',
  null,
];

export const RETROFITTING_APPLICATION: string[] = [
  'Not present',
  'From beginning',
  'After damage',
];

export const SIMULTANEOUS_EXCITATIONS_NB: string[] = ['1', '2', '3'];

export function isStone(value: string | null): boolean {
  return STONES.includes(value);
}

export function isMixedMaterial(value: string | null): boolean {
  return MIXED_MATERIAL.includes(value);
}
