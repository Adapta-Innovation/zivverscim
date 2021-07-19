class ZivverMissingRequiredFields(Exception):
    """When there are missing required fields missing"""
    pass


class ZivverCRUDError(Exception):
    """When there are erros in the response"""
    pass
