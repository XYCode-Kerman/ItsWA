echo "=== 开始使用 Auto PEP8 进行自动格式化 ==="
poetry run autopep8 -i **/*.py

echo "=== Auto PEP8 格式化结束，使用 Auto Flake 进行格式化 ==="
poetry run autoflake -i --remove-unused-variables --remove-duplicate-keys --remove-all-unused-imports --ignore-init-module-imports --remove-rhs-for-unused-variables **/*.py

echo "=== Auto Flake 格式化结束，使用 Isort 进行排序 ==="
poetry run isort .