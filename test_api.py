import requests
from datetime import datetime, timedelta
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"

def wait_for_server(timeout=30):
    print("Ожидание запуска сервера...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{BASE_URL}/employees/")
            if response.status_code in [200, 404]:
                print("Сервер запущен и готов к работе")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    print("Не удалось подключиться к серверу")
    return False

def test_employee_operations():
    print("Начинаем тестирование API...")
    
    try:
        # Создание сотрудника
        employee_data = {
            "full_name": "Иван Петров",
            "email": "ivan@example.com",
            "position": "Middle",
            "department": "IT",
            "hire_date": "2024-03-19T10:00:00",
            "salary": 150000.0
        }
        
        response = requests.post(f"{BASE_URL}/employees/", json=employee_data)
        print(f"Создание сотрудника: {response.status_code}")
        if response.status_code == 400 and "уже существует" in response.json().get("detail", ""):
            print("Сотрудник с таким email уже существует, продолжаем тестирование...")
            # Получаем список сотрудников чтобы найти ID существующего сотрудника
            response = requests.get(f"{BASE_URL}/employees/")
            employees = response.json()
            for emp in employees:
                if emp["email"] == employee_data["email"]:
                    employee_id = emp["id"]
                    break
        else:
            print(response.json())
            employee_id = response.json()["id"]
        
        # Получение списка сотрудников
        response = requests.get(f"{BASE_URL}/employees/")
        print(f"\nПолучение списка сотрудников: {response.status_code}")
        print(response.json())
        
        # Получение информации о сотруднике
        response = requests.get(f"{BASE_URL}/employees/{employee_id}")
        print(f"\nПолучение информации о сотруднике: {response.status_code}")
        print(response.json())
        
        # Создание метрики для сотрудника
        metric_data = {
            "employee_id": employee_id,
            "metric_type": "productivity",
            "value": 85.5,
            "date": datetime.now().isoformat(),
            "description": "Высокая продуктивность"
        }
        
        response = requests.post(f"{BASE_URL}/metrics/", json=metric_data)
        print(f"\nСоздание метрики: {response.status_code}")
        print(response.json())
        
        # Получение метрик сотрудника
        response = requests.get(f"{BASE_URL}/metrics/employee/{employee_id}")
        print(f"\nПолучение метрик сотрудника: {response.status_code}")
        print(response.json())
        
        # Создание отчета для сотрудника
        report_data = {
            "employee_id": employee_id,
            "report_type": "weekly",
            "start_date": (datetime.now() - timedelta(days=7)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "data": {
                "total_tasks": 15,
                "completed_tasks": 14,
                "productivity_score": 85.5,
                "quality_score": 90.0
            }
        }
        
        response = requests.post(f"{BASE_URL}/reports/", json=report_data)
        print(f"\nСоздание отчета: {response.status_code}")
        print(response.json())
        
        # Получение отчетов сотрудника
        response = requests.get(f"{BASE_URL}/reports/employee/{employee_id}")
        print(f"\nПолучение отчетов сотрудника: {response.status_code}")
        print(response.json())
        
        # Обновление информации о сотруднике
        update_data = {
            "position": "Senior",
            "salary": 180000.0
        }
        
        response = requests.put(f"{BASE_URL}/employees/{employee_id}", json=update_data)
        print(f"\nОбновление информации о сотруднике: {response.status_code}")
        print(response.json())
        
        # Удаление сотрудника
        response = requests.delete(f"{BASE_URL}/employees/{employee_id}")
        print(f"\nУдаление сотрудника: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not wait_for_server():
        sys.exit(1)
    test_employee_operations() 