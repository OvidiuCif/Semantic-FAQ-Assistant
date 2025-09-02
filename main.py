from dotenv import load_dotenv
from resources.database_utilities import get_db_connection
from modules.chat_logic import process_user_query

load_dotenv()

def main():
    engine = get_db_connection()
    print("\nSemantic FAQ Assistant initialized\n Type 'quit', 'exit', 'bye', 'close', 'arrivederci' to end,\nHave fun!")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['quit', 'exit', 'bye', 'close', 'arrivederci']:
            break
            
        try:
            # process the query using the shared module // implemented for reusability in API
            response_data = process_user_query(user_input, engine)
            
            #display
            if response_data["used_faq"]:
                print(f"[Found similar FAQ with {response_data['similarity']:.2f} similarity]")
            else:
                print("[No relevant FAQ found]")
            

            print("\nSemantic-FAQ-Assistant:", response_data["answer"]) #remove logs/if to much
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()