#!/bin/bash

POETRY_ENV_PATH=$(poetry env info -p)

source "$POETRY_ENV_PATH/bin/activate"