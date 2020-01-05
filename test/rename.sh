name_t=1
cd RealRoad/
for image in `ls *`
do
	if [ -f $image ];
	then
		mv $image image$name_t.jpg
		name_t=$(( $name_t + 1 ))
	fi
done
