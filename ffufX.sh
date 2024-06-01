#!/usr/bin/bash
exec 2>/dev/null

D="$1"
fX=$(mktemp --suffix=".txt")

if [ -t 0 ]; then
    :
else
  cat > $fX
fi

if [ ! -s "$fX" ]; then
    cat $D > $fX
else
    :
fi

NJobs=2 ; export NJobs
Jobs(){
	if [[  $(jobs | wc -l ) -ge $NJobs ]] ; then
		wait -n
	fi
}

function main(){
    x=$1
    bsedX="sed -e 's/^http:\/\///g' -e 's/^https:\/\///g' -e 's/^www\.//g'"
    Brand=$(echo $x | eval $bsedX)
    rX=$(mktemp --suffix=".txt")

    #Fetch data using ffuf and append to temporary file!
    ffuf -w db/Allmiro.txt -u "$x/FUZZ" -mc 200 -fs 0 -sa -s  >> "$rX"
    ffuf -w db/raft.txt -u "$x/FUZZ" -mc 200 -fs 0 -sa -s >> "$rX"

    #ffuf -w db/raft.txt -u "$x/_FUZZ" -mc 200 -fs 0 -sa -s >> "$rX"
    #ffuf -w db/raft.txt -u "$x/~FUZZ" -mc 200 -fs 0 -sa -s >> "$rX"

    for i in $(cat "$rX" | sort -u); do
        echo "$x/$i"
    done | sort -u | python3 utils/Uniqe.py
    sed -i "/$Brand/d" $D
}

for d in $(cat $fX); do
    main $d &
Jobs
done
wait
exit
