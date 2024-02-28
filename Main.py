import logging
from Modules.Funcs import menu,process_options



logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    
    logger.info("Debut du programme principal")
    print("Debut du programme principal")
    print("\n\n----------Sup-Trading----------\n")
    
    while(1):
        
        option = menu()
        if option == 4:
            logger.info("Quitter le programme")
            break
        
        if not process_options(option):
            break
    
    print("\nFin du programme principal\n")
    logger.info("Fin du programme principal\n")



