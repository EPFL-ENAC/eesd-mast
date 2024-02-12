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
}

export interface RunResult extends DBModel {
  run_id: string;
  experiment_id: number;
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
