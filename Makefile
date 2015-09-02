DESTDIR  = /usr/local/bin

PROGRAM  = git-open

install: $(PROGRAM)
	cp git-open $(DESTDIR)
	chmod +x $(DESTDIR)/git-open

clean:
	rm -f $(DESTDIR)/git-open