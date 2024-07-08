import re


class MermaidERD:
    def __init__(self, title="Entity Relationship Diagram"):
        self.title = title
        self.entities = []
        self.relationships = []

    def add_entity(self, entity_name: str, attributes: list[dict]):
        attr_str = "\n  ".join(self.sanitize_attributes(attributes))
        self.entities.append(f'{entity_name} {{\n  {attr_str}\n}}')

    def sanitize_attributes(self, attributes):
        # Escaping is still in progress issue:
        # https://github.com/mermaid-js/mermaid/issues/5123
        _attributes = []
        # re.sub('[^a-zA-Z0-9 \n\.]', '', my_str)
        for attribute in attributes:
            # replace spaces with "-"
            column_name = re.sub(r'\s+', '-', attribute["column_name"])
            column_type = re.sub(r'\s+', '-', attribute["column_type"])
            # replace special characters with underscore
            column_name = re.sub(r'[^a-zA-Z0-9\-()]', '_', column_name)
            column_type = re.sub(r'[^a-zA-Z0-9\-()]', '_', column_type)
            _attributes.append(f'{column_name} {column_type}')
        return _attributes

    def add_relationship(self, entity1, entity2, relationship, rel_type="1:N"):
        # Define relationship labels based on relationship type
        if rel_type == "1:1":
            rel_label = "||--||"
        elif rel_type == "1:N":
            rel_label = "||--o{"
        elif rel_type == "N:1":
            rel_label = "}o--||"
        elif rel_type == "N:N":
            rel_label = "}o--o{"
        else:
            raise ValueError(f"Invalid relationship type: {rel_type}")

        self.relationships.append(f'{entity1} {rel_label} {entity2} : {relationship}')

    def generate_code(self):
        code = ["---", self.title, "---", "erDiagram"]
        code.extend(self.entities)
        code.extend(self.relationships)
        return "\n".join(code)
