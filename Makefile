PY_MODULE := remoteme_back
TESTS := tests
MAX_LINE_LENGTH := 120

lint:
		perflint ${PY_MODULE}


format:
		python -m black -l ${MAX_LINE_LENGTH} ${PY_MODULE} ${TESTS}
		python -m isort ${PY_MODULE} ${TESTS}
		python -m flake8 --max-line-length=${MAX_LINE_LENGTH} --ignore E203,E501,E731,W503 ${PY_MODULE} ${TESTS}
		python -m mypy ${PY_MODULE} --ignore-missing-imports


test:
		python -m pytest ${TESTS} --asyncio-mode=auto -n auto