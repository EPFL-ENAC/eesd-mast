import vtk


def vtk2p(input_file: str, output_file: str):
    """Convert an unstructured grid in VTK format to polydata in VTP format.

    Args:
        input_file (_type_): Path to a local file containing an unstructured grid in VTK format.
        output_file (_type_): Path to a local file where the polydata in VTP format will be saved.
    """
    # Create a reader for the VTK file with unstructured grid data
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(input_file)

    # Read the VTK file
    reader.Update()

    # Get the unstructured grid from the reader
    unstructured_grid = reader.GetOutput()

    # Convert the unstructured grid to polydata (if needed)
    geometry_filter = vtk.vtkGeometryFilter()
    geometry_filter.SetInputData(unstructured_grid)
    geometry_filter.Update()

    # Get the polydata from the geometry filter
    polydata = geometry_filter.GetOutput()

    # Create a writer for the VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)

    # Set the input polydata for the writer
    writer.SetInputData(polydata)

    # Write the VTP file
    writer.Write()
