# Netcapacity

Esse script calcula o número máximo teórico de veículos que cabem em
uma rede, somando os comprimentos de todas as lanes e dividindo o
total pelo comprimento de um veículo.

Uso:

    netcapacity.py [options] --net-file FILE

Options:

    --help, -h              show this help message and exit -n FILE
    --net-file=FILE         A SUMO network whose capacity will be found.  -l N,
    --vehicle-length=N      The average length of vehicles [default: 5.0]

# summary2csv

Este script converte o summary-output do SUMO de .xml para .csv,
facilitando seu uso em programas de plotagem/planilhas eletrônicas.

Uso:

    summary2csv.py [options]

Options:

    --help, -h:                          show this help message and exit -x XMLFILE,
    --xml-file=XMLFILE                   the xml file to be converted (mandatory)
    --output-file=OUTFILE, -o OUTFILE    the output file (mandatory)
    --separator=SEPARATOR, -s SEPARATOR  the separator for the output file (default=whitespace)
    --total=TOTAL, -t TOTAL              the total number of vehicles in the simulation [use if you need to normalize waiting/total]

# IDtoNames

Esse script troca o ID das edges de uma rede que tenha sido
importada do OSM com a opção **--output.street-names** para os nomes
atribuídos.

Exemplo de uso:

    python IDtoNames -s ArquivoDeRede -o NovoArquivoDeRede

# countlinkusers

Dado um arquivo gerado com --vehroute-output, o script
countlinkusers.py escreve um arquivo com o número de veículos que usou
cada edge da rede viária em uma dada janela de tempo para cada
iteração de um dado experimento (especialmente os de tarifação
viária).

Requer a sumolib no PATH do python. A chamada do countlinkusers.py é a
seguinte:

    $ python countlinkusers.py [parametros]

Onde os parametros podem ser:

* -b BEGIN, --begin=BEGIN: (default=0) início da janela de tempo e
* -END, --end=END: (default=último timestep) fim da janela de tempo i
* -ITERATIONS, --iterations=ITERATIONS: número de iterações a serem
* -analizadas -first-iter=FIRST_ITER: número da primeira iteração a
* -ser analisada (é diferente em arquivos gerados pelo duaiterate (0)
* -ou pelos experimentos de tarifação viária (1)).  r
* -ROUTEINFO_PREFIX, --routeinfo-prefix=ROUTEINFO_PREFIX: prefixo dos
* -arquivos com as informações das rotas dos motoristas n NETFILE,
* ---netfile=NETFILE: arquivo da rede viária o OUTPUT,
* ---output=OUTPUT: arquivo de saída z ZERO_FILL,
* ---zero-fill=ZERO_FILL: preenche o nome dos arquivos a serem
* -analisados com zeros à esquerda até atingir o número de dígidos
* -especificados (e.q.: prefix_001.xml para -z 3). Especialmente útil
* -para analisar arquivos gerados pelo duaiterate.
