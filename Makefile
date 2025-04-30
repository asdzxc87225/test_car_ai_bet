# Makefile for my_ai_bet_tool
# 執行方式：make <目標>，例如 make test

# Python 解譯器與搜尋路徑
PYTHON := python
PYTHONPATH := .

# 主要資料檔案
LOG_FILE := data/game_log.csv

# 預設目標：列出可用指令
help:
	@echo ""
	@echo "🎮 My AI Bet Tool - 指令總覽"
	@echo "---------------------------------------------"
	@echo " make test       ▶ 執行單元測試 (pytest)"
	@echo " make validate   ▶ 驗證資料切分與特徵計算"
	@echo " make run        ▶ 啟動 UI 介面"
	@echo " make clean      ▶ 清理訓練中間檔案"
	@echo " make merge      ▶ 合併資料檔案"
	@echo " make train      ▶ 訓練檔案"
	@echo " make eval       ▶ 測試權重"
	@echo ""

# 📦 單元測試（tests/）
test:
	PYTHONPATH=$(PYTHONPATH) pytest -q tests/

# 🧪 資料驗證（scripts/validate_data.py）
validate:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/validate_data.py

# 🖼️ 啟動 UI 主程式
run:
	$(PYTHON) main.py

# 🧼 清理訓練後產生的檔案
clean:
	rm -f data/train.csv data/test.csv
#	rm -f data/models/*.pkl

# 🆕 建立訓練資料（測試用）
build-data:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c 'from data.dataset_split import split; split("$(LOG_FILE)")'
#合併資合併資料檔案:
merge:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  scripts/merge_split_data.py
train:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  scripts/q_train_legacy.py
eval:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./scripts/evaluate_q_table.py

gra:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./scripts/visualize_q_table.py
mark:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./scripts/analyze_transition_matrix.py
test2:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./scripts/test_BehaviorAnalyzer.py
test_data_facade:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./tests/test_data_facade.py
test_data_classifier:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON)  ./tests/test_data_classifier.py

