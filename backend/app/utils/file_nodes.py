class FileNode:
    def __init__(self, name, path=None, is_file=False):
        self.name = name
        self.path = path
        self.is_file = is_file
        self.children = [] if not is_file else None

    def add_file(self, file_ref):
        current_node = self
        parts = file_ref["name"].split('/')

        for part in parts:
            matching_child = next(
                (child for child in current_node.children if child.name == part), None)

            if matching_child is None:
                is_file = True if part == parts[-1] else False
                path = file_ref["path"] if is_file else None
                new_node = FileNode(part, path, is_file)
                current_node.children.append(new_node)
                current_node = new_node
            else:
                current_node = matching_child

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "is_file": self.is_file,
            "children": [child.to_dict() for child in self.children] if self.children else None
        }
