class Helper():
    @staticmethod
    def build_tree(paths):
        """
        Builds a nested dictionary tree structure from a list of file paths.
        """
        tree = {}
        for path in paths:
            parts = path.split('/')
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
        return tree
    
    @staticmethod
    def to_text_tree(tree, indent=''):
        """
        Converts a nested dictionary tree into a human-readable, text-based tree string.
        """
        output = ""
        keys = tree.keys()
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            prefix = "└── " if is_last else "├── "
            output += f"{indent}{prefix}{key}\n"
            if isinstance(tree[key], dict) and tree[key]:
                new_indent = indent + ("    " if is_last else "│   ")
                output += Helper.to_text_tree(tree[key], new_indent)
        return output