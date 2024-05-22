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

NJobs=1 ; export NJobs
Jobs(){
	if [[  $(jobs | wc -l ) -ge $NJobs ]] ; then
		wait -n
	fi
}

function main(){
    x=$1
    rX=$(mktemp --suffix=".txt")
    # Fetch data using ffuf and append to temporary file
    ffuf -w db/API.txt -u "$x/FUZZ" -mc 200 -fs 0 -sf -se | awk '{print $1}' | sed 's/[^[:print:]]//g' | sed 's/\[2K//g' > "$rX"
    for i in $(cat "$rX"); do
        echo "$x/$i"
    done | sort -u | python3 utils/Uniqe.py
}

for d in $(cat $fX); do
    main $d
done
wait
exit