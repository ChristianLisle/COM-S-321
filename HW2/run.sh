# Pass the first argument parameter (file) $1 to the dissassembler.
# Additionally, type -p to print dissassembled program to console.
if [ $# -eq 0 ]
    then
     echo "Usage: sh run.sh <LEGv8 Machine file> [-p]"
     exit 1
fi
python3 dissassembler/dissassembler.py $1 $2