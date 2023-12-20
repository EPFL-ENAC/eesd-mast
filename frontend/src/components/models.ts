export interface DBModel {
  id: number;
  [Key: string]: unknown;
}

export interface Reference extends DBModel {
  reference: string;
  link_to_experimental_paper: string | null;
  corresponding_author_email: string;
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
}

export interface RunResult extends DBModel {
  experiment_id: number;
}
