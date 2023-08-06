
def main(context):
    """
    Items in the main navigation bar can be direct links, or dropdowns with
    subitems. This context preprocessor adds a boolean field
    ``has_subitems`` that tells which one of them every element is. It
    also adds a ``slug`` field to be used as a CSS id.
    """
    for i, item in enumerate(context["navbar"]):
        context["navbar"][i] = dict(
            item,
            has_subitems=isinstance(item["target"], list),
            slug=(item["name"].replace(" ", "-").lower()),
        )
    return context
