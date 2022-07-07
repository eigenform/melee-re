
TARGET	:= libssbmpack

all: $(TARGET).so

$(TARGET).o: src/ssbm_pack.c
	gcc -c -fPIC $< -o $@

$(TARGET).so: $(TARGET).o
	gcc -shared $< -o $@

clean:
	rm -vf $(TARGET).{o,so}

.PHONY: clean all
