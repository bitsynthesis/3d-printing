.PHONY: all, clean, requirements, scad, venv

SRCS=$(wildcard models/*.py)
STLS=$(patsubst models/%.py,build/%.stl,$(SRCS))
SCADS=$(patsubst models/%.py,build/%.scad,$(SRCS))
VENV=~/.venv/3d-printing

all: $(STLS)

scad: $(SCADS)

build/%.stl: build/%.scad
	openscad -o $@ $<

build/%.scad: $(VENV) build
	PYTHONPATH=. python $(patsubst build/%.scad,models/%.py,$@)

$(VENV):
	python3 -m venv $@

build:
	mkdir build

requirements: $(VENV)
	. $</bin/activate && pip install -r requirements.txt

clean: build
	rm build/* || true
