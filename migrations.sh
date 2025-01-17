#!/bin/bash

if alembic revision --autogenerate; then
    echo "成功生成迁移文件"
    if alembic upgrade head; then
        echo "成功执行迁移"
    else
        echo "执行迁移失败"
        exit 1
    fi
else
    echo "生成迁移文件失败"
    exit 1
fi
