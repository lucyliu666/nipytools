#should be run in the subject's "mri" directory, where the labels are
theselabels=(posterior*)
for i in ${theselabels[@]}; do
dirr=$(dirname $i)
fname=$(basename $i)
fname=${fname%%.*}
mri_convert "$i" "$fname".nii.gz
mri_label2vol --seg "$fname".nii.gz --temp "$dirr"/nu.mgz --regheader --o "$fname".nii.gz
done
 

