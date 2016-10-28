#!/bin/bash
export APP_SETTINGS=config.ProductionConfig
export CLEARDB_DATABASE_URL="mysql+mysqldb://root:wangpl9203@localhost/wangpenglin"
python run.py
