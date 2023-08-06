from tala.model.semantic_object import SemanticObject

DONE = "done"


class Done(SemanticObject):
    def __eq__(self, other):
        return isinstance(other, Done)

    def as_semantic_expression(self):
        return DONE

    def __str__(self):
        return DONE

    def __repr__(self):
        return "Done()"

    def __hash__(self):
        return hash(DONE)
