DESTDIR  = /usr/local/bin

PROGRAM  = git-open

.PHONY: install uninstall clean test

install: $(PROGRAM)
	cp $(PROGRAM) $(DESTDIR)
	chmod +x $(DESTDIR)/$(PROGRAM)

uninstall clean:
	rm -f $(DESTDIR)/$(PROGRAM)

test:
	python3 -B -m unittest discover -s tests -v
