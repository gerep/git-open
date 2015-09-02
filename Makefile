DESTDIR  = /usr/local/bin

PROGRAM  = git-open

install: $(PROGRAM)
	cp $(PROGRAM) $(DESTDIR)
	chmod +x $(DESTDIR)/$(PROGRAM)

uninstall | clean:
	rm -f $(DESTDIR)/$(PROGRAM)