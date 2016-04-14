import pandas as pd
import re,os
from subprocess import call
#
# Sample data file to use for accessing header info
#
froot = '/home/mcgouldrick/maven/data/sci/kp/insitu/2015/10/'
fname = froot + 'mvn_kp_insitu_20151028_v02_r11.tab'
#
# Count the number of lines in the header
#
print "Reading sample file for header information..."
nheader = 0
for line in open(fname):
    if line.startswith('#'):
        nheader = nheader+1
#
# Read the header and create a DataFrame of the column header information
#
fin=open(fname)
#
#  Cycle through lines of header
#
for iline in range(nheader):
    line = fin.readline()
    #
    # Get number of columns of data stated in header
    #
    if re.search('Number of parameter columns',line):
        ncol = int(re.split("\s{3}",line)[1])
    #
    # Get the labels of the columns in the Column description section
    #
    elif re.search('PARAMETER',line):
        ParamListStartLine = iline
        ColStart = []
        ColEnd = []
        test = re.split('^#\s|\s{2,}',line)
        #
        # Get the column numbers for start and end of fields
        #
        for i in test[1:-1]:
            #
            # Yes, this is confusing; but we are starting from the 2nd
            #   entry, so we assume the start column of 1, and the start
            #   of the 2nd entry indicates the end of that column.
            #
            start = re.search(i,line).start()
            ColStart.append(start)
            if test.index(i) > 1:
                ColEnd.append(start)
            if test.index(i) == len(test[1:-1]):
                ColEnd.append(len(line))
#
#  Use the column field information to build colspecs argument for read_fwf
#
ColSpecs = []
for i,j in zip(ColStart,ColEnd):
    ColSpecs.append([i,j])
fin.close()
#
#  Read the table as a fixed width field table
#
test = pd.read_fwf(fname,
                   skiprows=range(ParamListStartLine)+[ParamListStartLine+1],
                   colspecs=ColSpecs,header=0,nrows=ncol)
#
#  Define filenames for creating LaTeX table from fwf
#
tempname = '/home/mcgouldrick/temp.tex'
foutname = '/home/mcgouldrick/kp_data_insitu_info_table.tex'
fout = open(tempname,'w')
TableCols = ['INSTRUMENT','PARAMETER','UNITS','FORMAT','NOTES']
HeaderLine = ' & '.join(TableCols) + '\\\\'
#
# Write LaTeX preamble
#
print "Writing LaTeX table..."
fout.write('\\documentclass[10pt]{article}\n')
fout.write('\\usepackage{booktabs}\n')
fout.write('\\usepackage{longtable}\n')
fout.write('\\usepackage{amssymb, amsmath, graphicx}\n')
fout.write('\\usepackage{rotating}\n')
fout.write('\\usepackage{geometry}\n')
fout.write('\\geometry{letterpaper, landscape, margin=0.5in}\n')
fout.write('\n')
fout.write('\\begin{document}')
fout.write('\n')
#
# Write the replacement lines for converting to longtable
#
fout.write('\\begin{center}\n')
fout.write('\\begin{longtable}{|p{1in}|p{2.5in}|p{1in}|p{1in}|p{4in}|}\n')
fout.write('\\caption[MAVEN In-Situ Key Parameter Data Table]{MAVEN In-Situ Key Parameter Data Table}\\\\\n')
fout.write('\n')
fout.write('\\hline\n%s%%FirstHead\n\\hline\n\\endfirsthead\n\n' % HeaderLine)
fout.write('\\hline\n%s%%LaterHead\n\\hline\n\\endhead\n\n' % HeaderLine)
fout.write('\\hline\n \\multicolumn{%1d}{c}{\\textit{(Continued on next page)}}\\\\\n' % len(TableCols))
fout.write('\\endfoot\n\n')
fout.write('\\hline\\hline\n\\endlastfoot\n\n')
fout.write('%% End add lines to top\n')
fout.write('%% Also Remove \\end{tabular} and \\bottomrule from end of document\n\n')
#
# Use unlimited column width for producing table.  LaTeX will word-wrap for us
#
pd.set_option('max_colwidth', -1)
#
# Write table
#
fout.write( pd.DataFrame(test).to_latex( columns=TableCols,index=False,
                                         na_rep='',longtable=False ) )
#
# Re-set max_colwidth to default value
#
pd.reset_option('max_colwidth')
#
# Add \end blocks for longtable and center
#
fout.write('\\end{longtable}\n\\end{center}\n')
fout.write('\end{document}')
fout.flush()
fout.close()
#
# Now, go back, open the written file and re-write corrections
# First, footnote information
#
print "Editing LaTeX table (adding footnotes, etc.)..."
Note1 = '\\footnotemark'
DoneNote1 = False
Text1 = '\\footnotetext{Instrument name is used to define substructures/dictionaries}\n'
Note2 = '\\footnote{EUV is here included as a separate instrument for naming purposes in the Tookit}'
DoneNote2 = False
Note3 = '\\footnote{Spacecraft substruct data contains ephemeris and geometry data within KP data files}'
DoneNote3 = False
Note4 = '\\footnote{APP orientation information is placed into its own substruct for visualization purposes}'
DoneNote4 = False
Note5 = '\\footnote{While these are spacecraft data, they are placed at base level struct/dict}'
DoneNote5 = False
#
#  Now, cycle through the lines of the file
#
fout = open(foutname,'w')
for line in open(tempname):
    # Remove the old tabular environment syntax
    if ( line.startswith('\\begin{tabular}') or 
         line.startswith('\\toprule') or 
         line.startswith('\\bottomrule') or
         line.startswith('\\midrule') or
         line.startswith('\\end{tabular}') ):
        fout.write('')
    elif 'INSTRUMENT' in line:
        # Add the Instrument name footnote (special case b/c in header)
        if 'FirstHead' in line and not DoneNote1:
            fout.write(line.replace('INSTRUMENT','INSTRUMENT'+Note1))
            DoneNote1 = True
        elif 'LaterHead' in line:
            fout.write(line)
        else:
            pass
    elif 'UTC/SCET' in line:
        # Also needed to write the instrument name footnote
        fout.write(Text1)
        fout.write(line)
    elif 'LPW-EUV' in line:
        # Change the LPW-EUV to EUV and add note
        if DoneNote2:
            fout.write(line.replace('LPW-EUV','EUV'))
        else:
            fout.write(line.replace('LPW-EUV','EUV'+Note2))
            DoneNote2 = True
    elif 'SPICE' in line:
        if 'APP' in line:
            # Change Articulating Platform instrument name from SPICE to APP
            if not DoneNote4:
                fout.write(line.replace('SPICE','APP'+Note4))
                DoneNote4 = True
            else:
                fout.write(line.replace('SPICE','APP'))
        elif 'Orbit Number' in line:
            # Add notes for Orbit number and IO_flag
            line = line.replace('SPICE','---'+Note5)
            fout.write(line)
        elif 'Inbound' in line:
            fout.write(line.replace('SPICE','---'+Note5))
        else:
            # Replace ASCII arrow with LaTeX arrows in coord transform entries
            if '->' in line:
                line = line.replace('->','$\\rightarrow$')
            if not DoneNote3:
                # Change SPICE to SPACECRAFT in all other SPICE entries
                fout.write(line.replace('SPICE','SPACECRAFT'+Note3,1))
                DoneNote3 = True
            else:
                fout.write(line.replace('SPICE','SPACECRAFT'))
    else:
        # If nothing changed, write the old line
        fout.write(line)
fout.flush()
fout.close()
#
# Now, Run LaTeX from here
#
print "Generating LaTeX table..."
call(["latex",foutname],stdout=open(os.devnull,'w'))
print "Generating PDF-capable postscipt file..."
call(["dvips", "-Ppdf", "-o", 
      foutname.replace('tex','ps'), foutname.replace('tex','dvi')],
      stdout=open(os.devnull,'w'),stderr=open(os.devnull,'w'))
print "Generating PDF file of table..."
call(["ps2pdf",foutname.replace('tex','ps')],stdout=open(os.devnull,'w'))
print "Cleaning up...."
call(["rm",tempname])
for i in ['aux','dvi','log','ps','tex']:
    call(["rm",foutname.replace('tex',i)])
