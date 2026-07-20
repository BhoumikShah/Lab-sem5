def evaluate_profile(gre, score_eng, cgpa):
    target_gre = 320
    target_eng = 90
    target_cgpa = 8.0
    
    if gre > target_gre and score_eng > target_eng and cgpa > target_cgpa:
        return "YES it meets expectations"
    else:
        return "Not quite yet"

def graduate_admissions_bot():
    print("--- Graduate Admissions Eligibility Checker ---")
    print("Bot: Type 'evaluate' to check your profile or 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").lower().strip()
        
        if user_input == 'quit':
            print("Bot: Goodbye!")
            break
            
        elif user_input == 'evaluate':
            gre = float(input("Enter your GRE score: "))
            eng = float(input("Enter your TOEFL/IELTS score: "))
            cgpa = float(input("Enter your CGPA: "))
            
            result = evaluate_profile(gre, eng, cgpa)
            print(f"Bot: {result}")
            
        else:
            print("Bot:  Type 'evaluate' to check your profile.")
if __name__ == '__main__':
    graduate_admissions_bot()