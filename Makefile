.PHONY: all, clean, requirements, venv

all: build/din_rail.scad \
	build/rpi_3b_din_mount.scad \
	build/vhs_clutch.scad \
	build/vhs_doorstop.scad

build/din_rail.scad: ~/.venv/3d-printing build
	. $</bin/activate && PYTHONPATH=. python ./models/din_rail.py

build/rpi_3b_din_mount.scad: ~/.venv/3d-printing build
	. $</bin/activate && PYTHONPATH=. python ./models/rpi_3b_din_mount.py

build/vhs_clutch.scad: ~/.venv/3d-printing build
	. $</bin/activate && PYTHONPATH=. python ./models/vhs_clutch.py

build/vhs_doorstop.scad: ~/.venv/3d-printing build
	. $</bin/activate && PYTHONPATH=. python ./models/vhs_doorstop.py

~/.venv/3d-printing:
	python3 -m venv $@

build:
	mkdir build

requirements: ~/.venv/3d-printing
	. $</bin/activate && pip install -r requirements.txt

clean: build
	rm build/* || true
