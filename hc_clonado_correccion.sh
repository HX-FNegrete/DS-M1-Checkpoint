input=$1
while read -r line
do
  # Here comma is our delimiter value
  IFS="," read -a myarray <<< $line
  user=${myarray[1]}
  repo=${myarray[0]}
  user=`echo $user | sed 's/ *$//g'`
  echo $user >> salida.txt
  mkdir -p $user
  git clone https://github.com/$user/$repo $user
done < "$input"
#pip install wrapt_timeout_decorator
#python hc_correccion.py