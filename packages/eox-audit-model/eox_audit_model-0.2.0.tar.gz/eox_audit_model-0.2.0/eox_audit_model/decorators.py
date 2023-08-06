"""eox-audit-model decorators file.

Functions:
    audit_method: audit decorator.
"""
from functools import wraps

from eox_audit_model.models import AuditModel


def audit_method(action='Undefined action.'):
    """Decorator in order to audit methods.

    Arguments:
        action: String, action associated to the audit process.

    Return:
        decorator output.
    """
    def decorator(func):
        """Decorator function"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Set the parameter in the right format and call AuditModel.execute_action"""
            parameters = {
                'args': args,
                'kwargs': kwargs,
            }

            return AuditModel.execute_action(
                action=action,
                method=func,
                parameters=parameters,
            )

        return wrapper

    return decorator
