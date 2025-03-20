from app.crud.employee import (
    get_employee,
    get_employee_by_email,
    get_employees,
    create_employee,
    update_employee,
    delete_employee
)

from app.crud.metric import (
    get_metric,
    create_metric,
    update_metric,
    delete_metric,
    get_employee_metrics
)

from app.crud.report import (
    get_report,
    create_report,
    update_report,
    delete_report,
    get_employee_reports
)

# Экспортируем функции напрямую
__all__ = [
    # Employee operations
    "get_employee",
    "get_employee_by_email",
    "get_employees",
    "create_employee",
    "update_employee",
    "delete_employee",
    
    # Metric operations
    "get_metric",
    "create_metric",
    "update_metric",
    "delete_metric",
    "get_employee_metrics",
    
    # Report operations
    "get_report",
    "create_report",
    "update_report",
    "delete_report",
    "get_employee_reports"
] 