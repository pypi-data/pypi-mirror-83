class BeanFindingError(Exception):
    pass


class NoSuchBeanError(BeanFindingError):
    pass


class MultipleBeanInstancesError(BeanFindingError):
    pass


class BeanIdAlreadyExistsError(Exception):
    pass


class ContextInitError(Exception):
    pass
