export interface DBModel {
  id: number;
  [Key: string]: unknown;
}

export interface Reference extends DBModel {
  reference: string;
  link_to_experimental_paper: string | null;
  corresponding_author_email: string;
  request_data_available: string | null;
  link_to_request_data: string | null;
}

export interface Experiment extends DBModel {
  reference_id: number;
  experiment_id: string | null;
  description: string | null;
  applied_excitation_directions: string[] | null;
  masonry_wall_thickness: number[] | null;
  internal_walls: boolean | null;
  retrofitted: boolean | null;
  open_measured_data: boolean | null;
  retrofitting_type: string[] | null;
  material_characterizations: string[] | null;
  associated_test_types: string[] | null;
  material_characterization_refs: string[] | null;
  experimental_results_reported: string[] | null;
  link_to_open_measured_data: string | null;
  crack_types_observed: string[] | null;
  files: FileNode;
  test_scale: number | null;
}

export interface RunResult extends DBModel {
  run_id: string;
  experiment_id: number;
  actual_pga_x: number | null;
  actual_pga_y: number | null;
  dg_reported: number | null;
  dg_derived: number | null;
  reported_t1_x: number | null;
  reported_t1_y: number | null;
}

export interface FileNode {
  name: string;
  path: string;
  size: number | undefined;
  alt_name: string | undefined;
  alt_path: string | undefined;
  alt_size: number | undefined;
  is_file: boolean;
  children: FileNode[] | undefined;
}

export interface RunResultFileNodes {
  top_displacement_histories: FileNode | undefined;
  global_force_displacement_curve: FileNode | undefined;
  shake_table_accelerations: FileNode | undefined;
  crack_maps: FileNode | undefined;
}

export interface Counts {
  experiments_count: number;
  references_count: number;
  run_results_count: number;
}

export interface FieldValue {
  field: string;
  value: string | number | null;
}

export interface FieldFrequencies {
  [Key: string]: number;
}

export interface ExperimentFrequencies {
  [Key: string]: FieldFrequencies;
}

export interface ExperimentParallelCount {
  masonry_unit_material: string | null;
  diaphragm_material: string | null;
  storeys_nb: number | null;
  test_scale: number | null;
  count: number;
}

export interface RunResultVulnerability {
  pgas: number[];
  dg: number;
}

export interface RunResultFragility {
  thresh: number[];
  prob: number[];
  x: number[];
  y: number[];
  dg: number;
}
