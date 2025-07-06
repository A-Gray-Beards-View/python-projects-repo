# Onion Architecture with Python and Dependency Injector

This document summarizes the key points and code structure for implementing **Onion Architecture** in Python using the `dependency-injector` library.

---

## 🧅 Onion Architecture Layers in Python

1. **Domain Layer (Core)**  
   - Contains business logic and entities  
   - Independent of frameworks or external dependencies

2. **Application Layer**  
   - Interfaces for use cases and services  
   - Defines abstract interfaces like repositories

3. **Infrastructure Layer**  
   - Implements application layer interfaces  
   - Deals with DB, APIs, etc.

4. **Presentation Layer**  
   - Entry points like Flask/FastAPI or CLI  
   - Calls application services

---

## 🔌 Dependency Injector Integration

Install the library:
```bash
pip install dependency-injector
```

### 1. Domain Layer

**entities.py**
```python
class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
```

**services.py**
```python
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, user: User):
        self.user_repository.save(user)
```

---

### 2. Application Layer

**interfaces.py**
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def find_by_id(self, user_id):
        pass
```

---

### 3. Infrastructure Layer

**repositories.py**
```python
from application.interfaces import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def save(self, user):
        print(f"Saving user {user.name} to the database.")

    def find_by_id(self, user_id):
        return None
```

---

### 4. Dependency Injection Setup

**containers.py**
```python
from dependency_injector import containers, providers
from domain.services import UserService
from infrastructure.repositories import UserRepositoryImpl

class ApplicationContainer(containers.DeclarativeContainer):
    db_connection = providers.Singleton(lambda: "Your DB Connection")

    user_repository = providers.Singleton(
        UserRepositoryImpl,
        db_connection=db_connection
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )
```

---

### 5. Presentation Layer (Flask Example)

**api.py**
```python
from flask import Flask, request, jsonify
from containers import ApplicationContainer
from domain.entities import User

app = Flask(__name__)
container = ApplicationContainer()
user_service = container.user_service()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(user_id=data['id'], name=data['name'])
    user_service.create_user(user)
    return jsonify({"message": "User created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

---

## ✅ Benefits

- Decouples logic for maintainability and testing
- Swappable infrastructure with clear interfaces
- Centralized configuration with `Dependency Injector`
