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
  test_files: FileNode | null;
  model_files: FileNode | null;
  plan_files: FileNode | null;
  test_scale: number | null;
  link_to_material_papers: string[] | null;
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
  selected: boolean | null;
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

export interface NumericalModel extends DBModel {
  experiment_id: number;
  software_used: string | null;
  software_used_comment: string | null;
  modeling_approach: string | null;
  modeling_approach_comment: string | null;
  units: string | null;
  units_comment: string | null;
  frame_elements: string | null;
  frame_elements_comment: string | null;
  diaphragm_elements: string | null;
  diaphragm_elements_comment: string | null;
  damping_model: string | null;
  damping_model_comment: string | null;
  global_geometry_def: string | null;
  global_geometry_def_comment: string | null;
  element_geometry_def: string | null;
  element_geometry_def_comment: string | null;
  mass_def: string | null;
  mass_def_comment: string | null;
  gravity_loads_def: string | null;
  gravity_loads_def_comment: string | null;
  wall_connections: string | null;
  wall_connections_comment: string | null;
  floor_connections: string | null;
  floor_connections_comment: string | null;
  base_support: string | null;
  base_support_comment: string | null;
  elastic_modulus: number | null;
  elastic_modulus_comment: string | null;
  shear_modulus: number | null;
  shear_modulus_comment: string | null;
  compression_strength: number | null;
  compression_strength_comment: string | null;
  tension_strength: number | null;
  tension_strength_comment: string | null;
  cohesion: number | null;
  cohesion_comment: string | null;
  friction_coeff: number | null;
  friction_coeff_comment: string | null;
  residual_friction_coeff: number | null;
  residual_friction_coeff_comment: string | null;
  damping_ratio: number | null;
  damping_ratio_comment: string | null;
  softening_coeff: number | null;
  softening_coeff_comment: string | null;
}
