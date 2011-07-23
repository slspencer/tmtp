#! /bin/bash 
echo "Marker test 01"
../mkpattern --client=testdata.json --pattern=./P_marker_test_01.py --styles=test_styles.json marker-test_01.svg
echo "Marker test 02"
../mkpattern --client=testdata.json --pattern=./P_marker_test_02.py --styles=test_styles.json marker-test_02.svg
