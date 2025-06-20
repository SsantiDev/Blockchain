#Punto de Entrada del Programa
from blockchain import Blockchain
import time

def AttackSimulation(blockchain):
    print("==== Simulating a blockchain attack ====")
    print("Modifying the data of the Second block...")
        
        # verify that we have enough blocks for the attack
        # and modify the data of the second block
    if len(blockchain.chain) >= 3:
        original_data = blockchain.chain[2].data
        blockchain.chain[2].data = "Transaction 2: Vale pays Zero 555 XRP"
        print(f"Original data: {original_data}")
        print(f"Modified data: {blockchain.chain[2].data}")
            
        is_valid_after_attack = blockchain.is_valid_chain()
        print(f"¿The blockchain is valid after the attack? {is_valid_after_attack}")
        
        print("==== Blockchain after the attack ====")
        blockchain.print_chain()        
        
        print("\n==== Analysis of the Attack ====")
        attacked_block = blockchain.chain[2]
        print(f"Block {attacked_block.index} current hash: {attacked_block.hash}")
        print(f"Block {attacked_block.index} recalculated hash: {attacked_block.calculate_hash()}")
        print("the attack was detected because the stored has does not match the recalculated hash.")
    else:
        print("Not enough blocks to simulate the attack. At least 3 blocks are required.")
        
    
def main():
    """
    Main function to run the blockchain application.
    Initializes the blockchain, adds blocks, and displays the chain.
    """
    try:
        # Initialize the blockchain with a difficulty level
        print("==== Initializing the blockchain ====")
        blockchain = Blockchain(difficulty=5)
        print(f"Blockchain initialized with {len(blockchain.chain)} block(s).")
        print(f"Difficulty level set to {blockchain.difficulty}.")
        
        # Add blocks to the blockchain
        print("==== Adding blocks to the blockchain ====")
        transactions = [
            "Transaction 1: Jorge pays Vale 115 XRP",
            "Transaction 2: Vale pays Zero 45 XRP",
            "Transaction 3: Zero pays Jorge 78 XRP"
        ]
        
        for idx, transaction in enumerate(transactions, start=1):
            print(f"Mining block {idx}...")
            try:
                new_block = blockchain.add_block(transaction)
                print(f"Block {new_block.index} mined successfully! With hash: {new_block.hash}")
                
                # Check if the new block's hash is valid
                is_valid = new_block.is_valid_hash(blockchain.difficulty)
                print(f"¿Blockhain is valid after the new block? {new_block.index}? {is_valid}")
                
                # Check if the blockchain is valid after adding the new block
                blockchain_valid = blockchain.is_valid_chain()
                print(f"¿The blockchain is valid after adding block {new_block.index}? {blockchain_valid}")
            except Exception as e:
                print(f"Error adding block {idx}: {e}")
                
            time.sleep(1)
            
        # Display the blockchain
        print("==== Complete String Blockchain ====")
        blockchain.print_chain()
        
        # Simulate an attack on the blockchain
        AttackSimulation(blockchain)
        print("\n==== Final Summary ==== ")
        print(f"Blockchain Status: {blockchain.get_chain_info()}")   
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__ == "__main__":
    main()
