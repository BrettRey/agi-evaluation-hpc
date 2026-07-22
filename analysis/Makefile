PYTHON ?= python3
ROOT := ..

.PHONY: test smoke standard refresh-lock clean-cache

test:
	cd $(ROOT) && $(PYTHON) -m unittest discover -s analysis/tests -v

smoke: test
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_instability --profile smoke
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_pss --profile smoke
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_bootstrap_coverage --profile smoke
	cd $(ROOT) && $(PYTHON) -m analysis.reanalyse_zhang --profile smoke
	cd $(ROOT) && $(PYTHON) -m analysis.summarize_evidence

standard: test
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_instability --profile standard
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_pss --profile standard
	cd $(ROOT) && $(PYTHON) -m analysis.simulate_bootstrap_coverage --profile standard
	cd $(ROOT) && $(PYTHON) -m analysis.reanalyse_zhang --profile standard
	cd $(ROOT) && $(PYTHON) -m analysis.summarize_evidence

refresh-lock:
	cd $(ROOT) && $(PYTHON) -m analysis.pin_sources

clean-cache:
	rm -rf cache
