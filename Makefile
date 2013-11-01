TARGET=KeyMacro.alfredworkflow

all:
	mkdir -p bin
	zip -j9 bin/$(TARGET) src/*.{plist,png,py}

clean:
	rm -rf bin

install: all
	open bin/$(TARGET)

