###################################################
#                                                 #
#   LICHEM: Layered Interacting CHEmical Models   #
#                                                 #
#               Symbiotic Chemistry               #
#                                                 #
###################################################

### Compiler settings

CXX=g++
CXXFLAGS=-static -fopenmp -O3
DEVFLAGS=-g -Wall
LDFLAGS=-I./src/ -I/usr/include/eigen3/
TEX=pdflatex
BIB=bibtex

### Compile rules for users and devs

install:	title binary manual compdone

Dev:	title devbin manual stats compdone

clean:	title delbin compdone

### Rules for building various parts of the code

binary:	
	@echo ""; \
	echo "### Compiling the LICHEM binary ###"
	$(CXX) $(CXXFLAGS) ./src/LICHEM.cpp -o LICHEM $(LDFLAGS)

devbin:	
	@echo ""; \
	echo "### Compiling the LICHEM development binary ###"
	$(CXX) $(CXXFLAGS) $(DEVFLAGS) ./src/LICHEM.cpp -o LICHEM $(LDFLAGS)

manual:	
	@echo ""; \
	echo "### Compiling the documentation ###"; \
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
	mv manual.pdf ../doc/LICHEM_manual.pdf; \
	rm -f manual.aux manual.bbl manual.blg; \
	rm -f manual.log manual.out manual.toc; \
	rm -f doclog.txt; \
        echo " [Complete]"

title:	
	@echo ""; \
	echo "###################################################"; \
	echo "#                                                 #"; \
	echo "#   LICHEM: Layered Interacting CHEmical Models   #"; \
	echo "#                                                 #"; \
	echo "#               Symbiotic Chemistry               #"; \
	echo "#                                                 #"; \
	echo "###################################################"

stats:	
	@echo ""; \
        echo "### Source code statistics ###"; \
	echo "Number of LICHEM source code files:"; \
	ls -al src/* | wc -l; \
	echo "Total length of LICHEM (lines):"; \
	cat src/* | wc -l

compdone:	
	@echo ""; \
	echo "Done."; \
	echo ""

delbin:	
	@echo ""; \
	echo '     ___'; \
	echo '    |_  |'; \
	echo '      \ \'; \
	echo '      |\ \'; \
	echo '      | \ \'; \
	echo '      \  \ \'; \
	echo '       \  \ \'; \
	echo '        \  \ \       <wrrr vroooom wrrr> '; \
	echo '         \__\ \________'; \
	echo '             |_________\'; \
	echo '             |__________|  ..,  ,.,. .,.,, ,..'; \
	echo ""; \
        echo ""; \
	echo "Removing binary and manual..."; \
	rm -f LICHEM ./doc/LICHEM_manual.pdf
