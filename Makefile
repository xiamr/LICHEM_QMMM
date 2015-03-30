###################################################
#                                                 #
# FLUKE: Fields Layered Under Kohn-Sham Electrons #
#                                                 #
###################################################

CXX=g++
CXXFLAGS=-static -fopenmp -g -O3
LDFLAGS=-I/usr/include/eigen3/
TEX=pdflatex
BIB=bibtex

### Compile rules for users and devs

install:	title binary manual compdone

Dev:	title binary devbin manual stats compdone

### Rules for building various parts of the code

binary:	
	@echo ""; \
	echo "Compiling the FLUKE binary..."
	cd src/; \
	$(CXX) $(CXXFLAGS) FLUKE.cpp -o FLUKE $(LDFLAGS)
	@mv src/FLUKE .

devbin:	
	@echo ""; \
	echo "Compiling the FLUKE development binary..."
	cd src/; \
	$(CXX) $(CXXFLAGS) -DDEVCOMP FLUKE.cpp -o FLUKE $(LDFLAGS)
	@mv src/FLUKE .

manual:	
	@echo ""; \
	echo "Compiling the documentation..."; \
	cd src/; \
	$(TEX) manual > doclog.txt; \
	$(BIB) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(BIB) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	$(TEX) manual > doclog.txt; \
	mv manual.pdf ../doc/FLUKE_manual.pdf; \
	rm -f manual.aux manual.bbl manual.blg; \
	rm -f manual.log manual.out manual.toc; \
	rm -f doclog.txt

title:	
	@echo ""; \
	echo "###################################################"; \
	echo "#                                                 #"; \
	echo "# FLUKE: Fields Layered Under Kohn-Sham Electrons #"; \
	echo "#                                                 #"; \
	echo "###################################################"

stats:	
	@echo ""; \
	echo "Number of FLUKE source code files:"; \
	ls -al src/* | wc -l; \
	echo "Total lenght of FLUKE (lines):"; \
	cat src/* | wc -l

compdone:	
	@echo ""; \
	echo "Done."; \
	echo ""