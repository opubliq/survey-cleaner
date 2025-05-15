.PHONY: tree

tree:
	@tree -L 3 > arborescence.txt
	@echo "Tree structure (3 levels) saved to arborescence.txt"

.PHONY: run

run:
	streamlit run app.py