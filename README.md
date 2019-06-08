# Sanic Boilerplate

Sanic boiler plate application

### Tech
- Sanic
- ReactJs
- Docker
- Alembic
- Postgres
- Gino (ORM)
- Pytest

### Feature details
- User model (Custom)
- Signup / Registration
- Login
- JWT Authentication

### Application structure
```
├── app                     # Sanic application
│   ├── domain              # Domain applications (Put other applications here)
│   │   ├── user
│   │   ├── messaging
│   ├── http                # Http views / template
│   ├── libs                # Core libraries
│   ├── media               # Media files
│   ├── static              # Static files
├── config                  # Config files
│   ├── base.py
│   ├── development.py
│   ├── production.py
│   ├── test.py
├── bin                     # Scripts
├── run.py                  # Run application
└── ...
```


### Migrate instructions
alembic revision -m "create user table" --version-path=app/domain/user/migrations --head=base --branch-label=user
alembic revision -m "create verification code table" --head=user@head
alembic revision -m "create sample table" --head=user@head
alembic -n development upgrade user@head
