.PHONY: all, clean, requirements, venv

SRCS=$(wildcard models/*.py)
TARGETS=$(patsubst models/%.py,build/%.scad,$(SRCS))
VENV=~/.venv/3d-printing

all: $(TARGETS)

build/%.scad: $(VENV) build
	. $</bin/activate && PYTHONPATH=. python $(patsubst build/%.scad,models/%.py,$@)

$(VENV):
	python3 -m venv $@

build:
	mkdir build

requirements: $(VENV)
	. $</bin/activate && pip install -r requirements.txt

clean: build
	rm build/* || true
