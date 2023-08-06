import os
import sys
import dat_file_reader

def main():
    verbose = "-v" in sys.argv
    file_path = sys.argv[1]
    results = dat_file_reader.read_full_dat_file(file_path)

    print("Found " + str(len(results)) + " segments")

    # TODO: modularizar as leituras
    # TODO: aceitar injeção de função - será chamada depois de ler uma tag
    # TODO: Salvar horário de início e fim de processamento do arquivo inteiro para analytics
    # ... inicialmente podemos só jogar em um log mesmo
    # ... futuramente podemos usar o google cloud para salvar os registros

if __name__ == "__main__":
    main()

