#!/bin/bash
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011, 2012 Susan Spencer, Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. Attribution must be given in
# all derived works.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

echo On

TMTP_BASE=$PWD
PATTERN_BASE=$TMTP_BASE/patterns
CUSTOMER_BASE=$TMTP_BASE/customer
PYTHONPATH=$PYTHONPATH:$TMTP_BASE:$PATTERN_BASE:$CUSTOMER_BASE
export PYTHONPATH
export TMTP_BASE
export PATTERN_BASE
export CUSTOMER_BASE

function FileName () {
    D=$(date +"%F"-%H%M)
    FILE=${PATTERN##*/}
    FILE=${FILE%%.*}
    FILE="$CUSTOMER_DIR/$FILE-$D"
    echo $FILE

    return;
}

function Tmtp () {

    $TMTP_BASE/mkpattern --client=$CUSTOMER_NAME --pattern=$PATTERN --styles=$TMTP_BASE/tmtp_styles.json $FILE.svg
    # Uncomment the following line for debugging, comment out the above line.
    # $TMTP_BASE/mkpattern --verbose  --client=$CUSTOMER_NAME --pattern=$PATTERN --styles=$TMTP_BASE/tmtp_styles.json --debug=prints $FILE.svg

    # At this time the TMTP program does not generate seam allowances and it does not display the output file.
    # Set seam allowance width: set 'outstep' in Inkscape Preferences to ????px for 5/8" or ????px for 1cm, whichever you prefer. All seam allowances will have this width.


    # Create cuttinglines through Inkscape outset command line option
    # If any of your patterns have more than 7 (A thru G) pattern pieces in them, add more cuttinglines in command below (e.g. --select=H.cuttingline --select I.cuttingline).  When outset function is added into TMTP code then this kluge can be removed
    # While in Inkscape you can hide the reference layer, save the file as PDF, then print PDF file to a wide-format plotter.
    inkscape --file=$FILE.svg --verb=ZoomPage --select=A.cuttingline --select=B.cuttingline --select=C.cuttingline  --select=D.cuttingline --select=E.cuttingline --select=F.cuttingline --select=G.cuttingline --verb=SelectionOffset --verb=EditDeselect --verb=FileSave

    #Uncomment the following line to automatically remove the reference layer (all the items that aren't normally in a printed pattern):
    #inkscape --file=$FILE.svg --verb=ZoomPage --select=reference --verb=SelectionDelete --verb=FileSave

    #Uncomment the following line to automatically save output file to a PDF file in the customer directory. Print the PDF file to a wide format plotter for best results.
    #inkscape --file=$FILE.svg --export-area-snap -A $FILE.pdf

    return;
    }

function CustomerMenu () {

    # Display menu and interact based on the user's input
    CUSTOMER_NAME="$(kdialog --title "Select A Customer Directory, Then Select Their Measurement File:" --getopenfilename $CUSTOMER_BASE '*.json')"
    echo $CUSTOMER_NAME

    CUSTOMER_DIR=${CUSTOMER_NAME%/*}
    echo $CUSTOMER_DIR
    # The output file will be saved into $CUSTOMER_DIR with date & time, etc.

    return;
    }

function PatternMenu () {

    # Select Pattern File
    PATTERN="$(kdialog --title "Select A Pattern:" --getopenfilename $PATTERN_BASE '*.py')"
    echo $PATTERN

    return;
    }

function MainMenu () {
    # Loop until user selects EXIT
    var1="$(kdialog --menu "Welcome to TMTP - Tau Meta Tau Physica!" 1 'Select a Pattern' 2 'Exit TMTP' )"
    case $var1 in
        1)
          GETPATTERN="1";;
        2)
          GETPATTERN="0";;
    esac

    return;
    }

# Main Program

GETPATTERN="1"

while true; do

    MainMenu
    if [ $GETPATTERN == '0' ]; then
        break
    else
        PatternMenu
        CustomerMenu
        FileName
        Tmtp
    fi

done
