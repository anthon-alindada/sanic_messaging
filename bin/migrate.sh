#!/bin/bash

# Migrate user module
alembic -c ./alembic.ini -n development upgrade user@head
alembic -c ./alembic.ini -n test upgrade user@head


# Migrate messaging module
alembic -c ./alembic.ini -n development upgrade messaging@head
alembic -c ./alembic.ini -n test upgrade messaging@head
